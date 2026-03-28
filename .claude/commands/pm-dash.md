# PM Dashboard

You are the PM Dashboard. Provide a quick overview of all artifacts in the PM workflow, with counts, status breakdowns, and data quality flags.

## How to Run

When the user invokes `/pm-dash`, use an `Explore` subagent to scan across all `data/` directories and produce a dashboard report.

## Dashboard Sections

### 1. Artifact Counts

Read all directories and count files (excluding .gitkeep):

| Artifact | Directory | Count |
|----------|-----------|-------|
| Interviews | `data/interviews/` | {n} |
| Insights | `data/insights/` | {n} |
| PRDs | `data/prds/` | {n} |
| OKRs | `data/strategy/okrs/` | {n} |
| Roadmap Items | `data/strategy/roadmap/` | {n} |
| Vision Docs | `data/strategy/vision/` | {n} |
| Competitor Profiles | `data/strategy/competitors/` | {n} |
| Journey Maps | `data/ux/journeys/` | {n} |
| GTM Drafts | `data/gtm/drafts/` | {n} |
| Test Cases | `data/uat/test-cases/` | {n} |
| UAT Reports | `data/uat/reports/` | {n} |
| Outcome Records | `data/outcomes/records/` | {n} |
| Impact Reports | `data/outcomes/reports/` | {n} |
| Retrospectives | `data/retros/` | {n} |
| Status Reports | `data/stakeholder/reports/` | {n} |
| Decisions | `data/stakeholder/decisions/` | {n} |
| Meeting Notes | `data/stakeholder/meetings/` | {n} |
| Eval Results | `data/evals/` | {n} |

### 2. Status Breakdowns

For artifact types with status fields, show the breakdown:

**Interviews**: {n} raw | {n} analyzed
**Insights**: {n} active | {n} superseded | {n} archived
**PRDs**: {n} draft | {n} review | {n} approved | {n} deprecated
**OKRs**: {n} active | {n} completed | {n} abandoned
**Roadmap**: {n} planned | {n} in-progress | {n} completed | {n} deferred
**Test Cases**: {n} pending | {n} pass | {n} fail | {n} blocked
**Outcomes**: {n} on-track | {n} partially-met | {n} met | {n} missed

### 3. Recent Activity

Show the 5 most recently created/updated artifacts across all types, sorted by `created_at` or `updated_at`.

### 4. Data Quality Flags

Check for and report issues organized by severity:

**❌ Errors (workflow rule violations):**
- **Unlinked PRDs**: PRDs with empty `linked_insights` (violates workflow rule #1)
- **Missing acceptance criteria**: PRDs that don't contain "Given" / "When" / "Then" in body (violates rule #3)
- **Broken cross-links**: Any `linked_*`, `*_ids`, or `prd_id` values that don't resolve to existing files
- **Unknown tags**: Any tags in frontmatter not found in `data/meta/tags.json`
- **Orphaned insights**: Insights whose `linked_interviews` reference IDs that don't exist (violates rule #2)

**⚠️ Warnings (quality gaps):**
- **Unanalyzed interviews**: Interviews with `status: raw` — no insight has been extracted yet
- **PRDs without OKRs**: PRDs with empty `okr_ids` — not linked to strategy (strategic drift risk)
- **PRDs without test cases**: PRDs that have no test cases in `data/uat/test-cases/`
- **PRDs without GTM**: Approved PRDs that have no GTM drafts in `data/gtm/drafts/`
- **Stale drafts**: PRDs in `draft` status for more than 14 days (based on `created_at`)
- **OKRs without outcomes**: Active OKRs that have no outcome records tracking progress
- **Roadmap items without PRDs**: Roadmap items with empty `linked_prds` — planned work not yet defined
- **Low eval scores**: Artifacts with eval scores averaging below 3.0

**💡 Suggestions (opportunities):**
- **Unlinked journeys**: PRDs that have no journey map — user experience not mapped
- **Missing retros**: Completed PRDs or periods with no retrospective
- **Unevaluated artifacts**: PRDs or insights that have never been scored by `/eval`

### 4b. Traceability Health

Show a quick traceability chain status — how well-connected is the artifact graph?

```
Interviews → Insights:  {n}/{total} interviews have linked insights ({pct}%)
Insights → PRDs:        {n}/{total} insights are linked from PRDs ({pct}%)
PRDs → OKRs:           {n}/{total} PRDs link to OKRs ({pct}%)
PRDs → Roadmap:        {n}/{total} PRDs link to roadmap items ({pct}%)
PRDs → Test Cases:     {n}/{total} PRDs have test cases ({pct}%)
PRDs → GTM:            {n}/{total} PRDs have GTM drafts ({pct}%)
PRDs → Outcomes:       {n}/{total} PRDs have outcome records ({pct}%)
OKRs → Outcomes:       {n}/{total} OKR key results have outcome data ({pct}%)
```

Flag any chain with <50% coverage as ⚠️ and <25% as ❌.

### 5. Workflow Coverage

Show which stages of the PM lifecycle have content:

```
Discovery:  [✓] Interviews  [✓] Insights  [ ] Analytics
Strategy:   [ ] Vision      [ ] OKRs      [ ] Roadmap    [ ] Competitors
Definition: [✓] PRDs        [ ] Journeys
GTM:        [ ] Drafts
Validation: [ ] Test Cases  [ ] UAT Reports
Outcomes:   [ ] Records     [ ] Impact Reports
Learning:   [ ] Retros      [ ] Decisions
```

Use ✓ for directories with content, empty box for empty directories.

---

## Output Format

Present the dashboard as a clean Markdown report directly in the conversation. Do not save to a file unless the user asks.

## Rules

- Use an `Explore` subagent to read across all data directories
- Parse both YAML frontmatter (.md files) and JSON files
- Skip .gitkeep files in counts
- Flag issues clearly with a severity indicator: ⚠️ warning, ❌ error
- Keep the output concise — this is a quick health check, not a deep analysis

---

## Next Steps (suggest based on flags)

| Flag | Suggest |
|------|---------|
| Unanalyzed interviews | "Run `/discover` to analyze them" |
| PRDs without OKRs | "Run `/strategy` to define and link OKRs" |
| No journey maps | "Run `/ux` to create journey maps from interviews" |
| No test cases | "Run `/uat` to generate test cases from PRD acceptance criteria" |
| No outcomes | "Run `/outcomes` to record post-launch metrics" |
| Stale drafts | "Review and advance these PRDs to `review` status" |
