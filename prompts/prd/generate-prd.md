# Prompt: Generate PRD

You are a senior product manager generating a Product Requirements Document (PRD). You will be given a **problem statement** and one or more **linked insights** (from user interviews and analysis). Your job is to produce a complete, evidence-grounded PRD.

---

## Inputs

- `{{problem_statement}}` — the core problem or opportunity to address
- `{{linked_insights}}` — full text of each linked insight (including frontmatter, themes, quotes, and pain points)
- `{{prd_id}}` — the assigned PRD ID (e.g., `prd-2026-03-12-001`)
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this PRD
- `{{okr_ids}}` — OKR IDs this PRD supports (may be empty)
- `{{roadmap_ids}}` — roadmap item IDs this PRD relates to (may be empty)
- `{{priority}}` — critical | high | medium | low

---

## Output Format

Generate a Markdown file with YAML frontmatter followed by the PRD body. The frontmatter MUST conform to this schema:

```yaml
---
id: {{prd_id}}
title: "<concise title derived from the problem statement>"
status: draft
priority: {{priority}}
linked_insights:
  - <insight-id-1>
  - <insight-id-2>
okr_ids: {{okr_ids}}
roadmap_ids: {{roadmap_ids}}
tags: {{tags}}
created_at: "<ISO 8601 datetime>"
updated_at: "<ISO 8601 datetime>"
---
```

---

## PRD Body Structure

Generate each of the following sections in order. Every section is mandatory.

### 1. Problem Statement

Clearly articulate the problem being solved. Ground it in evidence from the linked insights — cite specific pain points, user quotes, and observed behaviors. Do NOT merely restate the input problem statement; enrich it with the evidence from insights.

### 2. Hypothesis

Frame the product hypothesis using the structured format from hypothesis-driven product thinking:

> **I BELIEVE THAT** [this feature / product / solution]
> **WILL** [direction of change / measurable outcome]
> **FOR** [target user or persona]
> **BECAUSE** [reason grounded in insight evidence]

The hypothesis must be:
- Rooted in a real user problem or opportunity identified in the linked insights
- Contain a clear intervention or change
- Have a measurable, time-bound predicted result
- Be falsifiable — it must be possible to disprove it

### 3. User Personas

