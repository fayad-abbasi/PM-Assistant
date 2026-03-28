# Analytics Summary — Usage and Analytics Data Prompt Template

You are an expert product analyst. Your task is to summarize imported usage or analytics data into a structured insight that combines quantitative evidence with interpretive narrative. Follow the frameworks and steps below precisely.

---

## Inputs

- **Analytics data**: Raw or pre-processed usage data (CSV, JSON, or pasted table). This may include event logs, funnel reports, cohort tables, feature adoption metrics, retention data, engagement scores, or similar quantitative sources.
- **Context** (optional): Any accompanying notes about what the data represents, the time period, the product area, or known caveats.
- **Existing insights and interviews** (optional): Prior qualitative findings from `data/insights/` and `data/interviews/` that may add context.

---

## Step 1: Funnel Analysis

If the data contains any sequential user flow (sign-up, onboarding, feature activation, checkout, etc.), perform funnel analysis.

### Process

1. **Identify the funnel stages**: List each step in the user journey that the data covers, in order.
2. **Calculate stage-to-stage conversion**: For each transition, compute the conversion rate and the absolute drop-off count.
3. **Identify the critical drop-off points**: Flag any transition where:
   - Conversion drops below 50%
   - The absolute number of lost users is largest
   - The conversion rate declined compared to a prior period (if comparative data exists)
4. **Characterize each drop-off**: For each critical drop-off, describe:
   - **Where**: The exact transition (Stage A to Stage B)
   - **How big**: The percentage and absolute number lost
   - **Potential why**: Based on the data alone, what might explain the drop-off? (complexity, load time, unclear value, too many steps, etc.)
   - **What we do not know**: What qualitative context is missing that interviews or usability testing could provide?

### Output Table

| Stage | Users Entering | Users Completing | Conversion Rate | Drop-off | Flag |
|-------|---------------|-----------------|-----------------|----------|------|
| ... | ... | ... | ... | ... | ... |

---

## Step 2: Cohort Analysis

If the data contains time-based user groupings (sign-up date, first-use date, feature launch date, etc.), perform cohort analysis.

### Process

1. **Define cohorts**: Group users by the relevant time dimension (week, month, quarter) or by a meaningful event (signed up before/after a feature launch, acquired through different channels, etc.).
2. **Track retention over time**: For each cohort, calculate the percentage of users still active at key intervals (day 1, day 7, day 14, day 30, day 60, day 90 — adjust to match available data).
3. **Identify retention patterns**:
   - **Early drop-off**: Cohorts losing more than 50% of users in the first week signal onboarding or first-experience problems.
   - **Flattening curve**: The point where retention stabilizes indicates where users have found core value.
   - **Cohort divergence**: If newer cohorts retain better (or worse) than older ones, identify what changed between them.
4. **Calculate engagement signals**: If the data supports it, look at:
   - Frequency of use (daily, weekly, monthly active rates)
   - Depth of use (number of features used, session duration, actions per session)
   - Breadth of use (how many distinct features or areas the user engages with)

### Output Table

| Cohort | Size | Day 1 | Day 7 | Day 14 | Day 30 | Day 60 | Day 90 | Notes |
|--------|------|-------|-------|--------|--------|--------|--------|-------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

## Step 3: Numbers + Narrative

This is the core analytical step. For every quantitative finding, pair the number with a narrative interpretation. Follow the principle: numbers without narrative are blind; narrative without numbers is anecdotal.

### For Each Key Finding

| Element | Content |
|---------|---------|
| **The Number** | The specific metric, rate, count, or trend — stated precisely |
| **What It Shows** | A neutral description of what the data tells us at face value |
| **What It Might Mean** | An interpretive hypothesis about the user behavior or product dynamic driving this number. Frame as "This may indicate..." or "One explanation is..." — never as certainty |
| **What We Cannot Conclude** | Explicitly state the limits of the data. What alternative explanations exist? What confounding factors might be at play? |
| **Where Qualitative Research Would Help** | Identify the specific question that an interview, usability test, or survey could answer to move from hypothesis to validated insight |

---

## Step 4: Pattern Identification

Across all the analyses performed, identify the following pattern types:

### Drop-off Patterns
Points in user journeys where significant numbers of users disengage. For each:
- Location in the journey
- Magnitude (% and absolute)
- Whether it is worsening, stable, or improving over time

