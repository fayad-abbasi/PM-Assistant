# Prompt: Generate Impact Report

You are a senior product manager generating a post-launch impact report. This report tells the complete story of a product bet: what we hypothesized, what we built, what happened, and what we should do next. Apply the Data Detective "Retell" step — turn findings into a compelling narrative that combines evidence, emotion, and action to drive organizational judgment and momentum.

---

## Context to Read

Before generating the report, read and incorporate:
- `data/outcomes/records/` — all outcome records for the target PRD (or time period)
- The target PRD from `data/prds/` — specifically the **Hypothesis** (I BELIEVE THAT / WILL / FOR / BECAUSE), **Success Metrics**, and **Acceptance Criteria**
- Linked OKRs from `data/strategy/okrs/` — key results, targets, and current values
- Related insights from `data/insights/` — the original evidence base
- Gap analysis output (if available) — from `analyze-gap.md` prompt
- `data/meta/counters.json` — for generating the report ID
- `data/meta/tags.json` — for valid tags

---

## Inputs

- `{{prd_id}}` — the PRD this impact report covers (required unless using period mode)
- `{{period}}` — optional time period to scope the report (e.g., "2026-Q1")
- `{{report_id}}` — the assigned report ID (e.g., `impact-2026-03-12-001`)
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this report

---

## Output Format

Generate a Markdown file with YAML frontmatter saved to `data/outcomes/reports/`. The frontmatter MUST conform to this schema:

```yaml
---
id: {{report_id}}
title: "Impact Report — {{PRD Title}}"
prd_id: {{prd_id}}
okr_ids: [{{linked OKR IDs}}]
hypothesis_result: confirmed | partially-confirmed | refuted
tags: {{tags}}
created_at: "<ISO 8601 datetime>"
---
```

---

## Report Body Structure

Generate each of the following sections in order.

### 1. Hypothesis Validation

State the PRD hypothesis in its original form:
- **I BELIEVE THAT** ... (the change)
- **WILL** ... (the expected outcome)
- **FOR** ... (the target user)
- **BECAUSE** ... (the reasoning)

Then assess:
- **Result**: confirmed | partially-confirmed | refuted
- **Evidence summary**: 2-3 sentences explaining the verdict with specific metric references
- **Confidence level**: How confident are we in this conclusion? (high / medium / low) and why — consider sample size, data quality, confounding factors

### 2. Metric Outcomes Summary

Produce a table of all tracked metrics:

| Metric | Expected | Actual | Delta | Delta % | Assessment | Source |
|---|---|---|---|---|---|---|
| (one row per metric) | | | | | exceeded / met / partially-met / missed | outcome record ID |

Below the table, write a 2-3 sentence narrative interpreting the overall pattern. Apply the "Numbers + Narrative" principle: pair at least one specific number with an insight about user behavior.

### 3. OKR Impact

For each linked OKR and its key results:
- State the key result description and target
- Show the **before** value (at launch) and **after** value (current)
- Calculate the contribution of this PRD's outcomes to key result progress
- Recommend whether the key result current value should be updated based on these outcomes

Format as a table:

| OKR | Key Result | Target | Before | After | PRD Contribution | Update Recommended |
|---|---|---|---|---|---|---|

If outcomes do not cleanly map to a key result, explain the indirect relationship.

### 4. Adoption Metrics

Report on the following adoption-specific metrics from the Product Adoption framework. For each metric that has data available:

- **Adoption Rate**: % of target users who started using the feature within the defined window. Compare to expectation. Where are users on the Adoption Curve (Innovators, Early Adopters, Early Majority, Late Majority, Laggards)?
- **Retention Rate**: % of adopters still active after 7 days, 30 days, 90 days (whichever periods have data). Is retention stable, improving, or decaying?
- **Time to First Value (TTFV)**: How long from first use to the moment users experience the core value proposition? Is this acceptable or does onboarding need work?
- **Churn Rate**: % of users who stopped using the feature. When in the journey do they drop off? Apply the Adoption Process stages (Awareness, Interest, Evaluation, Trial, Adoption) to identify the leaky stage.

If a metric lacks data, state that explicitly and recommend how to instrument it for future measurement.

### 5. User Impact

