# Prompt: Extract Learnings from Retrospective

You are a senior product strategist distilling retrospective findings into concrete strategy updates. This is the critical feedback loop: learnings from retrospectives flow back into `/strategy` updates, OKR adjustments, roadmap changes, and new discovery work. Every output must be actionable and traceable to evidence in the retrospective.

---

## Context to Read

Before extracting learnings, read:
- The retrospective document specified by `{{retro_id}}` from `data/retros/`
- All artifacts referenced in the retrospective's frontmatter:
  - Linked PRDs from `data/prds/`
  - Linked outcomes from `data/outcomes/records/`
  - Linked OKRs from `data/strategy/okrs/`
- Current roadmap from `data/strategy/roadmap/` — to understand what is planned and what may need changing
- Current vision from `data/strategy/vision/` — to assess whether strategic direction needs adjustment
- `data/meta/tags.json` — for valid tags on any new artifacts proposed

---

## Inputs

- `{{retro_id}}` — the retrospective to extract learnings from (e.g., `retro-2026-03-12-001`)
- `{{retro_path}}` — file path to the retrospective document

---

## Output Format

Generate a structured Markdown document. This document is a working artifact for the product team — it does not need YAML frontmatter, but it must be clear, scannable, and actionable.

---

## Output Structure

### 1. Summary Table

Start with a summary table of all extracted learnings for quick scanning:

| # | Category | Finding | Priority | Affected Artifacts |
|---|----------|---------|----------|--------------------|
| 1 | Strategy Update | ... | high | vision-... |
| 2 | OKR Adjustment | ... | high | okr-... |
| 3 | Roadmap Change | ... | medium | roadmap-..., prd-... |
| ... | ... | ... | ... | ... |

Priority values: `high` (act this cycle), `medium` (act next cycle), `low` (backlog for future consideration).

### 2. Strategy Updates

Changes to vision, positioning, or market approach based on retrospective findings.

For each strategy update:

- **Finding**: What we learned that affects strategy (one sentence)
- **Evidence**: Which retro section and artifact IDs support this finding
- **Proposed Action**: Specific change to make — be precise (e.g., "Update vision document to deprioritize segment X in favor of segment Y" rather than "Revisit our strategy")
- **Priority**: high / medium / low
- **Affected Artifacts**: Which vision documents, strategy files need updating

If no strategy updates are warranted, state that explicitly and explain why the current strategy remains valid given the retrospective findings.

### 3. OKR Adjustments

OKRs to modify targets, carry forward, or abandon. Pull directly from the OKR Reflection section of the retrospective.

For each OKR adjustment:

- **Finding**: What the retrospective revealed about this OKR
- **Evidence**: Key result actuals vs targets, outcome record IDs
- **Current State**: The OKR's current objective, key results, and status
- **Proposed Action**: One of:
  - **Carry forward as-is**: Objective and key results remain unchanged for the next cycle
  - **Modify key results**: Specify which key results change and the new targets (e.g., "KR2 target from 30% to 20% based on outcome-2026-03-01-002 showing 18% is realistic ceiling")
  - **Modify objective**: Rewrite the objective statement (provide old and new)
  - **Abandon**: Remove this OKR from the active set (explain what replaces it, if anything)
- **Priority**: high / medium / low
- **Affected Artifacts**: OKR IDs, and any PRDs or roadmap items whose linkage changes

### 4. Roadmap Changes

Items to reprioritize, defer, add, or remove from the roadmap. Every change must be justified by a specific retrospective finding.

For each roadmap change:

- **Finding**: What the retrospective revealed that affects this roadmap item
- **Evidence**: Which retro section, outcome IDs, or hypothesis validation results support this
- **Proposed Action**: One of:
  - **Reprioritize**: Change priority level (state from and to, e.g., "medium to high")
  - **Defer**: Move to a later quarter (state which quarter and why)
  - **Add**: Propose a new roadmap item (provide title, description, quarter, priority, linked PRDs and OKRs)
  - **Remove**: Remove from roadmap entirely (explain why it is no longer relevant)
  - **Accelerate**: Move to an earlier quarter (state which quarter and why)
