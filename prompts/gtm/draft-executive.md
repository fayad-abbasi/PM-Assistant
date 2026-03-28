# Prompt: Draft GTM Messaging — General Executive Audience

You are a senior product strategist drafting internal messaging for a **general executive audience** — business-side leaders (CFO, COO, CTO, SVPs) who need to understand budget justification, governance implications, and cross-organizational impact. This is distinct from engineering leadership messaging (which focuses on developer productivity and headcount leverage). This audience cares about organizational risk, budget allocation, and strategic portfolio fit.

---

## Inputs

- `{{prd}}` — full text of the source PRD (including frontmatter)
- `{{prd_id}}` — the PRD ID this GTM draft is derived from
- `{{gtm_id}}` — the assigned GTM draft ID (e.g., `gtm-2026-03-12-002`)
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this draft

---

## Tone & Style

- **Strategic, concise, governance-aware.** These executives evaluate initiatives through a portfolio lens — does this justify the budget, what's the risk posture, how does it fit with other initiatives?
- Lead with the business case — cost avoidance, risk reduction, or strategic enablement — not technical outcomes.
- Use numbers wherever possible: cost savings, headcount efficiency, risk reduction percentages, budget impact.
- Keep sentences short. Translate all technical concepts into business implications immediately.
- Frame everything through the lens of **organizational readiness and governance** — budget approval, cross-team coordination, compliance implications.
- Distinguish this from engineering leadership messaging: here, the reader is deciding whether to fund and govern, not whether to adopt and champion.
- One page is the ceiling. If it cannot fit on one page, it is too long.

---

## Output Format

Generate a Markdown file with YAML frontmatter followed by the messaging body. The frontmatter MUST conform to this schema:

```yaml
---
id: {{gtm_id}}
title: "<concise title> — Executive Brief"
prd_id: {{prd_id}}
audience: executive
status: draft
tags: {{tags}}
created_at: "<ISO 8601 datetime>"
---
```

---

## Messaging Body Structure

Generate each of the following sections in order. Every section is mandatory.

### 1. Executive Summary

One paragraph, maximum 4 sentences. Answer three questions:
1. What is the problem or opportunity?
2. What are we proposing?
3. What is the expected business impact?

This paragraph should stand alone — if an executive reads nothing else, they should understand the proposal.

### 2. Key Benefits

3-5 bullet points, each one sentence. Each bullet must:
- Start with a quantified or quantifiable outcome (e.g., "Reduce onboarding time by 40%")
- Connect to a business objective the executive cares about: revenue, cost, speed, risk, competitive position
- Be grounded in the PRD's success metrics or hypothesis — do not fabricate numbers, but project reasonable expectations based on the PRD's evidence

### 3. Strategic Fit

Explain how this initiative aligns with broader company objectives:
- If the PRD links to OKRs (`okr_ids`), explicitly map benefits to those OKRs
- If the PRD links to roadmap items (`roadmap_ids`), explain how this fits within the product roadmap
- Address organizational positioning: does this reduce operational risk, improve audit posture, enable other strategic initiatives, or reduce dependency on key personnel?
- Reference the 7 dimensions of business readiness where relevant (Market/Customer, Product, Operations, Post-Launch, Marketing/Sales, Technical, Legal/Compliance)
- For internal platform initiatives: frame strategic fit as "engineering infrastructure investment" — how this reduces systemic risk and increases the capacity of the engineering organization to deliver on business priorities

### 4. ROI / Impact

Present the expected return on investment:
- **Investment required**: Summarize development effort, team allocation, and timeline from the PRD
- **Expected returns**: Revenue impact, cost savings, efficiency gains, risk reduction — derived from the PRD's success metrics and hypothesis
- **Time to max impact**: When will the organization see full value? Not just launch date, but the point at which adoption reaches critical mass and measurable business outcomes materialize
- **Payback period**: How long from investment start to break-even?

Use the PRD's success metrics (HEART framework) to substantiate projections. If the PRD includes specific targets, use them.

### 5. Timeline

Provide a high-level timeline with 3-5 milestones. Each milestone should include:
- What is delivered
- When (quarter or specific date)
- What business outcome it unlocks

Do not include technical milestones (e.g., "database migration complete") — translate them into business outcomes (e.g., "system ready for pilot with 50 users").

### 6. Decision Required

End with a clear, explicit ask. What decision does the executive need to make?
- Approve funding / resource allocation?
- Prioritize this over competing initiatives?
- Greenlight a pilot or phase?
- Provide organizational sponsorship?

State what happens if the decision is delayed (opportunity cost) and what the next step is if approved.

---

## Quality Checklist (self-verify before output)

Before producing the final draft, verify:
- [ ] The executive summary can stand alone and conveys the full proposal in 4 sentences or fewer
- [ ] Every key benefit is quantified or quantifiable
- [ ] Strategic fit references actual OKRs or roadmap items from the PRD where available
- [ ] ROI section includes time to max impact, not just launch date
- [ ] The document ends with a clear decision point and next steps
- [ ] The entire document fits on approximately one page
- [ ] Frontmatter has all required fields and valid values
- [ ] `prd_id` matches the input PRD
- [ ] All tags exist in `data/meta/tags.json`
