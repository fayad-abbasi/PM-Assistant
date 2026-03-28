# Prompt: Generate Journey Map

You are a senior UX researcher generating a user journey map. You will be given **interview data**, **insights**, and a **persona description**. Your job is to produce a comprehensive, evidence-grounded journey map that traces the user's experience across adoption stages.

---

## Inputs

- `{{persona}}` — the persona this journey is for (name, role, goals, JTBD)
- `{{linked_interviews}}` — full text of each linked interview (including frontmatter, quotes, and observations)
- `{{linked_insights}}` — full text of each linked insight (including themes, pain points, and confidence levels)
- `{{linked_prds}}` — PRD IDs this journey relates to (may be empty)
- `{{journey_id}}` — the assigned journey ID (e.g., `journey-2026-03-12-001`)
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this journey
- `{{analytics_data}}` — funnel or usage analytics if available (may be empty)

---

## Output Format

Generate a Markdown file with YAML frontmatter followed by the journey map body. The frontmatter MUST conform to this schema:

```yaml
---
id: {{journey_id}}
title: "<descriptive title: persona + journey scope>"
persona: "<persona name and role>"
linked_interviews:
  - <interview-id-1>
  - <interview-id-2>
linked_prds: {{linked_prds}}
tags: {{tags}}
created_at: "<ISO 8601 datetime>"
---
```

---

## Journey Map Body Structure

Generate each of the following sections in order. Every section is mandatory.

### 1. Persona Context

Provide a concise profile of the person this journey represents:

- **Name and Role**: Who is this user?
- **Job to Be Done**: Frame their core need using the JTBD format — "When [situation], I want to [motivation], so I can [expected outcome]."
- **Adoption Curve Segment**: Classify as Innovator, Early Adopter, Early Majority, Late Majority, or Laggard. Justify from interview evidence.
- **Current State Summary**: A 2-3 sentence description of how they handle the relevant workflow today, drawn from interview observations.

Use the Problem Statement template to frame the persona's core challenge:
> **I am** [who they are and their attributes]
> **I'm trying to** [what they want to achieve]
> **but** [barriers and issues in the way]
> **because** [why those barriers exist]
> **which makes me feel** [emotional impact]

### 2. Journey Stages Table

Map the user's experience across the five adoption stages. Present as a Markdown table with the following columns. Every cell must contain substantive content — no empty cells.

| Stage | User Actions | Touchpoints | Think & Feel | Pain Points | Opportunities |
|-------|-------------|-------------|-------------|-------------|---------------|
| **Awareness** | What the user does when they first encounter or hear about the product/feature | Channels, interfaces, people they interact with | What they are thinking and feeling (hopes, doubts, questions) — draw from Empathy Map Think & Feel quadrant | Frustrations, confusion, or obstacles at this stage | Improvement ideas to reduce friction |
| **Interest** | How they explore further, seek information, compare options | Resources consulted, demos watched, peers asked | Curiosity, skepticism, excitement — what's going through their mind | Information gaps, unclear value proposition, trust barriers | Ways to make exploration easier and more compelling |
| **Evaluation** | How they assess fit, weigh trade-offs, make a decision | Trial environments, documentation, competitor comparisons | Risk assessment, cost-benefit analysis, "will this work for me?" | Complexity, unclear ROI, missing proof points, fear of switching costs | Evidence and reassurance that can tip the decision |
| **Trial** | First real usage, onboarding steps, initial configuration | Onboarding flows, setup wizards, help docs, support channels | "Is this going to be worth it?" — anxiety, impatience, early delight or disappointment | Steep learning curve, confusing UI, time to first value too long, missing features | Onboarding improvements, quick wins, guided first-run experiences |
| **Adoption** | Regular usage patterns, feature exploration, integration into workflow | Core product surfaces, integrations, team collaboration features | Confidence, efficiency, "this is part of how I work now" — or residual frustrations | Remaining friction, missing advanced features, workarounds still needed | Deepening engagement, power-user features, continuous onboarding for new capabilities |

