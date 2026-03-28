# Journey Map Evaluation Rubric

**Artifact type**: `journey`
**Rubric name**: `rubric-journey`

Use this rubric with the judge prompt to evaluate user journey maps.

---

## Dimensions

### 1. completeness

**What it measures**: Does the journey cover all relevant stages from awareness through post-adoption? Are all columns filled (actions, touchpoints, thoughts, pain points, opportunities)?

| Score | Criteria |
|-------|----------|
| **1** | Fewer than three adoption stages are covered. Multiple columns are empty or contain placeholder text. The journey reads as a fragment, not a complete map. No persona context or emotional arc is provided. |
| **2** | Most adoption stages are listed but coverage is uneven — some stages have detailed entries while others are stubs with generic content (e.g., "user feels frustrated" with no specifics). One or more columns (touchpoints, opportunities) are consistently thin across all stages. Persona context is present but shallow. |
| **3** | All five adoption stages (Discovery, Evaluation, First Use, Integration, Mastery) are present. Every column has content for every stage, though some entries are generic rather than specific to this persona and product. Moments of truth are identified but may lack depth. Improvement recommendations exist but not for every pain point. |
| **4** | All five stages are thoroughly covered with specific, differentiated content in every column. Moments of truth are well-defined with evidence. Improvement recommendations exist for most pain points. Emotional arc is mapped. Minor gaps remain — for example, the interview evidence index may be incomplete, or one stage has noticeably less detail than others. |
| **5** | Every stage has rich, specific content across all columns. No empty or generic cells. Moments of truth are compelling and well-evidenced. Every pain point has a corresponding improvement recommendation with impact and complexity assessment. Emotional arc is clearly depicted with explanations for sentiment shifts. The interview evidence index is complete with quotes for every stage. The journey could be handed to a design team as a complete brief. |

---

### 2. evidence_grounding

**What it measures**: Are stages informed by actual interview data and insights? Are specific quotes and observations referenced?

| Score | Criteria |
|-------|----------|
| **1** | No interview or insight references anywhere in the journey. Content appears entirely assumed or fabricated. The `linked_interviews` frontmatter field is empty or the listed IDs are never referenced in the body. |
| **2** | Interview IDs appear in the frontmatter and are mentioned in passing, but no specific quotes, observations, or behavioral data are cited. The journey reads as if it could have been written without reading the interviews. |
| **3** | Some stages include references to specific interviews or insights. At least 2-3 direct user quotes are included. However, evidence is concentrated in one or two stages while others lack any citations. The connection between evidence and journey content is implicit rather than explicit. |
| **4** | Most stages cite specific interview data — quotes, observed behaviors, or stated frustrations. The interview evidence index connects each stage to source data. Insights are referenced by ID. The journey clearly could not have been written without the research. A few stages or claims still lack direct evidence. |
| **5** | Every stage is grounded in specific, cited evidence. Direct quotes from interviews are included for each stage. Behavioral observations (not just stated opinions) are referenced. The interview evidence index is complete and accurate. Pain points and moments of truth are backed by multiple data points. The journey serves as an auditable chain from raw interviews through to design implications. |

---

### 3. emotional_mapping

**What it measures**: Is the emotional arc clearly depicted? Does it use empathy map dimensions (Think & Feel, Pain, Gain)? Are moments of truth identified?

| Score | Criteria |
|-------|----------|
| **1** | No emotional dimension is present. The journey lists actions and touchpoints but ignores what the user thinks, feels, or experiences emotionally. No moments of truth are identified. |
| **2** | A Think & Feel column exists but contains only surface-level or generic entries ("user is happy", "user is frustrated") without connection to specific evidence or empathy map dimensions. No emotional arc is plotted across stages. Moments of truth are absent or vaguely described. |
| **3** | The Think & Feel column includes specific emotions tied to each stage. The emotional arc section exists and labels each stage as positive, neutral, or negative. At least one empathy map dimension beyond Think & Feel is referenced (e.g., what the user hears from peers, what they see in their environment). 2-3 moments of truth are identified. However, the emotional narrative lacks depth — it describes states rather than explaining transitions. |
| **4** | Emotional mapping draws explicitly from multiple empathy map quadrants: Think & Feel, Hear, See, Say & Do, Pain, and Gain. The emotional arc describes not just the state at each stage but why sentiment shifts between stages. Moments of truth (3-5) are well-defined with evidence and risk assessment. The emotional journey is specific to this persona, not generic. |
| **5** | The emotional arc is a compelling narrative grounded in evidence. All empathy map quadrants are reflected in the journey. Contradictions between what users say and what they do are surfaced (the Say & Do gap). Moments of truth are precisely identified with specific quotes, current vs. desired outcomes, and risk levels. The emotional mapping reveals non-obvious insights — for example, a stage that appears positive on the surface but masks underlying anxiety. Captures developer-specific emotional dimensions: trust in tool reliability, confidence in using it correctly, frustration with cognitive overhead, satisfaction from reduced toil. The emotional dimension would inform design priorities if handed to a product team. |

