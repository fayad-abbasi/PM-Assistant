# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered PM workflow running natively in Claude Code — no web app, no API server. The entire workflow operates through slash commands (`.claude/commands/`), hooks, subagents, MCP servers, and file storage. All artifacts live as Markdown/JSON files in `data/`, git-versioned.

## Architecture

No web app. No FastAPI. No React. The entire PM workflow runs **inside Claude Code** using its native primitives. You talk to Claude Code in natural language. Slash commands give structured entry points. Everything stays in files you can read, edit, and version control.

### Core Primitives

| Primitive | Location | Role |
|-----------|----------|------|
| **Slash commands** | `.claude/commands/*.md` | User-invocable skills for each workflow step |
| **Prompt templates** | `prompts/` | Reusable prompts read by commands during generation |
| **Hooks** | `.claude/settings.json` | Session-start context injection + automated validation on write events |
| **Subagents** | (runtime) | `general-purpose` for generation (read + write), `Explore` for read-only analysis |
| **MCP servers** | `mcp-servers/` | External tool integrations (Jira, Slack, etc.) — Python FastMCP via `uv` |
| **Data** | `data/` | All PM artifacts as Markdown/JSON files — the source of truth |
| **Meta** | `data/meta/` | Shared metadata: tag taxonomy, ID counters, tag definitions, learnings |
| **Background** | `background_information/` | PM frameworks and reference material — ingested via `/ingest`. **Local-only** — not included in the repo. Place your own PM books, course summaries, and framework references here and run `/ingest scan` to integrate them into the workflow. |

### Design Principles

