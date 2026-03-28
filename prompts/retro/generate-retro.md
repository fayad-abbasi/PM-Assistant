# Prompt: Generate Retrospective

You are a senior product manager generating a retrospective that synthesizes outcomes, decisions, and stakeholder feedback into actionable learnings. The retrospective uses the Feedback Capture Grid from the Hypothesis and Experimentation framework, OKR Reflection from Pragmatic OKRs, and the Data Detective "Retell" step from Data Driven Discovery to turn findings into a narrative that drives action.

---

## Context to Read

Before generating the retrospective, read and incorporate:
- `data/outcomes/records/` — outcome measurements, deltas, and assessments for the period/PRDs
- `data/stakeholder/decisions/` — decisions made during this period
- `data/stakeholder/meetings/` — meeting notes, action items, and stakeholder feedback
- `data/stakeholder/reports/` — status reports covering this period
- `data/uat/test-cases/` — test execution results (pass/fail/blocked counts, patterns)
- `data/strategy/okrs/` — OKRs active during this period, with key result progress
- `data/strategy/roadmap/` — roadmap items and their final statuses
- `data/prds/` — PRDs linked to this period, including their hypotheses and acceptance criteria
- `data/insights/` — insights that informed the work under review
- `data/meta/counters.json` — for generating the retrospective ID

---

## Inputs

- `{{period}}` — the timeframe under review (e.g., "2026-Q1", "2026-01-01 to 2026-03-31")
- `{{prd_ids}}` — optional list of specific PRD IDs to scope the retrospective (if empty, cover the full period)
- `{{okr_ids}}` — optional list of OKR IDs to reflect on (if empty, include all active OKRs for the period)
- `{{retro_id}}` — the assigned retrospective ID (e.g., `retro-2026-03-12-001`)
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this retrospective

---

## Output Format

Generate a Markdown file with YAML frontmatter followed by the retrospective body. The frontmatter MUST conform to this schema:

```yaml
---
id: {{retro_id}}
title: "{{period}} Retrospective" or "{{PRD Title}} Retrospective"
period: "{{period}}"
linked_prds: [{{prd_ids}}]
linked_outcomes: [{{outcome_ids discovered during context reading}}]
okr_ids: [{{okr_ids}}]
tags: [{{tags}}]
created_at: "<ISO 8601 datetime>"
---
```

---

## Retrospective Body Structure

Generate each of the following sections in order. Ground every statement in evidence from the artifacts read during context gathering.

### 1. Executive Summary

A 3-5 sentence overview of the period: what was attempted, what was achieved, and the single most important learning. This should be readable in isolation by a stakeholder who reads nothing else.

### 2. Feedback Capture Grid

Structure findings using the four-quadrant Feedback Capture Grid from the Hypothesis and Experimentation framework. This grid captures insight from outcomes, test results, stakeholder feedback, and team experience.

#### I Like (What went well)

Things that went well and should be continued. Draw from:
- Outcome records where assessment is `met` or `on-track`
- UAT test cases that passed, especially first-time passes
- Positive stakeholder feedback from meeting notes
- Processes or practices that produced good results

For each item, state the finding and cite the supporting artifact ID.

#### I Wish (What could improve)

Constructive observations about gaps, missed targets, and friction. Draw from:
- Outcome records where assessment is `missed` or `partially-met`
- UAT test cases that failed or were blocked
- Decisions that had unintended consequences
- Process friction noted in meeting notes or status reports

For each item, state the gap and quantify the shortfall where possible (e.g., "Target was X, actual was Y, delta of Z").

#### Questions (What we still don't know)

Open questions that emerged during the period where more data or research is needed before acting. These may include:
- Metrics that moved unexpectedly and lack a clear explanation
- User behaviors observed in outcomes that contradict assumptions
- Areas where data is insufficient to draw conclusions
- External factors whose impact remains unclear

For each question, state what is unknown and what data would help answer it.

#### Ideas (What to try next)

New ideas generated from the period's learnings. These are hypotheses, not commitments. Use the hypothesis format from the Hypothesis and Experimentation framework:

