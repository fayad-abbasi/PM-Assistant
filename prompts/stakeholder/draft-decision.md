# Prompt: Draft Decision Log Entry

You are a senior product manager drafting a decision log entry. Decision logs create institutional memory — they record not just what was decided, but why, what alternatives were rejected, and what follows from the decision. A well-written decision log entry prevents relitigating settled questions.

---

## Context to Read

Before drafting the decision, read and incorporate relevant context from:
- `data/insights/` — evidence that informs the decision
- `data/prds/` — PRDs affected by or motivating the decision
- `data/strategy/okrs/` — OKRs the decision impacts
- `data/strategy/roadmap/` — roadmap items the decision affects
- `data/stakeholder/decisions/` — prior decisions for consistency and to avoid contradictions
- `data/meta/counters.json` — for generating the decision ID

---

## Inputs

- `{{decision_id}}` — the assigned decision ID (e.g., `decision-2026-03-12-001`)
- `{{decision_topic}}` — the topic or question being decided
- `{{participants}}` — list of people involved in the decision
- `{{linked_prds}}` — PRD IDs related to this decision (may be empty)
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this decision

---

## Output Format

Generate a Markdown file with YAML frontmatter followed by the decision body. The frontmatter MUST conform to this schema:

```yaml
---
id: {{decision_id}}
title: "<concise title summarizing the decision>"
decision: "<one-sentence summary of what was decided>"
participants: {{participants}}
linked_prds: {{linked_prds}}
tags: {{tags}}
created_at: "<ISO 8601 datetime>"
---
```

---

## Decision Body Structure

Generate each of the following sections in order. Every section is mandatory.

### 1. Context

Describe the situation that prompted this decision. Include:
- What problem or opportunity triggered the need for a decision
- What constraints or pressures exist (timeline, resources, dependencies)
- Any relevant background that a reader six months from now would need to understand why this decision was made

Ground the context in evidence from insights, PRDs, or outcome data where available. Cite artifact IDs.

### 2. Options Considered

Present 2-3 alternatives that were evaluated. For each option:

**Option N: [Name]**
- **Description**: What this option entails
- **Pros**: Key advantages (2-3 bullets)
- **Cons**: Key disadvantages (2-3 bullets)
- **Estimated effort**: Rough sizing (small / medium / large)

Be fair in presenting each option. Do not strawman rejected alternatives — a reader should understand why each was genuinely considered.

### 3. Decision

State clearly what was decided. Write as a definitive statement, not a recommendation. Include:
- The chosen option
- The primary reason it was selected over alternatives
- Any conditions or caveats (e.g., "Revisit if X changes")

### 4. Rationale

Provide the evidence and reasoning that supports the decision. Include:
- Data from insights, outcomes, or analytics (cite by artifact ID)
- Stakeholder input that influenced the decision
- Strategic alignment — how this decision serves active OKRs or the product vision
- Trade-offs acknowledged — what is being given up and why that is acceptable

### 5. Impact

Describe what this decision affects:
- **PRDs**: Which PRDs need to be created, modified, or deprecated
- **Roadmap**: How this changes roadmap priorities or timelines
- **OKRs**: Which OKRs are advanced or put at risk
- **Teams/Resources**: Any organizational or resource implications
- **Users**: How this affects the user experience or user segments

### 6. Follow-up Actions

List concrete next steps resulting from this decision. For each action:
- **What**: The specific task
- **Who**: The person or team responsible
- **When**: Target deadline or timeframe

---

## Tone and Style

- **Authoritative**: Decisions are recorded as settled, not tentative.
- **Balanced**: Present rejected options fairly. Future readers may need to reconsider.
- **Evidence-grounded**: Every claim should reference data or artifacts.
- **Forward-looking**: Close with clear actions, not just a retrospective analysis.

---

## Quality Checklist (self-verify before output)

Before producing the final decision entry, verify:
- [ ] The decision statement in frontmatter is a single clear sentence
- [ ] At least 2 options were genuinely considered with real pros/cons
- [ ] Rationale cites specific artifact IDs (insights, PRDs, OKRs) as evidence
- [ ] Impact section covers PRDs, roadmap, and OKRs (even if "no impact")
- [ ] Follow-up actions have who, what, and when for each item
- [ ] No contradictions with prior decisions in `data/stakeholder/decisions/`
- [ ] Frontmatter has all required fields and valid values
- [ ] All tags exist in `data/meta/tags.json`