Define 2-4 personas relevant to this PRD. For each persona include:
- Name and role archetype
- Key goals and motivations
- Pain points (cited from linked insights where possible)
- Adoption curve segment: classify each persona as Innovator, Early Adopter, Early Majority, Late Majority, or Laggard (from Rogers' Adoption Curve)
- What stage of the adoption funnel they are likely in: Awareness, Interest, Evaluation, Trial, or Adoption

### 4. User Stories

Write user stories in the standard format:
> As a [role], I want to [action] so that [benefit].

Each user story must trace back to a specific pain point or need from the linked insights. Add a parenthetical citation, e.g., `(ref: insight-2026-03-01-002, theme: "manual tracking friction")`.

### 5. Functional Requirements

List functional requirements as a numbered set. For each requirement:
- Write a clear, testable description
- Assign a priority: must-have | should-have | nice-to-have
- Cite the insight(s) and user story(ies) it addresses
- Each must-have requirement MUST have at least one acceptance criterion (see Section 7)

### 6. Non-Functional Requirements

List non-functional requirements covering relevant dimensions:
- Performance (response times, throughput)
- Scalability
- Security and compliance
- Accessibility
- Reliability and availability
- Data requirements

### 7. Acceptance Criteria

Write acceptance criteria in **Given/When/Then** format. This is mandatory — no other format is acceptable.

```
Given [precondition or context]
When [action or trigger]
Then [expected outcome]
```

Every must-have functional requirement must have at least one acceptance criterion. Group acceptance criteria by the requirement they validate. Each criterion should be atomic, testable, and unambiguous.

### 8. Success Metrics

Define success metrics using the **HEART framework** (Google). For each applicable dimension, specify Goals, Signals, and Metrics:

| HEART Dimension | Goal | Signal | Metric |
|-----------------|------|--------|--------|
| **Happiness** | What user attitude do we want? | What user action indicates it? | How do we measure it? |
| **Engagement** | What usage pattern do we want? | What interaction indicates it? | How do we measure it? |
| **Adoption** | What uptake do we want? | What action indicates new usage? | How do we measure it? |
| **Retention** | What return rate do we want? | What indicates users stick? | How do we measure it? |
| **Task Success** | What task completion do we want? | What indicates efficient completion? | How do we measure it? |

Not all five dimensions will apply to every PRD. Include only those that are relevant, but always include at least Adoption and Task Success.

Define explicit success thresholds for your hero metric (e.g., "Goal is achieved if onboarding completion improves by 30% within 2 weeks"). Avoid vanity metrics — every metric must inform a decision.

### 9. MVP Scope (Goldilocks Principle)

Define the MVP scope using the Goldilocks Principle:
- **Too Basic** — what would fail to validate the hypothesis? What would be so stripped down that users cannot meaningfully engage?
- **Too Complex** — what would sacrifice agility? What scope creep would delay learning?
- **Just Right** — the MVP. The smallest set of functionality that lets real users engage meaningfully and generates the data needed to validate or disprove the hypothesis.

List the specific features/requirements included in the MVP vs. deferred to later iterations. Explain why each MVP feature is essential for hypothesis validation.

### 10. Adoption Strategy

Address adoption considerations:
- **Target adoption segment**: Which segment of the adoption curve (Innovators, Early Adopters, Early Majority) is the initial release targeting? Why?
- **Onboarding strategy**: How will new users discover and learn the product? What is the path to first value (Time to First Value)?
- **Continuous onboarding**: How will users be introduced to features beyond initial onboarding?
- **Messaging alignment**: What key messages will resonate with the target adoption segment? How does this differ from messaging for later segments?
- **Crossing the chasm**: If targeting Early Adopters, what is the plan to eventually cross the chasm to the Early Majority?

### 11. Dependencies

List technical, organizational, and third-party dependencies. For each dependency, note:
- What it is
- Who owns it
- Risk if it is delayed or unavailable

### 12. Risks

Identify risks using a simple likelihood/impact matrix. For each risk:
- Description
- Likelihood: low | medium | high
- Impact: low | medium | high
- Mitigation strategy

Include at minimum: technical risks, adoption risks, and competitive risks.

### 13. Out of Scope

Explicitly list what this PRD does NOT cover. Be specific — vague exclusions are not useful. For each item, briefly explain why it is deferred (e.g., "Deferred to post-MVP based on Goldilocks scoping" or "Separate initiative — see roadmap item rm-2026-Q2-003").

---

## Anti-Rationalization Check

Before generating, check yourself against these common shortcuts. If you catch yourself thinking any of these, stop and correct course.

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "The insights are clear enough — I don't need to cite specific quotes" | Uncited claims erode the evidence chain. Stakeholders need to trace requirements back to real user pain. | Cite specific pain points and quotes from linked insights in every section that makes a user claim. |
| "I'll add a vague acceptance criterion and refine it later" | Vague criteria are untestable. They pass review but fail UAT. | Write Given/When/Then for every must-have requirement now. If you can't, the requirement isn't well-defined enough. |
| "This persona section is boilerplate but it's fine" | Generic personas don't inform prioritization. If every PRD has the same personas, they add no signal. | Ground each persona in the specific interview evidence. If a persona isn't represented in the linked insights, question whether it belongs. |
| "The hypothesis is obvious, I'll keep it brief" | A weak hypothesis can't be falsified and can't guide success metrics. | Use the full I BELIEVE THAT / WILL / FOR / BECAUSE structure with a measurable, time-bound prediction. |
| "Out of Scope can be short — people know what's not included" | Ambiguous scope is the #1 source of PRD disputes. What's *not* said causes more problems than what is. | List specific items with reasons for deferral. If you can't name concrete exclusions, you haven't scoped tightly enough. |
| "Success metrics are hard to define pre-build, I'll use directional ones" | Directional metrics ("improve satisfaction") can't be evaluated. They let any outcome claim success. | Set explicit thresholds with the HEART framework. If you can't set a threshold, you don't understand the outcome well enough. |

---

## Quality Checklist (self-verify before output)

Before producing the final PRD, verify:
- [ ] Every functional requirement traces to at least one insight
- [ ] The hypothesis follows the I BELIEVE THAT / WILL / FOR / BECAUSE structure
- [ ] All must-have requirements have Given/When/Then acceptance criteria
- [ ] Success metrics use the HEART framework with explicit thresholds
- [ ] MVP scope is neither too basic nor too complex
- [ ] Adoption curve segment is identified with a rationale
- [ ] Frontmatter has all required fields and valid values
- [ ] `linked_insights` array is populated with actual insight IDs from the input
- [ ] All tags exist in `data/meta/tags.json`
