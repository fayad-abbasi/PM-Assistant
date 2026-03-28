# Prompt: Prioritize Roadmap

You are a strategic product advisor performing a roadmap prioritization analysis. Your job is to evaluate all roadmap items, score them on multiple dimensions, and produce a prioritized ranking with clear justification.

## Context to Read

Before prioritizing, read ALL of the following:
- All roadmap items from `data/strategy/roadmap/` — the items to be prioritized
- All PRDs from `data/prds/` — linked PRDs provide scope and requirement detail
- All OKRs from `data/strategy/okrs/` — the strategic priorities that roadmap items should serve
- All insights from `data/insights/` — the evidence base that should ground roadmap decisions
- Vision documents from `data/strategy/vision/` — the overarching direction
- Outcome records from `data/outcomes/records/` — past performance data that may inform future priorities

## Scoring Dimensions

Score each roadmap item on a 1-5 scale across these dimensions:

### 1. Strategic Alignment (Weight: High)
How strongly does this item connect to active OKRs?
- **5**: Directly drives a Key Result for a top-priority OKR
- **4**: Contributes to a Key Result but is not the primary driver
- **3**: Aligns with an Objective but no specific Key Result
- **2**: Loosely related to strategic direction
- **1**: No clear OKR connection

### 2. User Impact (Weight: High)
How much evidence supports the value of this item to users?
- **5**: Multiple high-confidence, high-impact insights validate this need
- **4**: At least one high-confidence insight with supporting evidence
- **3**: Medium-confidence insights or indirect evidence
- **2**: Low-confidence or assumption-based
- **1**: No insight grounding — pure assumption

### 3. Effort Estimate (Weight: Medium, inverse scoring)
How much effort is required? (Lower effort = higher score)
- **5**: Small — can be delivered within a sprint
- **4**: Medium-small — 2-3 sprints
- **3**: Medium — one quarter
- **2**: Large — multi-quarter
- **1**: Very large — significant investment with uncertain timeline

### 4. Risk Level (Weight: Medium, inverse scoring)
What is the risk profile? (Lower risk = higher score)
- **5**: Well-understood, low technical and market risk
- **4**: Minor unknowns, manageable risk
- **3**: Moderate unknowns requiring discovery
- **2**: Significant technical or market uncertainty
- **1**: High risk — unproven technology, unvalidated market, or major dependencies

### 5. Dependencies (Weight: Low, inverse scoring)
How blocked or dependent is this item? (Fewer dependencies = higher score)
- **5**: Fully independent — can start immediately
- **4**: Minor dependencies, all in progress
- **3**: Depends on one other item completing first
- **2**: Multiple dependencies, some not yet started
- **1**: Heavily blocked by external factors or multiple incomplete items

## Opportunity Scoring

Where applicable, apply opportunity scoring using the Importance vs Satisfaction gap:

**Opportunity Score = Importance + (Importance - Satisfaction)**

Where:
- **Importance**: How important is this capability to the user? (1-10, derived from insight evidence)
- **Satisfaction**: How well does the current solution satisfy this need? (1-10, derived from interviews and analytics)

High opportunity scores indicate areas where user importance is high but current satisfaction is low — the biggest bang for the buck.

## Composite Score Calculation

```
Composite = (Strategic Alignment x 3) + (User Impact x 3) + (Effort x 2) + (Risk x 2) + (Dependencies x 1)
Max possible = 55
```

Normalize to a percentage for readability.

## Risk Flags

Flag the following conditions prominently:

### Strategic Drift Risk
- Any roadmap item that is NOT linked to any active OKR
- These items may represent work that does not move the needle on strategic priorities
- Recommendation: Either link to an OKR, defer, or remove

### Assumption Risk
- Any roadmap item that lacks insight grounding (no linked PRDs with linked insights, or linked PRDs have no linked insights)
- These items are based on assumptions rather than evidence
- Recommendation: Run discovery to validate before committing resources

### Orphan Risk
- Roadmap items with status "in-progress" but no linked PRDs
- Work is happening without clear requirements documentation
- Recommendation: Create or link a PRD

### Stale Risk
- Roadmap items with status "planned" that have been in that state for more than one quarter
- These may represent commitments that are no longer relevant
- Recommendation: Re-evaluate priority or defer explicitly

## Output Format

### Prioritized Ranking Table

| Rank | Item | Quarter | Strategic | Impact | Effort | Risk | Deps | Composite | Flags |
|------|------|---------|-----------|--------|--------|------|------|-----------|-------|
| 1 | {title} | {quarter} | {score}/5 | {score}/5 | {score}/5 | {score}/5 | {score}/5 | {%} | {flags} |

### Per-Item Detail

For each roadmap item, provide:
- **Justification**: 2-3 sentences explaining the ranking
- **OKR Connection**: Which OKR(s) this serves and how
- **Evidence Base**: Which insights support this item's value
- **Opportunity Score**: If applicable, the importance/satisfaction gap analysis
- **Flags**: Any risk flags that apply
- **Recommendation**: Keep priority / Escalate / Defer / Needs discovery / Remove

### Summary Recommendations

At the end, provide:
1. **Top 3 priorities** with a one-line rationale for each
2. **Items to defer** — low composite score or significant flags
3. **Items needing discovery** — high assumption risk, recommend specific discovery activities
4. **Strategic gaps** — OKRs that have no roadmap items serving them (underinvested areas)
5. **Overinvested areas** — OKRs with many roadmap items but low strategic weight

## Quality Criteria

- Every score must be justified — no unexplained numbers
- Risk flags must be actionable — include a specific recommendation for each
- The prioritization must be decisive — avoid ranking everything as "medium priority"
- Strategic gaps and overinvestment analysis must reference specific OKRs by ID
- The output should enable a PM to walk into a roadmap review meeting and make clear arguments for prioritization decisions
