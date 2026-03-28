"""MCP tools for Jira integration.

Each function here becomes a tool exposed by the FastMCP server. Tools cover
the full lifecycle: generating a ticket hierarchy from a PRD, creating
individual issues, querying, and transitioning status.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from jira_client import JiraClient
from config import JIRA_BASE_URL, JIRA_PROJECT_KEY

mcp = FastMCP("jira")


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from a Markdown file as a dict."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    import yaml  # lazy import — only needed when parsing PRDs
    return yaml.safe_load(match.group(1)) or {}


def _extract_sections(text: str) -> dict[str, str]:
    """Split Markdown body (after frontmatter) into {heading: content}."""
    # Strip frontmatter
    body = re.sub(r"^---.*?---\s*", "", text, count=1, flags=re.DOTALL)
    sections: dict[str, str] = {}
    current_heading = "_preamble"
    current_lines: list[str] = []
    for line in body.splitlines():
        heading_match = re.match(r"^#{1,3}\s+(.+)", line)
        if heading_match:
            sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = heading_match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    sections[current_heading] = "\n".join(current_lines).strip()
    return sections


def _extract_requirements(sections: dict[str, str]) -> list[dict]:
    """Extract functional requirements as a list of {id, text} dicts."""
    requirements = []
    for heading, content in sections.items():
        if "functional requirement" in heading.lower() or "requirements" in heading.lower():
            # Look for numbered or bulleted items
            for match in re.finditer(
                r"(?:^|\n)\s*(?:\d+[\.\)]\s*|[-*]\s+)(.+)", content
            ):
                req_text = match.group(1).strip()
                if req_text and len(req_text) > 10:  # skip trivial lines
                    requirements.append({"text": req_text})
    # Assign simple IDs
    for i, req in enumerate(requirements, 1):
        req["id"] = f"FR-{i:03d}"
    return requirements


def _extract_acceptance_criteria(sections: dict[str, str]) -> list[dict]:
    """Extract Given/When/Then acceptance criteria blocks."""
    criteria = []
    for heading, content in sections.items():
        if "acceptance" in heading.lower() or "criteria" in heading.lower():
            # Split on Given markers
            blocks = re.split(r"(?=\*?\*?Given\b)", content)
            for block in blocks:
                block = block.strip()
                if not block:
                    continue
                given = re.search(r"Given\s+(.+?)(?=When|$)", block, re.DOTALL | re.IGNORECASE)
                when = re.search(r"When\s+(.+?)(?=Then|$)", block, re.DOTALL | re.IGNORECASE)
                then = re.search(r"Then\s+(.+?)(?=$)", block, re.DOTALL | re.IGNORECASE)
                if given and when and then:
                    criteria.append({
                        "given": given.group(1).strip().rstrip(",").strip(),
                        "when": when.group(1).strip().rstrip(",").strip(),
                        "then": then.group(1).strip(),
                    })
    for i, ac in enumerate(criteria, 1):
        ac["id"] = f"AC-{i:03d}"
    return criteria


def _build_hierarchy(
    prd_meta: dict,
    prd_title: str,
    requirements: list[dict],
    acceptance_criteria: list[dict],
) -> dict:
    """Build the Epic / Story / Task hierarchy dict from parsed PRD data."""
    epic = {
        "type": "Epic",
        "summary": prd_title,
        "description": (
            f"Epic generated from PRD {prd_meta.get('id', 'unknown')}. "
            f"Priority: {prd_meta.get('priority', 'unset')}."
        ),
        "stories": [],
    }

    # One Story per functional requirement
    for req in requirements:
        story = {
            "type": "Story",
            "summary": req["text"][:200],
            "description": f"[{req['id']}] {req['text']}",
            "tasks": [],
        }
        epic["stories"].append(story)

    # Distribute acceptance criteria as Tasks under Stories.
    # If more ACs than stories, extras go under the last story.
    if epic["stories"]:
        for i, ac in enumerate(acceptance_criteria):
            story_index = min(i, len(epic["stories"]) - 1)
            task_summary = f"AC: Given {ac['given'][:80]}..."
            task_desc = (
                f"**Given** {ac['given']}\n"
                f"**When** {ac['when']}\n"
                f"**Then** {ac['then']}"
            )
            epic["stories"][story_index]["tasks"].append({
                "type": "Task",
                "summary": task_summary,
                "description": task_desc,
                "ac_id": ac["id"],
            })
    elif acceptance_criteria:
        # No requirements parsed — make one story from the PRD title
        story = {
            "type": "Story",
            "summary": f"Implement: {prd_title[:180]}",
            "description": f"Story for PRD {prd_meta.get('id', 'unknown')}",
            "tasks": [],
        }
        for ac in acceptance_criteria:
            story["tasks"].append({
                "type": "Task",
                "summary": f"AC: Given {ac['given'][:80]}...",
                "description": (
                    f"**Given** {ac['given']}\n"
                    f"**When** {ac['when']}\n"
                    f"**Then** {ac['then']}"
                ),
                "ac_id": ac["id"],
            })
        epic["stories"].append(story)

    return epic


# ------------------------------------------------------------------
# MCP Tools
# ------------------------------------------------------------------

@mcp.tool()
async def generate_ticket_hierarchy(
    prd_path: str,
    project_key: str = "",
    dry_run: bool = True,
) -> str:
    """Read a PRD file and generate an Epic/Story/Task ticket hierarchy for Jira.

    Parses the PRD's functional requirements into Stories and acceptance
    criteria into Tasks (sub-tasks). If dry_run is True (default), returns
    the planned hierarchy as JSON without creating anything in Jira. If
    dry_run is False, creates all tickets in Jira and returns the created
    issue keys.

    Args:
        prd_path: Path to the PRD Markdown file (relative to project root or absolute).
        project_key: Jira project key (e.g. "PM"). Falls back to JIRA_PROJECT_KEY env var.
        dry_run: If True, return planned hierarchy without creating tickets.
                 If False, create the tickets in Jira.
    """
    project_key = project_key or JIRA_PROJECT_KEY
    if not project_key:
        return json.dumps({
            "error": "No project_key provided and JIRA_PROJECT_KEY env var is not set."
        })

    # Read and parse the PRD
    prd_file = Path(prd_path)
    if not prd_file.is_absolute():
        prd_file = Path.cwd() / prd_file
    if not prd_file.exists():
        return json.dumps({"error": f"PRD file not found: {prd_file}"})

    text = prd_file.read_text(encoding="utf-8")
    meta = _parse_frontmatter(text)
    sections = _extract_sections(text)
    requirements = _extract_requirements(sections)
    acceptance_criteria = _extract_acceptance_criteria(sections)

    prd_title = meta.get("title", prd_file.stem.replace("-", " ").title())
    hierarchy = _build_hierarchy(meta, prd_title, requirements, acceptance_criteria)

    if dry_run:
        return json.dumps({
            "mode": "dry_run",
            "project_key": project_key,
            "prd_id": meta.get("id", "unknown"),
            "prd_title": prd_title,
            "stats": {
                "stories": len(hierarchy["stories"]),
                "tasks": sum(len(s["tasks"]) for s in hierarchy["stories"]),
            },
            "hierarchy": hierarchy,
        }, indent=2)

    # Live run — create tickets in Jira
    created: dict = {"epic": None, "stories": [], "tasks": []}
    async with JiraClient() as jira:
        epic_key = await jira.create_issue(
            project_key=project_key,
            issue_type="Epic",
            summary=hierarchy["summary"],
            description=hierarchy["description"],
            labels=["pm-assistant"],
        )
        created["epic"] = epic_key

        for story in hierarchy["stories"]:
            story_key = await jira.create_issue(
                project_key=project_key,
                issue_type="Story",
                summary=story["summary"],
                description=story["description"],
                parent_key=epic_key,
                labels=["pm-assistant"],
            )
            created["stories"].append(story_key)

            for task in story["tasks"]:
                task_key = await jira.create_issue(
                    project_key=project_key,
                    issue_type="Sub-task",
                    summary=task["summary"],
                    description=task["description"],
                    parent_key=story_key,
                    labels=["pm-assistant"],
                )
                created["tasks"].append(task_key)

    base_url = JIRA_BASE_URL
    return json.dumps({
        "mode": "created",
        "project_key": project_key,
        "prd_id": meta.get("id", "unknown"),
        "created": created,
        "links": {
            "epic": f"{base_url}/browse/{created['epic']}",
            "stories": [f"{base_url}/browse/{k}" for k in created["stories"]],
            "tasks": [f"{base_url}/browse/{k}" for k in created["tasks"]],
        },
    }, indent=2)


@mcp.tool()
async def create_epic(
    project_key: str,
    summary: str,
    description: str,
) -> str:
    """Create a single Epic in Jira.

    Args:
        project_key: Jira project key (e.g. "PM").
        summary: Epic title / summary.
        description: Detailed description of the epic.

    Returns:
        JSON with the created epic key and browse URL.
    """
    async with JiraClient() as jira:
        key = await jira.create_issue(
            project_key=project_key,
            issue_type="Epic",
            summary=summary,
            description=description,
            labels=["pm-assistant"],
        )
    return json.dumps({
        "key": key,
        "url": f"{JIRA_BASE_URL}/browse/{key}",
    })


@mcp.tool()
async def create_story(
    project_key: str,
    epic_key: str,
    summary: str,
    description: str,
    acceptance_criteria: str = "",
) -> str:
    """Create a Story linked to an Epic in Jira.

    Acceptance criteria are appended to the description so they appear
    directly on the Story ticket.

    Args:
        project_key: Jira project key (e.g. "PM").
        epic_key: The parent Epic's issue key (e.g. "PM-1").
        summary: Story title / summary.
        description: Story description.
        acceptance_criteria: Given/When/Then acceptance criteria text.

    Returns:
        JSON with the created story key and browse URL.
    """
    full_description = description
    if acceptance_criteria:
        full_description += f"\n\n--- Acceptance Criteria ---\n{acceptance_criteria}"

    async with JiraClient() as jira:
        key = await jira.create_issue(
            project_key=project_key,
            issue_type="Story",
            summary=summary,
            description=full_description,
            parent_key=epic_key,
            labels=["pm-assistant"],
        )
    return json.dumps({
        "key": key,
        "url": f"{JIRA_BASE_URL}/browse/{key}",
    })


@mcp.tool()
async def create_task(
    project_key: str,
    parent_key: str,
    summary: str,
    description: str,
) -> str:
    """Create a sub-task under a Story or Epic in Jira.

    Args:
        project_key: Jira project key (e.g. "PM").
        parent_key: Parent issue key (Story or Epic, e.g. "PM-5").
        summary: Task title / summary.
        description: Task description.

    Returns:
        JSON with the created task key and browse URL.
    """
    async with JiraClient() as jira:
        key = await jira.create_issue(
            project_key=project_key,
            issue_type="Sub-task",
            summary=summary,
            description=description,
            parent_key=parent_key,
            labels=["pm-assistant"],
        )
    return json.dumps({
        "key": key,
        "url": f"{JIRA_BASE_URL}/browse/{key}",
    })


@mcp.tool()
async def get_issues(
    project_key: str,
    issue_type: str = "",
    status: str = "",
) -> str:
    """Query Jira issues with optional filters for type and status.

    Args:
        project_key: Jira project key to search within.
        issue_type: Filter by issue type (e.g. "Epic", "Story", "Task"). Optional.
        status: Filter by status (e.g. "To Do", "In Progress", "Done"). Optional.

    Returns:
        JSON array of matching issues with key, summary, status, and type.
    """
    clauses = [f'project = "{project_key}"']
    if issue_type:
        clauses.append(f'issuetype = "{issue_type}"')
    if status:
        clauses.append(f'status = "{status}"')
    jql = " AND ".join(clauses) + " ORDER BY created DESC"

    async with JiraClient() as jira:
        issues = await jira.search_issues(jql)

    results = []
    for issue in issues:
        fields = issue.get("fields", {})
        results.append({
            "key": issue["key"],
            "summary": fields.get("summary", ""),
            "status": fields.get("status", {}).get("name", ""),
            "type": fields.get("issuetype", {}).get("name", ""),
            "priority": fields.get("priority", {}).get("name", ""),
            "url": f"{JIRA_BASE_URL}/browse/{issue['key']}",
        })

    return json.dumps(results, indent=2)


@mcp.tool()
async def transition_issue(
    issue_key: str,
    status: str,
) -> str:
    """Move a Jira issue to a new status.

    The status name must match an available transition for the issue
    (e.g. "In Progress", "Done", "To Do"). The tool will list available
    transitions if the requested one is not valid.

    Args:
        issue_key: The issue key to transition (e.g. "PM-42").
        status: The target status/transition name.

    Returns:
        JSON confirmation or error with available transitions.
    """
    async with JiraClient() as jira:
        try:
            await jira.transition_issue(issue_key, status)
            return json.dumps({
                "success": True,
                "issue_key": issue_key,
                "new_status": status,
                "url": f"{JIRA_BASE_URL}/browse/{issue_key}",
            })
        except Exception as e:
            return json.dumps({
                "success": False,
                "issue_key": issue_key,
                "error": str(e),
            })