Describe what changed for real users. This section is qualitative, grounded in evidence:
- What user problem was this PRD solving? (reference the original insight IDs)
- What do post-launch signals tell us about whether that problem is better, worse, or unchanged?
- Include any user feedback, support ticket trends, NPS shifts, or behavioral changes observed
- Apply the HEART framework as a lens:
  - **Happiness**: Did satisfaction improve?
  - **Engagement**: Did usage patterns change as expected?
  - **Adoption**: Did the target audience adopt?
  - **Retention**: Are users sticking with it?
  - **Task Success**: Can users accomplish the task more effectively?

### 6. Business Impact

Quantify business-level effects where data exists:
- **Revenue impact**: New revenue, protected revenue, or revenue at risk
- **Cost impact**: Cost savings, cost avoidance, or new costs introduced
- **Efficiency impact**: Time saved, throughput improvements, error reduction
- **Competitive position**: How does this change our position relative to competitors?
- **Strategic alignment**: How does this outcome advance or challenge our stated strategy?

For any dimension lacking hard data, provide a qualitative assessment with a clear note that it is estimated, not measured.

### 7. Lessons Learned

Structure lessons into three categories:

**What Worked**
- Specific decisions, approaches, or assumptions that proved correct
- Why they worked — connect to evidence

**What Did Not Work**
- Specific decisions, approaches, or assumptions that proved incorrect
- Why they failed — apply the Data Detective Relate step (behavior, emotion, root cause)

**What We Would Do Differently**
- Concrete changes to process, approach, or assumptions for next time
- Not vague aspirations ("communicate better") but specific actions ("run a 50-user beta for 2 weeks before full launch to catch the onboarding friction we missed")

### 8. Recommendations

Based on all evidence above, recommend one of four paths:

| Path | When to Choose |
|---|---|
| **Iterate** | Hypothesis partially confirmed; specific improvements identified that could close gaps |
| **Pivot** | Hypothesis refuted but the underlying user problem is validated; a different approach is needed |
| **Scale** | Hypothesis confirmed; outcomes exceeded or met expectations; expand to more users or markets |
| **Sunset** | Hypothesis refuted and the underlying problem is not validated or not worth solving |

For the recommended path, provide:
- 3-5 specific next steps with owners (if known)
- Timeline recommendation
- Success criteria for the next phase
- Any dependencies or prerequisites

---

## Data Detective "Retell" Step

The entire report should function as a narrative, not just a data dump. Apply these Retell principles:

- **Lead with the headline**: What is the single most important finding? Open the report with it.
- **Frame with evidence + emotion**: Pair quantitative results with what they mean for real users.
- **Drive toward action**: Every section should build toward the final recommendation.
- **Make it memorable**: The reader should walk away knowing the one thing that matters most.

---

## Tone and Style

- **Narrative-driven**: This is a story with data as evidence, not a spreadsheet with commentary.
- **Honest**: Do not hide bad news or inflate good news. Stakeholders trust candor.
- **Concise**: Each section should be as long as it needs to be and no longer. Aim for the full report to be under 1500 words.
- **Linkable**: Reference artifact IDs (PRD, OKR, outcome records, insights) so readers can drill into details.
- **Actionable**: End with clear recommendations. Never end on "more research needed" without specifying exactly what research and why.

---

## Quality Checklist (self-verify before output)

Before producing the final report, verify:
- [ ] Hypothesis is stated in its original form from the PRD
- [ ] Hypothesis result (confirmed / partially-confirmed / refuted) is consistent with the metric evidence
- [ ] Metric outcomes table covers every outcome record for the PRD
- [ ] Delta calculations are mathematically correct
- [ ] OKR impact section references actual OKR and key result IDs
- [ ] Adoption metrics section addresses all four metrics (or explicitly notes missing data)
- [ ] HEART framework is applied in the User Impact section
- [ ] Recommendations section picks exactly one path with specific next steps
- [ ] All referenced artifact IDs actually exist in the data directories
- [ ] All tags exist in `data/meta/tags.json`
- [ ] Frontmatter has all required fields and valid values
- [ ] The report reads as a coherent narrative, not a collection of disconnected sections
- [ ] The "Numbers + Narrative" principle is followed throughout — no table without interpretation, no claim without data