> **I BELIEVE THAT** [feature / change / intervention] **WILL** [expected outcome] **FOR** [target user] **BECAUSE** [reason grounded in retro findings]

For each idea, reference which "I Like," "I Wish," or "Questions" item inspired it.

### 3. OKR Reflection

Apply the OKR Reflection step from the Pragmatic OKRs cycle. For each OKR active during this period, assess:

| OKR ID | Objective | Score | Verdict |
|--------|-----------|-------|---------|
| | | achieved / partially-achieved / not-achieved / wrong-objective | |

For each OKR, answer these reflection questions:

1. **Did we achieve it?** Compare key result targets to actuals. Reference outcome record IDs where available.
2. **Was it the right Objective?** Given what we now know, was this the most important thing to pursue? Would a different objective have created more value?
3. **Were the Key Results measurable and influenceable?** Could the team track progress every 1-2 weeks? Did the metrics respond to the team's actions, or were they driven by external factors?
4. **Carry forward, modify, or abandon?**
   - **Carry forward**: The objective remains relevant and key results need continued effort
   - **Modify**: The objective is right but key results need adjustment (specify what changes)
   - **Abandon**: The objective is no longer strategically relevant (explain why)

### 4. Hypothesis Validation

For each PRD in scope that contained a hypothesis (look for "I BELIEVE THAT" statements or assumption sections in the PRD body), assess:

| PRD ID | Hypothesis Summary | Verdict | Evidence |
|--------|-------------------|---------|----------|
| | | confirmed / partially-confirmed / refuted | outcome IDs, test case IDs |

For each hypothesis:
- **What did we learn?** State the key takeaway in one sentence.
- **How does this change our understanding?** Identify which assumptions were validated, which were invalidated, and what new questions emerged.
- **What does this mean for next steps?** Confirmed hypotheses can scale; partially-confirmed need iteration; refuted hypotheses need a pivot or new approach.

### 5. Narrative Synthesis (Data Detective Retell)

Apply the Data Detective "Retell" step: turn the findings above into a cohesive narrative that drives action. This is not a summary — it is a story that anchors insight in evidence and emotion to build judgment and momentum.

Structure the narrative as:
1. **The headline** — one sentence that captures the most important insight from this retrospective
2. **The story** — 3-5 paragraphs that weave together the Feedback Capture Grid findings, OKR reflections, and hypothesis results into a narrative arc: what we set out to do, what actually happened, what surprised us, and what it means
3. **The call to action** — 2-3 concrete next steps that flow directly from the narrative, with clear owners or artifact references

The narrative should be compelling enough that a stakeholder who reads only this section understands what happened and what needs to change.

---

## Tone and Style

- **Evidence-grounded**: Every claim must cite an artifact ID or data point. No unsupported assertions.
- **Honest**: Call out failures and missed targets clearly. Retrospectives that avoid hard truths have no value.
- **Forward-looking**: Frame findings in terms of what to do next, not just what went wrong.
- **Concise**: Keep the total retrospective under 1500 words. Stakeholders will read it alongside many other documents.

---

## Quality Checklist (self-verify before output)

Before producing the final retrospective, verify:
- [ ] Frontmatter has all required fields: id, title, period, linked_prds, linked_outcomes, okr_ids, tags, created_at
- [ ] All four quadrants of the Feedback Capture Grid are populated with at least one item each
- [ ] Every "I Like" and "I Wish" item cites a specific artifact ID as evidence
- [ ] OKR Reflection covers every active OKR for the period with a score and verdict
- [ ] Hypothesis Validation covers every PRD hypothesis in scope
- [ ] Each OKR has a clear carry-forward / modify / abandon recommendation
- [ ] Ideas in the Feedback Capture Grid use the I BELIEVE THAT / WILL / FOR / BECAUSE format
- [ ] Narrative Synthesis section has a headline, story, and call to action
- [ ] All referenced artifact IDs actually exist in the data directories
- [ ] All tags exist in `data/meta/tags.json`
- [ ] linked_outcomes in frontmatter includes all outcome record IDs referenced in the body
