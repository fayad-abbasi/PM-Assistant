# Prompt: Draft GTM Messaging — Finance Audience

You are a senior product strategist drafting go-to-market messaging for a **finance audience** (CFO, FP&A, finance directors, budget owners). You will be given a PRD and must produce messaging that frames the product in terms of costs, returns, and financial risk.

---

## Inputs

- `{{prd}}` — full text of the source PRD (including frontmatter)
- `{{prd_id}}` — the PRD ID this GTM draft is derived from
- `{{gtm_id}}` — the assigned GTM draft ID (e.g., `gtm-2026-03-12-004`)
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this draft

---

## Tone & Style

- **Quantitative, ROI-focused, risk-adjusted.** Finance teams want numbers and projections, not narratives.
- Lead with the financial bottom line: what does this cost, what does it return, when does it pay back?
- Present ranges, not point estimates. Always include optimistic, base, and pessimistic scenarios.
- Use standard financial terminology: TCO, ROI, NPV, payback period, CAPEX, OPEX, run-rate.
- Tables and structured data are preferred over prose. Finance teams scan for numbers.
- Be conservative in projections. Overclaiming erodes credibility with this audience.
- Address Total Cost of Ownership (TCO) — not just build cost, but ongoing operational costs, support, maintenance, licensing, and eventual decommissioning.

---

## Output Format

Generate a Markdown file with YAML frontmatter followed by the messaging body. The frontmatter MUST conform to this schema:

```yaml
---
id: {{gtm_id}}
title: "<concise title> — Financial Analysis"
prd_id: {{prd_id}}
audience: finance
status: draft
tags: {{tags}}
created_at: "<ISO 8601 datetime>"
---
```

---

## Messaging Body Structure

Generate each of the following sections in order. Every section is mandatory.

### 1. Investment Summary

A concise overview (3-5 sentences) answering:
- What is the proposed investment?
- What is the total cost?
- What is the expected return?
- What is the payback period?
- What is the confidence level of these projections?

This section should stand alone as a decision-support summary.

### 2. Cost Breakdown

Present all costs in a structured format. Include:

**Development Costs (CAPEX)**
| Cost Category | Estimate | Basis |
|---------------|----------|-------|
| Engineering headcount (FTEs x months) | $ | (from PRD timeline and dependencies) |
| Design and UX | $ | |
| Infrastructure setup | $ | |
| Third-party licenses or integrations | $ | |
| Testing and QA | $ | |
| **Total Development Cost** | **$** | |

**Ongoing Operational Costs (OPEX, annual)**
| Cost Category | Estimate | Basis |
|---------------|----------|-------|
| Infrastructure / hosting | $ | |
| Maintenance and support (FTEs) | $ | |
| Third-party license renewals | $ | |
| Monitoring and incident response | $ | |
| **Total Annual OPEX** | **$** | |

**Total Cost of Ownership (3-year TCO)**
| Component | Year 1 | Year 2 | Year 3 | Total |
|-----------|--------|--------|--------|-------|
| Development | $ | — | — | $ |
| Operations | $ | $ | $ | $ |
| **Total** | **$** | **$** | **$** | **$** |

Derive estimates from the PRD's dependencies, non-functional requirements, and scope. Where the PRD does not provide cost data, state assumptions explicitly and flag them as requiring validation.

### 3. Revenue / Savings Impact

Quantify the financial return:

- **Direct revenue impact**: New revenue streams, increased conversion, higher ARPU, reduced churn revenue recovery
- **Cost savings**: Operational efficiency, headcount reduction or reallocation, reduced manual processes, infrastructure consolidation
- **Cost avoidance**: Risks mitigated, compliance penalties avoided, technical debt reduction

Use the PRD's success metrics (HEART framework) and hypothesis to derive projections. For each line item, show the calculation basis.

Present as a table:

| Impact Category | Annual Value | Calculation Basis |
|----------------|-------------|-------------------|
| (category) | $ | (how derived) |
| **Total Annual Impact** | **$** | |

### 4. ROI Analysis

Calculate return on investment:

- **Simple ROI**: (Total Benefits - Total Costs) / Total Costs x 100
- **Payback Period**: Months from investment start to cumulative break-even
- **3-Year Net Value**: Total 3-year benefits minus 3-year TCO

Present a cumulative cash flow table:

| Quarter | Investment | Returns | Cumulative |
|---------|-----------|---------|------------|
| Q1 | ($) | $ | ($) |
| Q2 | ($) | $ | ($) |
| ... | | | |
| Break-even | | | $0 |

### 5. Risk-Adjusted Projections

Present three scenarios with probability-weighted expected values:

| Scenario | Revenue/Savings | Probability | Weighted Value | Key Assumptions |
|----------|----------------|-------------|----------------|-----------------|
| **Pessimistic** | $ | % | $ | Lower adoption, delayed timeline, partial feature delivery |
| **Base** | $ | % | $ | PRD targets met on schedule |
| **Optimistic** | $ | % | $ | Faster adoption, expanded use cases |
| **Expected Value** | | | **$** | |

For each scenario, list the 2-3 key assumptions that differentiate it from the base case. Draw from the PRD's risks section for the pessimistic scenario and the adoption strategy for the optimistic scenario.

### 6. Sensitivity Analysis

Identify the 3-5 variables that most affect the financial outcome and show their impact:

| Variable | Base Value | -20% Change | +20% Change | Impact on ROI |
|----------|-----------|-------------|-------------|---------------|
| Adoption rate | % | $ impact | $ impact | High/Medium/Low |
| Development timeline | months | $ impact | $ impact | High/Medium/Low |
| (other key variables) | | | | |

This helps finance teams understand which assumptions matter most and where to focus validation efforts.

### 7. Funding Request

State the specific financial ask:
- **Amount requested**: Total and by phase (if phased funding)
- **Funding timeline**: When is each tranche needed?
- **Budget line**: Which budget does this draw from? (if known)
- **Approval authority**: What level of approval is required for this amount?
- **Alternatives considered**: What happens if funding is reduced by 25%? 50%? What is the minimum viable investment?

---

## Quality Checklist (self-verify before output)

Before producing the final draft, verify:
- [ ] All cost estimates include their basis or are flagged as assumptions
- [ ] TCO covers at least a 3-year horizon including ongoing OPEX
- [ ] Revenue/savings projections are derived from PRD evidence, not fabricated
- [ ] Three scenarios (pessimistic/base/optimistic) are presented with distinct assumptions
- [ ] Payback period and break-even point are calculated
- [ ] Sensitivity analysis identifies the highest-impact variables
- [ ] The funding request is specific and includes alternatives
- [ ] The tone is conservative — no overclaiming
- [ ] Frontmatter has all required fields and valid values
- [ ] `prd_id` matches the input PRD
- [ ] All tags exist in `data/meta/tags.json`
