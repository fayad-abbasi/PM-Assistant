# Weekly

One-shot command that generates both a status report and a dashboard in a single invocation. Designed for end-of-week wrap-up — no menus, no questions.

**Accepts an optional argument**: `/weekly ramp-up` for first-30-days mode.

## Mode Detection

- `/weekly` or `/weekly standard` — standard status report + dashboard
- `/weekly ramp-up` — first-30-days ramp-up report + dashboard (see Ramp-Up Mode below)

---

## Standard Mode

Run both of these in parallel using subagents:

### 1. Status Report (general-purpose subagent)

- Determine the current week period (e.g., "2026-W11")
- Read `prompts/stakeholder/generate-status-report.md`
- Read `data/meta/counters.json`, increment the `status` counter, write back
- Read across all `data/` directories: OKRs, roadmap items, PRDs, outcomes, decisions, recent insights, meetings
- Write the status report to `data/stakeholder/reports/status-{week}-{NNN}.md` with frontmatter:
```yaml
---
id: status-{week}-{NNN}
title: "Week {N} Status Report"
period: "{YYYY-WNN}"
tags: []
created_at: {ISO-datetime}
---
```

### 2. Dashboard (Explore subagent)

Run the full `/pm-dash` dashboard scan:
- Artifact counts across all `data/` directories
- Status breakdowns per type
- Recent activity (5 most recent artifacts)
- Data quality flags (errors, warnings, suggestions)
- Traceability health percentages
- Workflow coverage checklist

---

## Ramp-Up Mode (`/weekly ramp-up`)

Designed for the first 30-60 days in a new role. Produces a "here's what I'm learning" summary instead of a project status report. Run both in parallel:

### 1. Ramp-Up Report (general-purpose subagent)

- Determine the current week period and calculate which week of ramp-up this is (Week 1, Week 2, etc.)
- Read `data/meta/counters.json`, increment the `status` counter, write back
- Read across these directories for ramp-up context:
  - `data/interviews/` — who you've talked to, key themes
  - `data/insights/` — patterns emerging from conversations
  - `data/stakeholder/meetings/` — meetings attended, action items
  - `data/stakeholder/people/` — relationship map built so far
  - `data/stakeholder/decisions/` — decisions observed or participated in
- Generate a ramp-up report with these sections:

```markdown
## Ramp-Up Week {N} Summary

### People Met This Week
{Table: Name | Role | Team | Key Takeaway}
{Pull from interviews, meetings, and person pages created this week}

### Key Learnings
{Bulleted list of the most important things learned this week}
{Grounded in interview insights and meeting notes}

### Emerging Themes
{3-5 themes crystallizing from conversations}
{Reference specific interviews/insights}

### Open Questions
{Questions that need answering — things you're still trying to understand}
{Flag who might be able to answer each one}

### Relationships to Build
{People you haven't met yet but should, based on what you've learned}

### Next Week Focus
{Where to direct attention based on what you learned this week}
```

- Write to `data/stakeholder/reports/ramp-up-{week}-{NNN}.md` with frontmatter:
```yaml
---
id: status-{week}-{NNN}
title: "Ramp-Up Week {N} Report"
period: "{YYYY-WNN}"
tags: [developer-onboarding]
created_at: {ISO-datetime}
---
```

### 2. Dashboard (Explore subagent)

Same as standard mode — run the full `/pm-dash` dashboard scan.

---

## Output

Present both results in a single response:

**Standard mode:**
```
STATUS REPORT saved: data/stakeholder/reports/status-2026-W11-001.md

Highlights:
- {2-3 bullet summary of the week}

---

DASHBOARD — 2026-03-13

{full dashboard output from /pm-dash}
```

**Ramp-up mode:**
```
RAMP-UP REPORT (Week {N}) saved: data/stakeholder/reports/ramp-up-2026-W14-001.md

This Week:
- Met {N} people across {N} teams
- {2-3 key learnings}
- Top emerging theme: {theme}

---

DASHBOARD — 2026-03-27

{full dashboard output from /pm-dash}
```

## Rules

- No questions — auto-detect the week period from today's date
- Run both subagents in parallel for speed
- Status report is saved to file; dashboard is displayed inline only (unless user asks to save)
- Always read and update `data/meta/counters.json` for the status report
- In ramp-up mode, if no interviews or meetings exist yet, note that and suggest using `/discover` and `/status meeting` to start capturing