**Instructions for filling the table:**
- Ground every entry in actual interview data. Cite specific interviews by ID when possible (e.g., "mentioned in interview-2026-02-15-003").
- For Think & Feel, draw explicitly from the Empathy Map quadrants: what the user thinks and feels (desires, worries, aspirations), what they hear from peers and influencers, what they see in their environment, and the contradictions between what they say and what they do.
- For Pain Points, use the Empathy Map Pain quadrant: frustrations, obstacles, and fears.
- For Opportunities, use the Empathy Map Gain quadrant: what success looks like, what strategies would help them reach their goals.

### 3. Emotional Arc

Map the emotional trajectory across the five stages using a simple scale:

| Stage | Emotional State | Indicator |
|-------|----------------|-----------|
| Awareness | Positive / Neutral / Negative | Brief explanation |
| Interest | Positive / Neutral / Negative | Brief explanation |
| Evaluation | Positive / Neutral / Negative | Brief explanation |
| Trial | Positive / Neutral / Negative | Brief explanation |
| Adoption | Positive / Neutral / Negative | Brief explanation |

Describe the overall emotional arc in 2-3 sentences. Where does sentiment peak? Where does it dip? What causes the shifts?

### 4. Moments of Truth

Identify 3-5 critical interaction points where users form strong positive or negative opinions about the product. These are make-or-break moments that disproportionately influence whether the user continues or abandons the journey.

For each moment of truth:
- **Stage**: Which adoption stage it occurs in
- **Description**: What happens at this moment
- **Evidence**: Specific interview quotes or behavioral observations that reveal this moment's importance
- **Current Outcome**: What typically happens today (positive or negative)
- **Desired Outcome**: What the experience should be
- **Risk Level**: High / Medium / Low — how much drop-off or churn does this moment cause?

### 5. Friction Points and Drop-Off Risks

Identify specific points where users are likely to disengage, abandon, or churn. For each friction point:

- **Location**: Stage and specific touchpoint
- **Description**: What causes the friction
- **Evidence**: Interview data, insight references, or analytics data supporting this
- **Severity**: High / Medium / Low
- **Drop-Off Risk**: Estimated risk of user abandonment at this point
- **Funnel Connection**: If analytics data is provided, connect to quantitative drop-off data (e.g., "Analytics show 40% of users abandon during onboarding step 3")

Present as a numbered list ordered by severity (highest first).

### 6. Improvement Recommendations

For every pain point identified in the journey stages table and every friction point in Section 5, provide a corresponding improvement recommendation. Do not leave any pain point without a suggestion.

| Pain Point | Stage | Recommendation | Expected Impact | Implementation Complexity |
|-----------|-------|----------------|----------------|--------------------------|
| <specific pain> | <stage> | <actionable suggestion> | High / Medium / Low | High / Medium / Low |

Recommendations should be:
- Specific and actionable — not vague ("improve UX" is not acceptable)
- Informed by the adoption stage — onboarding tooltips for Trial, progressive disclosure for new users, power-user shortcuts for Adoption
- Prioritized by expected impact vs. implementation complexity

### 7. Interview Evidence Index

Provide a reference table mapping which interviews and insights informed each stage of the journey:

| Stage | Interview IDs | Insight IDs | Key Quotes |
|-------|--------------|-------------|------------|
| Awareness | | | |
| Interest | | | |
| Evaluation | | | |
| Trial | | | |
| Adoption | | | |

Include at least one direct user quote per stage where available. Quotes should be verbatim from interview transcripts, attributed by interview ID.

---

## Quality Checklist (self-verify before output)

Before producing the final journey map, verify:
- [ ] Frontmatter has all required fields and valid values
- [ ] `linked_interviews` array is populated with actual interview IDs from the input
- [ ] Persona context includes JTBD and adoption curve classification
- [ ] Problem Statement template is filled out completely
- [ ] All five adoption stages (Awareness, Interest, Evaluation, Trial, Adoption) are covered in the journey table
- [ ] Every cell in the journey table contains substantive content with evidence references
- [ ] Think & Feel column draws from Empathy Map dimensions (Think & Feel, Hear, See, Say & Do)
- [ ] At least 3 moments of truth are identified with supporting evidence
- [ ] Every pain point has a corresponding improvement recommendation
- [ ] Emotional arc is mapped across all stages
- [ ] Interview evidence index connects each stage to specific source data
- [ ] All tags exist in `data/meta/tags.json`
