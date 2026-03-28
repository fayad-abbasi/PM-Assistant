"""Async HTTP client for Jira REST API v3.

Uses httpx with basic auth (email + API token). All methods raise
descriptive errors for common failure modes (auth, not-found, permissions).
"""

from __future__ import annotations

import httpx

from config import JIRA_API_BASE, JIRA_EMAIL, JIRA_API_TOKEN


class JiraError(Exception):
    """Base error for Jira API failures."""


class JiraAuthError(JiraError):
    """Authentication failed — check JIRA_EMAIL and JIRA_API_TOKEN."""


class JiraNotFoundError(JiraError):
    """The requested resource was not found."""


class JiraPermissionError(JiraError):
    """Insufficient permissions for this operation."""


def _raise_for_status(response: httpx.Response) -> None:
    """Translate HTTP status codes into descriptive exceptions."""
    if response.is_success:
        return
    status = response.status_code
    try:
        body = response.json()
        messages = body.get("errorMessages", [])
        errors = body.get("errors", {})
        detail = "; ".join(messages) if messages else str(errors)
    except Exception:
        detail = response.text[:500]

    if status == 401:
        raise JiraAuthError(
            f"Authentication failed (HTTP 401). Verify JIRA_EMAIL and "
            f"JIRA_API_TOKEN are correct. Detail: {detail}"
        )
    if status == 403:
        raise JiraPermissionError(
            f"Permission denied (HTTP 403). The API token may lack the "
            f"required project permissions. Detail: {detail}"
        )
    if status == 404:
        raise JiraNotFoundError(
            f"Not found (HTTP 404). The issue, project, or resource does "
            f"not exist. Detail: {detail}"
        )
    raise JiraError(f"Jira API error (HTTP {status}): {detail}")


class JiraClient:
    """Async Jira REST API v3 client.

    Use as an async context manager::

        async with JiraClient() as jira:
            key = await jira.create_issue(...)
    """

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "JiraClient":
        self._client = httpx.AsyncClient(
            base_url=JIRA_API_BASE,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
        return self

    async def __aexit__(self, *exc) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("JiraClient must be used as an async context manager")
        return self._client

    # ------------------------------------------------------------------
    # Issue CRUD
    # ------------------------------------------------------------------

    async def create_issue(
        self,
        project_key: str,
        issue_type: str,
        summary: str,
        description: str,
        parent_key: str | None = None,
        labels: list[str] | None = None,
    ) -> str:
        """Create a Jira issue and return its key (e.g. 'PROJ-42').

        Parameters
        ----------
        project_key : str
            The Jira project key (e.g. "PM").
        issue_type : str
            Issue type name: "Epic", "Story", "Task", "Sub-task", etc.
        summary : str
            One-line summary / title.
        description : str
            Full description in Atlassian Document Format (ADF) plain text
            will be wrapped automatically.
        parent_key : str, optional
            Parent issue key for sub-tasks or stories under an epic.
        labels : list[str], optional
            Labels to apply to the issue.
        """
        # Wrap plain text description into minimal ADF
        adf_description = {
            "version": 1,
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": description}],
                }
            ],
        }

        fields: dict = {
            "project": {"key": project_key},
            "issuetype": {"name": issue_type},
            "summary": summary,
            "description": adf_description,
        }

        if parent_key:
            fields["parent"] = {"key": parent_key}

        if labels:
            fields["labels"] = labels

        resp = await self.client.post("/issue", json={"fields": fields})
        _raise_for_status(resp)
        data = resp.json()
        return data["key"]

    async def get_issue(self, issue_key: str) -> dict:
        """Fetch full issue data by key."""
        resp = await self.client.get(f"/issue/{issue_key}")
        _raise_for_status(resp)
        return resp.json()

    async def search_issues(self, jql: str, max_results: int = 50) -> list[dict]:
        """Search issues using JQL. Returns a list of issue dicts."""
        resp = await self.client.post(
            "/search",
            json={
                "jql": jql,
                "maxResults": max_results,
                "fields": [
                    "summary",
                    "status",
                    "issuetype",
                    "priority",
                    "parent",
                    "labels",
                    "assignee",
                ],
            },
        )
        _raise_for_status(resp)
        return resp.json().get("issues", [])

    async def transition_issue(self, issue_key: str, transition_name: str) -> None:
        """Transition an issue to a new status by transition name.

        First fetches available transitions, then executes the matching one.
        Raises JiraError if the requested transition is not available.
        """
        # Get available transitions
        resp = await self.client.get(f"/issue/{issue_key}/transitions")
        _raise_for_status(resp)
        transitions = resp.json().get("transitions", [])

        target = None
        available_names = []
        for t in transitions:
            available_names.append(t["name"])
            if t["name"].lower() == transition_name.lower():
                target = t
                break

        if target is None:
            raise JiraError(
                f"Transition '{transition_name}' is not available for "
                f"{issue_key}. Available transitions: {available_names}"
            )

        resp = await self.client.post(
            f"/issue/{issue_key}/transitions",
            json={"transition": {"id": target["id"]}},
        )
        _raise_for_status(resp)

    async def add_comment(self, issue_key: str, body: str) -> dict:
        """Add a comment to an issue. Returns the created comment data."""
        adf_body = {
            "version": 1,
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": body}],
                }
            ],
        }
        resp = await self.client.post(
            f"/issue/{issue_key}/comment",
            json={"body": adf_body},
        )
        _raise_for_status(resp)
        return resp.json()