### Retention Patterns
How user engagement evolves after initial acquisition. For each:
- Time to core value (when does retention start to flatten?)
- Segments that retain better or worse
- Correlation with specific onboarding steps or early actions

### Engagement Signals
Behaviors that correlate with long-term retention or high satisfaction. For each:
- The specific behavior or action
- How strongly it correlates with retention
- Whether it is increasing or decreasing over time

### Red Flags
Metrics that suggest systemic problems:
- Declining trend lines
- Segments with disproportionately poor outcomes
- Metrics that are significantly below industry benchmarks (if known)
- Leading indicators of churn

---

## Step 5: Qualitative Research Flags

For each major finding, assess whether qualitative research (interviews, usability testing, contextual inquiry) would add meaningful context. Produce a prioritized list of recommended qualitative investigations.

### Format

| Priority | Finding | Open Question | Recommended Method | Expected Value |
|----------|---------|--------------|-------------------|----------------|
| 1 | ... | "Why are users dropping off at step X?" | 5-8 user interviews focused on step X experience | Understand the blockers and emotional state at this transition |
| 2 | ... | ... | ... | ... |

**Priority criteria:**
- **High**: The data shows a significant problem but gives no indication of cause. Qualitative research is essential before acting.
- **Medium**: The data suggests a pattern with plausible explanations, but validation is needed before investing in a solution.
- **Low**: The data is clear enough to act on, but qualitative depth would strengthen confidence or reveal optimization opportunities.

---

## Output Format

Produce a Markdown file with the following structure:

```markdown
---
title: "{Descriptive title for the analytics summary}"
data_source: "{Description of the data source, e.g., 'Amplitude export, Jan-Mar 2026'}"
period: "{Time period covered}"
created_at: "{ISO-8601 datetime}"
---

## Key Metrics

{A concise table or bullet list of the 5-10 most important metrics from the data, each with its value and a one-line interpretation.}

| Metric | Value | Interpretation |
|--------|-------|---------------|
| ... | ... | ... |

## Funnel Analysis

{Funnel table and narrative for each critical drop-off point. If no funnel data exists, state "No sequential funnel data available in this dataset."}

## Cohort Analysis

{Cohort retention table and narrative for key patterns. If no cohort data exists, state "No time-based cohort data available in this dataset."}

## Patterns

### Drop-off Patterns
{Bulleted findings}

### Retention Patterns
{Bulleted findings}

### Engagement Signals
{Bulleted findings}

### Red Flags
{Bulleted findings}

## Hypotheses

{For each major pattern, state a testable hypothesis in the format:}
> **If** [condition], **then** [predicted behavior/outcome], **because** [reasoning from data].

{Include 3-7 hypotheses, ranked by potential impact.}

## Recommended Next Steps

### Immediate Actions
{Actions that the data supports with sufficient confidence — no further research needed.}

### Qualitative Research Needed
{Prioritized table of recommended investigations as defined in Step 5.}

### Deeper Quantitative Analysis
{Follow-up data questions that require additional data pulls, segmentation, or instrumentation.}

## Appendix: Data Notes

- **Source**: {Where the data came from}
- **Period**: {Exact date range}
- **Known caveats**: {Any data quality issues, missing segments, sampling biases, or instrumentation gaps}
- **Definitions**: {Definitions of key metrics or events if they are non-obvious}
```

---

## Rules

1. Never present a number without context. Every metric must include what it measures, the time period, and a baseline for comparison (prior period, benchmark, or target) where available.
2. Clearly separate what the data shows (fact) from what it might mean (interpretation). Use hedging language ("may indicate", "suggests", "one explanation is") for all interpretive statements.
3. Do not fabricate benchmarks or industry norms. If you reference a benchmark, state its source. If no benchmark is available, say so.
4. Flag data quality issues explicitly. If the dataset has gaps, small sample sizes, missing segments, or ambiguous event definitions, note these in the Data Notes appendix and factor them into your confidence levels.
5. When recommending qualitative research, be specific about the question to answer, the method, and the expected value — not generic "do more research" recommendations.
6. If the data is insufficient for funnel or cohort analysis, skip those sections and state why rather than forcing an incomplete analysis.
7. Hypotheses must be falsifiable. Each one should specify what evidence would confirm or refute it.
8. This template produces a summary document, not a frontmattered insight artifact. If the findings warrant creating a formal insight (type: single or batch), note this in Recommended Next Steps with guidance on which themes to focus on.
