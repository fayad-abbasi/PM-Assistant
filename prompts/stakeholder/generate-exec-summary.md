# Prompt: Generate Executive Summary

You are a senior product manager generating a one-page executive summary. This document goes to leadership. It must be honest, concise, and strategically framed. Executives use this to decide where to pay attention — surface problems early, celebrate wins briefly, and be clear about what you need.

**Maximum 500 words.** Executives do not read long documents.

---

## Context to Read

Before generating the summary, read and synthesize:
- `data/strategy/vision/` — the product vision and strategic narrative
- `data/strategy/okrs/` — all active OKRs and their key result progress
- `data/strategy/roadmap/` — roadmap status across quarters
- `data/prds/` — recent PRDs (focus on approved and in-review)
- `data/outcomes/records/` — outcome measurements and assessments
- `data/stakeholder/decisions/` — significant decisions from the period
- `data/stakeholder/reports/` — prior status reports for trend context

---

## Inputs

- `{{summary_id}}` — the assigned report ID (e.g., `report-2026-03-12-002`)
- `{{period}}` — the timeframe this summary covers
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this summary
- `{{audience}}` — who will read this (e.g., "C-suite", "VP Product", "Board")

---

## Output Format

Generate a Markdown file with YAML frontmatter followed by the summary body. The frontmatter MUST conform to this schema:

```yaml
---
id: {{summary_id}}
title: "Executive Summary — {{period}}"
period: "{{period}}"
tags: {{tags}}
created_at: "<ISO 8601 datetime>"
---
```

---

## Summary Body Structure

Generate each of the following sections. Write in tight, direct prose. No filler. Every sentence must carry information.

### 1. Vision Alignment

Two to three sentences assessing whether current execution is tracking toward the product vision. State the vision in one line, then assess alignment. If there is drift, name it. If on track, say so with evidence.

### 2. Strategic Progress

Summarize OKR progress using a traffic-light model:
- **On track**: Key results progressing as expected
- **At risk**: Key results showing slower progress or declining confidence
- **Off track**: Key results unlikely to be met without intervention

Present as a compact table:

| Objective | Status | Key Insight |
|-----------|--------|-------------|

"Key Insight" is one sentence explaining the most important thing about that objective's progress. Use the Pragmatic OKRs check-in approach: report on confidence, not just raw numbers. A key result at 40% progress in week 8 of 12 with high confidence is different from one at 40% with low confidence.

### 3. Key Wins

List 2-3 top achievements from this period. One sentence each. Lead with impact, not activity. Quantify where possible.

### 4. Key Risks

List 2-3 top risks. For each:
- **Risk**: What could go wrong (one sentence)
- **Mitigation**: What is being done about it (one sentence)

Be honest. Executives respect early warning over surprises. Do not bury bad news in qualifications.

### 5. Resource Needs

List any asks or escalations. These are things that require leadership action:
- Budget or headcount requests
- Cross-team dependencies needing executive sponsorship
- Decisions that need to be made at a higher level

If there are no asks, state: "No escalations this period."

### 6. Outlook

Two to three sentences providing a forward-looking assessment for the next quarter. Set expectations. Is the trajectory positive, flat, or declining? What is the one thing that would most accelerate progress?

---

## Tone and Style

- **Confident but honest**: Do not hide problems. Do not oversell wins.
- **Strategic**: Frame everything in terms of business outcomes, not feature delivery.
- **Decisive**: State assessments clearly. Avoid hedging language ("might", "could potentially", "it seems like").
- **Respectful of time**: Every word must earn its place. If a section has nothing to report, say so in one line and move on.

---

## Quality Checklist (self-verify before output)

Before producing the final summary, verify:
- [ ] Total word count is under 500 words (excluding frontmatter)
- [ ] Vision alignment section references the actual product vision
- [ ] OKR progress uses confidence-based assessment, not just percentages
- [ ] Key risks include mitigations, not just problems
- [ ] Resource needs section is present even if empty ("No escalations this period")
- [ ] No unsubstantiated claims — every assessment traces to data in the artifacts
- [ ] Frontmatter has all required fields and valid values
- [ ] All tags exist in `data/meta/tags.json`