1. **File-native**: Every artifact is a file. No database, no state outside `data/`.
2. **Git-versioned**: All work is tracked in version control. Diffs show what changed and when.
3. **Evidence-traced**: Every PRD links to insights, every insight links to interviews, every OKR links to evidence. The chain is auditable.
4. **Quality-gated**: Generated artifacts are auto-scored against rubrics. Below-threshold outputs get fixed before being presented.
5. **Continuously improvable**: New frameworks drop into `background_information/`, `/ingest` evaluates and integrates them into the workflow.

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/discover` | Manage interviews, run analysis, import analytics |
| `/prd` | Create, generate, edit, convert PRDs |
| `/gtm` | Draft audience-specific messages from PRDs |
| `/strategy` | Vision, OKRs, roadmap, competitive analysis |
| `/ost` | Opportunity Solution Trees — outcome → opportunities → solutions → assumption tests → decision |
| `/ux` | Journey maps, design references |
| `/uat` | Test case generation, execution tracking, reports |
| `/outcomes` | Post-launch metrics, impact reports |
| `/retro` | Retrospectives, lessons learned, strategy feedback loops |
| `/status` | Stakeholder reports, decision log, meeting notes |
| `/jira` | Create Jira tickets from PRDs (via MCP) |
| `/eval` | Run quality evaluations on AI outputs |
| `/search` | Cross-artifact search and query by tags, links, content |
| `/pm-dash` | Overview dashboard with data quality flags |
| `/quick-insight` | Fast capture — paste a quote, get a tagged insight in one step |
| `/weekly` | One-shot status report + dashboard for end-of-week wrap-up |
| `/link-check` | Verify all cross-links, tags, and workflow rules across data/ |
| `/next` | Prioritized recommendations for what to work on next |
| `/quality-check` | Post-generation structural + content quality validation |
| `/refresh` | Re-inject session context on demand (same as session-start hook, mid-session) |

## Data Conventions

- All data files use **YAML frontmatter** with required fields: `id`, `title`, `created_at`
- IDs follow the pattern `{type}-{YYYY-MM-DD}-{NNN}` — counters tracked in `data/meta/counters.json`
- When creating an artifact: read counters.json, increment, use as ID, write counters back
- Dates in ISO 8601 format
- Files are Markdown (`.md`) for human-readable artifacts, JSON (`.json`) for structured data
- Filenames use kebab-case
- Tags must exist in `data/meta/tags.json` — add new tags there first

### Status Enums by Type

- **Interviews**: `raw` | `analyzed`
- **Insights**: `active` | `superseded` | `archived`
- **PRDs**: `draft` | `review` | `approved` | `deprecated`
- **GTM drafts**: `draft` | `approved`
- **OKRs**: `active` | `completed` | `abandoned`
- **Roadmap items**: `planned` | `in-progress` | `completed` | `deferred`
- **Test cases**: `pending` | `pass` | `fail` | `blocked`
- **Outcomes**: `on-track` | `partially-met` | `met` | `missed`
- **OSTs**: `exploring` | `testing` | `decided` | `implemented`

## Frontmatter Schemas

### Interview (`data/interviews/*.md`)
```yaml
id: interview-{date}-{NNN}
title: string
date: ISO-date
interviewee: string
role: string
company: string
tags: [from tags.json]
status: raw | analyzed
created_at: ISO-datetime
```

### Insight (`data/insights/*.md`)
```yaml
id: insight-{date}-{NNN}
title: string
type: single | batch
linked_interviews: [interview IDs]
themes: [strings]
confidence: low | medium | high
impact: low | medium | high
tags: [from tags.json]
status: active | superseded | archived
created_at: ISO-datetime
```

### PRD (`data/prds/*.md`)
```yaml
id: prd-{date}-{NNN}
title: string
status: draft | review | approved | deprecated
priority: critical | high | medium | low
linked_insights: [insight IDs]
okr_ids: [OKR IDs]
roadmap_ids: [roadmap IDs]
tags: [from tags.json]
created_at: ISO-datetime
updated_at: ISO-datetime
```

### OKR (`data/strategy/okrs/*.json`)
Fields: id, objective, period, key_results[], status, created_at

### Roadmap Item (`data/strategy/roadmap/*.json`)
Fields: id, title, description, quarter, status, priority, linked_prds[], okr_ids[], created_at

### OST (`data/strategy/ost/*.md`)
```yaml
id: ost-{date}-{NNN}
title: string
outcome: string
okr_id: string or null
linked_insights: [insight IDs]
selected_solution: string or null
prd_id: string or null
status: exploring | testing | decided | implemented
tags: [from tags.json]
created_at: ISO-datetime
updated_at: ISO-datetime
```

### GTM Draft (`data/gtm/drafts/*.md`)
Fields: id, title, prd_id, audience (developer|engineering-manager|tech-lead|engineering-leadership|executive|compliance|finance), status, tags, created_at

### Journey Map (`data/ux/journeys/*.md`)
Fields: id, title, persona, linked_interviews[], linked_prds[], tags, created_at

### Test Case (`data/uat/test-cases/*.json`)
Fields: id, title, prd_id, acceptance_criterion, given, when, then, status, result_notes, executed_at, created_at

### Outcome Record (`data/outcomes/records/*.json`)
Fields: id, prd_id, okr_ids[], metric, expected, actual, unit, delta, assessment, tags, recorded_at, created_at

### Retrospective (`data/retros/*.md`)
Fields: id, title, period, linked_prds[], linked_outcomes[], okr_ids[], tags, created_at

### Decision Log (`data/stakeholder/decisions/*.md`)
Fields: id, title, decision, participants[], linked_prds[], tags, created_at

### Status Report (`data/stakeholder/reports/*.md`)
Fields: id, title, period, tags, created_at

### Meeting Notes (`data/stakeholder/meetings/*.md`)
Fields: id, title, date, attendees[], action_items[], tags, created_at

### Eval Result (`data/evals/*.json`)
Fields: id, artifact_id, artifact_type, rubric, scores{}, max_score, feedback, created_at

### Person Page (`data/stakeholder/people/*.md`)
```yaml
id: person-{slug}
name: string
role: string
company: string
relationship: stakeholder | team | executive | customer | partner
tags: [from tags.json]
created_at: ISO-datetime
updated_at: ISO-datetime
```
Body: Living profile with sections — Background, Priorities, Communication Style, Interaction Log (appended over time), Open Commitments

### Learnings (`data/meta/learnings.md`)
Not frontmatter-based. Append-only file capturing Claude's mistakes and corrections. Injected into every session via session-start hook.

## Workflow Rules

1. Every PRD must link to at least one insight
2. Every insight must link to its source interviews
3. Acceptance criteria must be in **Given/When/Then** format
4. GTM drafts must specify the source PRD and target audience
5. Test cases must reference the acceptance criterion they validate
6. Outcome records must link to the PRD and relevant OKRs
7. Use `general-purpose` subagents for generation tasks (they write files directly)
8. Use `Explore` subagents for read-only analysis (they return results)
9. Tags must exist in `data/meta/tags.json` — add new tags there first
10. Always read and update `data/meta/counters.json` when creating new artifacts
11. **Verification loop**: After generating an artifact (insight, PRD, GTM draft, journey map), auto-run the quality-checker — score against the eval rubric, fix issues if below threshold (avg >= 3.5, all dimensions >= 3), save the eval result. Present the final artifact only after it passes.
12. **Quality-checker**: `/quality-check` validates structure (frontmatter, links, tags, rules) + content quality (rubric scoring). Called automatically by generation commands or standalone.
13. PRDs should link to an OST when one exists — the OST provides the evidence trail from outcome to solution
14. Before creating a PRD for a non-trivial initiative, consider building an OST first to explore alternatives and test assumptions

## MCP Servers

All servers use Python + FastMCP + httpx, run via `uv`. Configured in `.claude/settings.json`, env vars sourced from `.env`.

| Server | Directory | Purpose |
|--------|-----------|---------|
| Jira | `mcp-servers/jira-server/` | Jira Cloud CRUD (epics, stories, tasks, transitions) |
| Miro | `mcp-servers/miro-server/` | Affinity maps, visual journey maps, mind maps |
| Lucid | `mcp-servers/lucid-server/` | Flowcharts, architecture diagrams |
| Figma | `mcp-servers/figma-server/` | Design file access, asset export, comments |
| Slack | `mcp-servers/slack-server/` | Search messages, post updates, read threads, channel history |

Note: MCP servers are placeholders until the actual tool stack is confirmed in the new role.

## Example Workflows

### Discovery → Strategy → Execution (Full Lifecycle)

```
/discover              → Add and analyze interviews with internal engineers
/discover batch        → Cross-cutting patterns across interviews
/ost                   → Map outcome → opportunities → solutions → assumption tests
/discover test-assumption → Run and record assumption tests
/ost resume            → Review results, pick winning solution
/prd                   → Generate PRD from OST decision (pre-populated)
/strategy okrs         → Define outcome-focused OKRs linked to PRD
/strategy roadmap      → Add roadmap items linked to OKRs
/gtm internal          → Draft internal adoption messaging (4 engineering audiences)
/uat                   → Generate test cases from PRD acceptance criteria
/outcomes              → Track post-launch metrics against OKR targets
/retro                 → Retrospective feeding learnings back to strategy
```

### Day-to-Day Quick Captures

```
/quick-insight         → Paste a quote or observation, get a tagged insight instantly
/status meeting        → Paste rough meeting notes, get structured notes + action items
/status person         → Create or update a stakeholder profile
/weekly ramp-up        → End-of-week summary: who you met, what you learned, what's next
```

### Continuous Improvement

```
/ingest scan           → Check for new background material
/ingest review         → Evaluate how new material could improve the workflow
/ingest apply          → Apply recommended changes to prompts, rubrics, commands
/pm-dash               → Dashboard with artifact counts, quality flags, traceability health
/link-check            → Verify all cross-references and tag validity
/eval                  → Score any artifact against its rubric
```

### Thinking and Problem Solving

```
/grill-me              → Stress-test a plan — confrontational, one question at a time
/grill-me --conversation → Thought partner — collaborative exploration of a half-formed idea
```

## Future Enhancements

### End-to-End Testing
Automated end-to-end verification of the full artifact chain: interview → insight → OST → PRD → GTM → UAT → outcomes → retro. Should validate that cross-links resolve, eval scores meet thresholds, and all workflow rules are satisfied. Could be a `/verify` command or part of `/pm-dash`.

### MCP Server Activation
Once the tool stack is confirmed in the new role, activate and configure the relevant MCP servers (likely Jira and Slack first). Update `/jira`, `/status`, and `/discover` to leverage live integrations.

### Workflow Analytics
Track meta-metrics about the PM workflow itself: average eval scores over time, time between interview and insight, number of assumption tests per OST, PRD cycle time. Surface trends in `/pm-dash`.

### Template Library
Curated templates for common DevEx scenarios: platform migration PRDs, developer tool adoption campaigns, service deprecation plans, golden path proposals. Accessible via `/prd --template`.

### Multi-Product Support
If the role expands to cover multiple products or platforms, add product/area scoping to artifacts and commands so `/pm-dash` and `/search` can filter by product context.
