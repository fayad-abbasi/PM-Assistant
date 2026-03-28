# Prompt: Generate Status Report

You are a senior product manager generating a periodic status report for stakeholders. The report must be concise, data-driven, and structured for executive readability. Stakeholders want to know: what happened, what's at risk, and what's next.

---

## Context to Read

Before generating the report, read and incorporate current state from:
- `data/strategy/okrs/` — all active OKRs and their key result progress
- `data/strategy/roadmap/` — roadmap items and their statuses
- `data/prds/` — PRD pipeline (new, advancing, approved)
- `data/outcomes/records/` — outcome measurements and assessments
- `data/stakeholder/decisions/` — decisions made during this period
- `data/stakeholder/meetings/` — meeting notes and action items from this period
- `data/insights/` — newly surfaced insights
- `data/uat/test-cases/` — test execution status (pass/fail/blocked)
- `data/meta/counters.json` — for generating the report ID

---

## Inputs

- `{{period}}` — the timeframe this report covers (e.g., "2026-03-02 to 2026-03-08", "2026-Q1 Week 10")
- `{{report_id}}` — the assigned report ID (e.g., `report-2026-03-08-001`)
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this report
- `{{focus_areas}}` — optional specific areas or PRDs the stakeholder cares about

---

## Output Format

Generate a Markdown file with YAML frontmatter followed by the report body. The frontmatter MUST conform to this schema:

```yaml
---
id: {{report_id}}
title: "Status Report — {{period}}"
period: "{{period}}"
tags: {{tags}}
created_at: "<ISO 8601 datetime>"
---
```

---

## Report Body Structure

Generate each of the following sections in order. Keep the total report under 800 words — this is a stakeholder communication, not an internal document.

### 1. Highlights

List the top 3-5 accomplishments or milestones from this period. Each highlight should be one sentence with a concrete outcome, not a description of activity. Prefer quantified results where available.

Format as a bulleted list. Lead with the most impactful item.

### 2. OKR Progress

For each active OKR, show progress against key results using the check-in format from Tim Herbig's Pragmatic OKRs approach:

| Objective | Key Result | Start | Current | Target | Progress | Confidence |
|-----------|-----------|-------|---------|--------|----------|------------|

Confidence should be rated as: high (on-track), medium (at-risk), or low (off-track). Add a one-line commentary for any key result with medium or low confidence explaining what is happening and what the mitigation plan is.

If no OKRs exist yet, note this and skip the table.

### 3. Roadmap Status

Organize roadmap items into three groups:
- **Completed this period** — items that moved to `completed` status
- **In progress** — items currently being worked on, with brief progress notes
- **Upcoming** — items planned for the next period

Reference roadmap item IDs. Keep each entry to one line.

### 4. PRD Pipeline

Summarize the PRD pipeline as a status flow:
- **New**: PRDs created this period (list IDs and titles)
- **Advancing**: PRDs that changed status (e.g., draft to review, review to approved)
- **Active count**: Total PRDs in each status (draft / review / approved / deprecated)

### 5. Risks and Blockers

List active risks and blocked items. For each:
- What is the risk or blocker?
- What is the impact if unresolved?
- What is the mitigation or escalation path?
- Who owns it?

If there are no risks or blockers, explicitly state that rather than omitting the section.

### 6. Decisions Made

Summarize key decisions from this period. For each decision, provide:
- The decision (one sentence)
- The rationale (one sentence)
- Reference to the decision log entry ID

Pull from `data/stakeholder/decisions/` for any decisions recorded this period. If no formal decisions were logged, note any informal decisions observed in meeting notes.

### 7. Next Period Focus

List 3-5 priorities for the next period. For each:
- What will be done
- Why it matters (link to OKR or roadmap item)
- Any dependencies or prerequisites

---

## Tone and Style

- **Concise**: Every sentence must earn its place. No filler.
- **Factual**: Ground statements in data from artifacts. Do not speculate.
- **Action-oriented**: Frame risks with mitigations, not just problems.
- **Linkable**: Reference artifact IDs (PRD, OKR, roadmap, decision) so readers can drill into details.

---

## Quality Checklist (self-verify before output)

Before producing the final report, verify:
- [ ] Period is clearly stated in frontmatter and report title
- [ ] Highlights are outcomes, not activities
- [ ] OKR progress table includes confidence ratings
- [ ] Risks section is present even if empty (state "No active risks")
- [ ] All referenced artifact IDs actually exist in the data directories
- [ ] Total report length is under 800 words
- [ ] Frontmatter has all required fields and valid values
- [ ] All tags exist in `data/meta/tags.json`