- **Priority**: high / medium / low
- **Affected Artifacts**: Roadmap item IDs, linked PRD IDs, linked OKR IDs

### 5. Process Improvements

Changes to how the team does discovery, build, test, or measure. These are operational improvements, not product changes.

For each process improvement:

- **Finding**: What friction, inefficiency, or gap the retrospective surfaced
- **Evidence**: Which retro section describes this (e.g., "I Wish" quadrant item 3, or blocked test cases)
- **Proposed Action**: Specific change to the process (e.g., "Add a pre-launch UAT gate requiring 90% test case pass rate before approval" rather than "Improve testing")
- **Priority**: high / medium / low
- **Affected Artifacts**: Any command templates, prompt files, or workflow steps that need updating

### 6. New Hypotheses

Hypotheses generated from retrospective learnings. These feed back into the discovery cycle and may become future PRDs.

For each new hypothesis, use the format from the Hypothesis and Experimentation framework:

> **I BELIEVE THAT** [feature / product / solution]
> **WILL** [direction of change / thing that will change]
> **FOR** [target user]
> **BECAUSE** [reason for change, grounded in retrospective evidence]

For each hypothesis also provide:

- **Origin**: Which retro finding or "Ideas" quadrant item generated this hypothesis
- **Type**: Working / Descriptive / Relational / Formalized (from the hypothesis classification system)
- **Validation Method**: How to test this — A/B test, user interviews, usage analytics, concierge test, etc.
- **Success Criteria**: What metric, at what threshold, would confirm or refute this hypothesis
- **Priority**: high / medium / low
- **Linked Artifacts**: Retro ID, and any existing PRDs or insights this relates to

### 7. Research Gaps

Areas where the team needs more data or user research before making decisions. These feed into `/discover` as future research priorities.

For each research gap:

- **Finding**: What we do not know and why it matters
- **Evidence**: Which retro "Questions" quadrant item or hypothesis validation surfaced this gap
- **Proposed Research**: What type of research would close this gap (interviews, analytics mining, survey, A/B test, cohort analysis, usability testing)
- **Decision Blocked**: Which decisions or artifacts are waiting on this research
- **Priority**: high / medium / low

---

## Feedback Loop Connections

At the end of the document, include a section mapping learnings to the slash commands that should act on them:

| Learning # | Action | Command | Target Artifact |
|------------|--------|---------|-----------------|
| 1 | Update vision to deprioritize segment X | `/strategy` | vision-... |
| 2 | Modify OKR key result targets | `/strategy` | okr-... |
| 3 | Add new roadmap item for Q2 | `/strategy` | (new) |
| 4 | Create new PRD from hypothesis | `/prd` | (new) |
| 5 | Schedule user interviews on topic Y | `/discover` | (new) |
| ... | ... | ... | ... |

This table makes it explicit that retrospective learnings are not just documented — they are routed to specific workflows for execution.

---

## Tone and Style

- **Actionable**: Every learning must end with a concrete proposed action. Observations without recommendations have no place here.
- **Traceable**: Every proposed change must cite the retrospective finding and underlying artifact IDs that justify it. No changes without evidence.
- **Decisive**: Recommend a specific action, not a menu of options. If the evidence is ambiguous, say so and route it to a research gap instead of proposing a half-confident change.
- **Prioritized**: Not all learnings are equal. Use priority ratings honestly — marking everything as "high" defeats the purpose.

---

## Quality Checklist (self-verify before output)

Before producing the final document, verify:
- [ ] Summary table includes every learning detailed in sections 2-7
- [ ] Every learning has all four required fields: Finding, Evidence, Proposed Action, Priority
- [ ] Every proposed action cites specific artifact IDs from the retrospective
- [ ] OKR Adjustments cover every OKR mentioned in the retrospective's OKR Reflection section
- [ ] New Hypotheses use the I BELIEVE THAT / WILL / FOR / BECAUSE format
- [ ] Research Gaps identify specific blocked decisions, not vague "we should learn more" statements
- [ ] Feedback Loop Connections table maps every learning to a specific command and target
- [ ] Priority distribution is realistic — not everything is "high"
- [ ] No proposed action contradicts another proposed action in the same document
- [ ] All referenced artifact IDs match IDs found in the retrospective document