---

### 4. actionability

**What it measures**: Does each pain point have a corresponding improvement suggestion? Are opportunities specific and implementable?

| Score | Criteria |
|-------|----------|
| **1** | Pain points are listed but no improvement suggestions are provided. The journey identifies problems without proposing solutions. The Opportunities column in the journey table is empty or contains vague platitudes ("improve the experience"). |
| **2** | Some improvement suggestions exist but they are generic and not tied to specific pain points (e.g., "make it easier to use", "improve onboarding"). No assessment of impact or implementation complexity. Many pain points have no corresponding recommendation. |
| **3** | Most pain points have improvement suggestions. Suggestions are more specific (e.g., "add a CLI --dry-run flag during first use") but lack prioritization or impact assessment. Some suggestions are adoption-aware (mentioning onboarding, progressive disclosure) but this is inconsistent. The recommendations table is present but incomplete. |
| **4** | Every pain point has a corresponding, specific improvement recommendation. Recommendations include expected impact and implementation complexity. Suggestions are differentiated by adoption stage — onboarding improvements for Trial, power-user features for Adoption. Friction points are ordered by severity. The recommendations could be used as input to a product backlog. |
| **5** | Every pain point and friction point has a specific, actionable recommendation with impact and complexity assessment. Recommendations are clearly adoption-stage-aware: interactive tutorials and example commands for First Use users, aliases, config files, and power-user workflows for Mastery users, value demonstration for Evaluation users. Recommendations are prioritized and could be directly translated into user stories or design tickets. Drop-off risks are quantified where analytics data exists. The improvement section alone would be valuable as a standalone planning artifact. |

---

### 5. persona_fit

**What it measures**: Is the journey tailored to a specific persona with clear JTBD context? Does it account for their adoption curve segment?

| Score | Criteria |
|-------|----------|
| **1** | No persona is defined or the persona is a generic placeholder ("the user"). No JTBD is articulated. The journey could apply to anyone and therefore applies to no one. |
| **2** | A persona is named in the frontmatter but the journey content does not reflect their specific characteristics. The JTBD is absent or vague. The adoption curve segment is not identified. The journey stages read the same regardless of who the persona is. |
| **3** | The persona section includes a name, role, and goals. A JTBD is articulated but may be generic. The adoption curve segment is identified (e.g., "Early Majority") but not justified with evidence. Some journey content reflects the persona's specific context, but other parts are generic enough to apply to any user. The Problem Statement template is partially filled. |
| **4** | The persona is well-defined with specific goals, pain points, and behavioral context drawn from interviews. The JTBD is clear and specific. The adoption curve segment is identified and justified with evidence from interviews. The Problem Statement template is fully completed. Most journey content is clearly tailored to this specific persona — different personas would produce a noticeably different journey. |
| **5** | The persona is vivid and evidence-based. The JTBD is specific, well-framed, and grounded in research. The adoption curve segment is justified with multiple data points. The Problem Statement template captures the persona's situation, barriers, and emotional impact with specificity. Every stage of the journey reflects this persona's unique context — their technical sophistication, their organizational role, their specific workflow, and their emotional disposition. It is impossible to read this journey and not know exactly who it was written for. The journey accounts for where this persona sits on the adoption curve and adjusts expectations accordingly (e.g., an Early Majority user needs more proof at the Evaluation stage than an Early Adopter). |
