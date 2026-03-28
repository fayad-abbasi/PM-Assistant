# PRD Evaluation Rubric

**Artifact type**: `prd`
**Rubric name**: `rubric-prd`

Use this rubric with the judge prompt to evaluate Product Requirements Documents.

---

## Dimensions

### 1. completeness

**What it measures**: Are all required PRD sections present and substantive?

Required sections: Problem Statement, Hypothesis, Personas, User Stories, Functional Requirements, Non-Functional Requirements, Acceptance Criteria, Success Metrics, Risks and Mitigations, Scope (in-scope and out-of-scope).

| Score | Criteria |
|-------|----------|
| **1** | Fewer than half of the required sections are present. The document reads as a feature request, not a PRD. |
| **2** | Most sections are listed but several are stubs or placeholders (e.g., "TBD", empty tables). Key sections like acceptance criteria or success metrics are missing. |
| **3** | All required sections are present. Some sections are thin — for example, risks list only 1-2 items, or personas lack behavioral detail. Functional as a draft. |
| **4** | All sections are present with meaningful content. Personas have goals and pain points. Risks include likelihood and mitigation plans. Success metrics have targets. Minor gaps remain. |
| **5** | Every section is thorough. Personas are backed by research. Requirements are prioritized (MoSCoW or similar). Risks include contingency plans. Scope boundaries are explicit with rationale for exclusions. For DevEx PRDs: technical feasibility is assessed, migration paths are defined, backward compatibility is addressed, and developer adoption friction is explicitly considered. |

---

### 2. insight_grounding

**What it measures**: Are requirements traced back to specific insights with evidence?

Every PRD must link to at least one insight. This dimension checks whether those links are meaningful — not just ID references but actual evidence threading from user research through to requirements.

| Score | Criteria |
|-------|----------|
| **1** | No linked insights. Requirements appear invented without research backing. The `linked_insights` frontmatter field is empty or absent. |
| **2** | Insights are referenced in frontmatter but never mentioned in the document body. There is no visible connection between research findings and the stated requirements. |
| **3** | Insights are referenced and summarized in the document. Some requirements can be traced to an insight, but the mapping is incomplete — several requirements have no clear research basis. |
| **4** | Most requirements are explicitly tied to insights. The PRD includes direct quotes or paraphrased evidence from interviews or analytics. The reasoning from insight to requirement is clear. |
| **5** | Every requirement traces to a specific insight with supporting evidence (quotes, data points, or behavioral observations). The PRD uses a traceability structure (e.g., a table or inline references) that makes the research-to-requirement chain auditable. Numbers and narrative are both present. |

---

### 3. acceptance_criteria_quality

**What it measures**: Are all acceptance criteria in proper Given/When/Then format, testable, and unambiguous?

Per project conventions, acceptance criteria must use Given/When/Then format. This dimension evaluates both format compliance and substantive quality.

| Score | Criteria |
|-------|----------|
| **1** | No acceptance criteria are present, or they are informal statements like "the feature should work correctly." |
| **2** | Some acceptance criteria exist but are not in Given/When/Then format. Criteria are vague or untestable (e.g., "Given a user, When they use the feature, Then it works well"). |
| **3** | Most criteria use Given/When/Then format. Some criteria are testable, but others contain ambiguous terms ("quickly", "appropriate", "correctly") without measurable thresholds. |
| **4** | All criteria use proper Given/When/Then format. Most are testable with clear expected outcomes. Edge cases and error states are partially covered. Minor ambiguities remain in 1-2 criteria. |
| **5** | All criteria are in Given/When/Then format with specific, measurable conditions and outcomes. Edge cases, error states, and boundary conditions are covered. Each criterion could be handed directly to QA without further clarification. No ambiguous language. For platform PRDs: criteria cover both the happy path and the migration/rollback path. |

---

### 4. adoption_readiness

**What it measures**: Does the PRD address how the product will be adopted by target users?

Evaluated through the HEART framework lens (Happiness, Engagement, Adoption, Retention, Task Success). A strong PRD anticipates not just what to build but how users will discover, learn, and continue using it.

| Score | Criteria |
|-------|----------|
| **1** | No mention of target user segments, onboarding, or adoption strategy. The PRD assumes engineers will adopt because it's mandated. |
| **2** | Target users are named but adoption is not addressed. No onboarding considerations, no adoption metrics, no discussion of how engineers move from awareness to regular usage. No migration path from existing tools or workflows. |
| **3** | The PRD identifies target user segments and includes a basic rollout plan but no migration path from existing tools. Adoption metrics are absent or generic ("track adoption rate"). HEART dimensions are not explicitly addressed. |
| **4** | The PRD defines target segments with adoption-stage thinking. At least 2-3 HEART dimensions are addressed: e.g., Task Success via acceptance criteria, Adoption via onboarding plan, Retention via engagement metrics. Specific adoption metrics with targets are included. Migration from existing tools is acknowledged with a basic plan. |
| **5** | The PRD includes a golden path strategy, progressive rollout across teams, migration guides, rollback plan, and developer satisfaction measurement. All five HEART dimensions are covered with goals, signals, and metrics. Time-to-first-value is defined. The risk of engineers reverting to old workarounds is identified with mitigation. Onboarding is designed for different user segments (per the adoption curve). The PRD bridges discovery and delivery with a clear plan for driving organic adoption through demonstrated value, not mandates. |

---

### 5. clarity_and_precision

**What it measures**: Is the language specific, actionable, and free of vague or unmeasurable terms?

| Score | Criteria |
|-------|----------|
| **1** | The document is filled with vague language ("should be fast", "user-friendly", "scalable", "as needed"). Requirements are opinions, not specifications. |
| **2** | Some sections use precise language, but vague terms appear frequently in critical areas (requirements, acceptance criteria, success metrics). Measurable thresholds are rare. |
| **3** | Most language is clear. Vague terms appear occasionally but not in acceptance criteria or success metrics. Requirements are generally actionable, though some could be more specific. |
| **4** | Language is consistently precise. Requirements use measurable terms (response times in ms, percentage thresholds, specific user actions). Rare instances of imprecision exist but do not affect testability. |
| **5** | Every requirement, metric, and criterion is expressed in specific, measurable, unambiguous language. Performance targets include numbers. User actions are described step-by-step. There are no weasel words, no "etc.", no "various", no "appropriate" without definition. The document could be implemented by a team with no additional clarification. |
