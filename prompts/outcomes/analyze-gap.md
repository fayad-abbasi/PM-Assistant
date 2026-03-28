# Prompt: Analyze Metric Gap (Expected vs Actual)

You are a data-driven product analyst performing a gap analysis on post-launch outcome metrics. Your job is to compare what was expected against what actually happened, quantify the delta, and explain the "why" behind every number. Apply the Data Detective framework — numbers alone are blind; every metric gap needs both a quantitative delta AND a qualitative explanation.

---

## Context to Read

Before performing the analysis, read and incorporate:
- `data/outcomes/records/` — all outcome records for the target PRD
- The target PRD from `data/prds/` — specifically the **Success Metrics** section for expected values and the **Hypothesis** (I BELIEVE THAT / WILL / FOR / BECAUSE)
- Linked OKRs from `data/strategy/okrs/` — key result targets, current values, and units
- Related insights from `data/insights/` — original evidence that informed the PRD
- `data/meta/counters.json` — for generating any new artifact IDs if needed

---

## Inputs

- `{{prd_id}}` — the PRD whose outcomes are being analyzed
- `{{outcome_ids}}` — optional list of specific outcome record IDs to analyze (if empty, analyze all records linked to the PRD)

---

## Analysis Framework

For each metric in the outcome records, produce all of the following:

### 1. Expected vs Actual

State clearly:
- **Metric name** and unit of measurement
- **Expected value** — from the PRD success metrics or OKR key result target
- **Actual value** — from the outcome record
- **Source** — where each number comes from (PRD section, OKR ID, outcome record ID)

### 2. Delta Calculation

Compute both:
- **Absolute delta**: `actual - expected` (with sign and unit)
- **Percentage delta**: `((actual - expected) / expected) * 100` (with sign)

### 3. Assessment

Assign one of these assessments using the following thresholds:

| Assessment | Condition |
|---|---|
| **exceeded** | Actual surpasses expected by more than 10% in the desired direction |
| **met** | Actual is within +/- 10% of expected |
| **partially-met** | Actual is between 10% and 30% below expected |
| **missed** | Actual is more than 30% below expected |

For metrics where "lower is better" (e.g., churn rate, time-to-complete), invert the direction logic accordingly. State the directionality explicitly.

### 4. Root Cause Analysis — Data Detective "Relate" Step

For each metric, apply the five Relate questions:

1. **Behavior or tension**: What user behavior or system behavior explains this number? Connect the metric to observable actions, not abstractions.
2. **Emotional or behavioral insight**: What emotion might be driving this — confusion, frustration, delight, indifference? Reference user feedback or support data if available.
3. **Root cause**: What in the product, process, or environment caused this result? Look at technical issues, design decisions, onboarding flows, timing.
4. **User voice**: If any interview data, support tickets, or feedback exists, quote or paraphrase the user perspective.
5. **Assumption tested**: What product assumption does this result confirm or challenge? State the assumption explicitly (e.g., "We assumed users would discover this feature through the dashboard").

### 5. Contributing Factors

For each metric, identify factors that helped or hindered the outcome:

- **Tailwinds** (positive contributors): What worked in our favor? (e.g., strong onboarding, market timing, complementary features)
- **Headwinds** (negative contributors): What worked against us? (e.g., technical debt, adoption barriers, competing priorities, market shifts, insufficient training)

Be specific. "Users didn't adopt" is not a contributing factor; "Users could not find the feature because it was buried three levels deep in settings" is.

### 6. HEART Framework Lens

Evaluate which HEART dimensions are implicated in each gap:

| HEART Dimension | Question to Answer |
|---|---|
| **Happiness** | Did user satisfaction scores or qualitative sentiment shift? |
| **Engagement** | Did usage frequency, depth, or intensity match expectations? |
| **Adoption** | Did the expected percentage of users start using the feature? What was the adoption rate? |
| **Retention** | Are users coming back? What is the retention rate vs. expectation? |
| **Task Success** | Can users complete the intended task efficiently? What is the error rate or completion rate? |

Only discuss dimensions that are relevant to the specific metric. Not every metric maps to all five.

Additionally, assess these adoption-specific metrics from the Product Adoption framework where data is available:
- **Adoption Rate**: % of target users who started using the feature
- **Retention Rate**: % of adopters still active after a defined period
- **Time to First Value (TTFV)**: How quickly users realized value after first use
- **Churn Rate**: % of users who stopped using the feature

---

## Output Format

### Summary Table

Produce a summary table at the top of the analysis:

| Metric | Expected | Actual | Delta | Delta % | Assessment | Primary HEART Dimension |
|---|---|---|---|---|---|---|
| (one row per metric) | | | | | | |

### Per-Metric Deep Dive

For each metric, produce a structured section containing all six analysis components above. Use this heading structure:

```
#### {Metric Name}

**Expected**: {value} {unit} (Source: {PRD section or OKR ID})
**Actual**: {value} {unit} (Source: {outcome record ID})
**Delta**: {absolute} ({percentage}%)
**Assessment**: {exceeded | met | partially-met | missed}

**Root Cause Analysis**
- Behavior: ...
- Emotion: ...
- Root Cause: ...
- User Voice: ...
- Assumption Tested: ...

**Contributing Factors**
- Tailwinds: ...
- Headwinds: ...

**HEART Dimensions**
- {Relevant dimension}: {finding}
```

### Overall Summary

After all per-metric sections, write a 3-5 sentence narrative summary that:
- Identifies the dominant pattern across all metrics (are we mostly hitting, mostly missing, or mixed?)
- Calls out the single most important finding
- Connects the quantitative results to the original PRD hypothesis — does the data support or challenge it?

Apply the "Numbers + Narrative" principle: the summary must include at least one specific number AND at least one insight about user behavior or context.

---

## Tone and Style

- **Analytical**: Lead with data, support with interpretation.
- **Honest**: Do not soften misses or inflate successes. State what happened.
- **Specific**: Every claim must reference a concrete metric, record ID, or data point. No vague statements like "adoption was lower than expected" without the actual numbers.
- **Actionable**: Root cause analysis should naturally point toward what to do next (but save formal recommendations for the impact report).

---

## Quality Checklist (self-verify before output)

Before producing the final analysis, verify:
- [ ] Every outcome record for the PRD has been analyzed
- [ ] Delta calculations are mathematically correct (spot-check at least one)
- [ ] Assessment thresholds are applied consistently and directionality is correct
- [ ] Root cause analysis addresses all five Relate questions for each metric
- [ ] Contributing factors are specific, not generic
- [ ] HEART dimensions are only discussed where relevant
- [ ] Summary table matches the detailed sections
- [ ] All referenced artifact IDs (PRD, OKR, outcome records) actually exist in the data
- [ ] The overall summary includes both a number and a narrative insight
