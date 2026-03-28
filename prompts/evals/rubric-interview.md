# Interview Analysis Evaluation Rubric

**Artifact type**: `insight` (derived from interviews)
**Rubric name**: `rubric-interview`

Use this rubric with the judge prompt to evaluate interview analysis insights — the artifacts produced when raw interview transcripts are analyzed for themes, pain points, and opportunities.

---

## Dimensions

### 1. theme_extraction

**What it measures**: Are themes clearly identified, specific (not generic), and supported by evidence?

Themes should emerge from the data, not be imposed. Generic themes like "users want a better experience" add no value. Strong themes are named precisely and grounded in observed patterns.

| Score | Criteria |
|-------|----------|
| **1** | No themes are identified, or themes are so generic they could apply to any product (e.g., "usability", "performance", "communication"). |
| **2** | Themes are listed but are broad and unsupported. No quotes, no behavioral evidence, no indication of how many interviewees surfaced each theme. Themes read as assumptions rather than findings. |
| **3** | Themes are reasonably specific (e.g., "CI pipeline friction compounds across the inner loop" rather than just "usability"). Some evidence is provided but not consistently — some themes have supporting quotes while others do not. |
| **4** | Themes are specific and descriptive. Each theme is supported by at least one piece of evidence (quote, behavioral observation, or data point). The analysis distinguishes between primary and secondary themes. |
| **5** | Themes are sharply defined, mutually distinct, and ordered by prevalence or impact. Every theme is supported by multiple pieces of evidence across interviewees. Counter-evidence or outliers are noted. The theme names themselves are informative (e.g., "Onboarding paradox: self-service was revoked because guardrails weren't built first"). |

---

### 2. pain_point_depth

**What it measures**: Are pain points described with context, frequency, severity, and user quotes?

Following the Data Detective Framework: numbers without narrative are blind, narrative without numbers are anecdotal. Pain points need both dimensions. For DevEx, "numbers" means engineering metrics (build times, cycle times, incident counts) not revenue/conversion metrics.

| Score | Criteria |
|-------|----------|
| **1** | No pain points are identified, or pain points are stated without any supporting detail (e.g., a bare list: "onboarding is hard, navigation is confusing"). |
| **2** | Pain points are described but lack context. No indication of frequency (how many users mentioned it), severity (how much it blocks the user), or direct quotes. Pain points read as the analyst's interpretation rather than the user's experience. |
| **3** | Pain points include some context — either frequency or severity or quotes, but not all three. The reader understands what hurts but not how badly or how often. Some pain points are well-documented while others are thin. |
| **4** | Most pain points include frequency indicators (e.g., "mentioned by 4 of 6 interviewees"), severity context (e.g., "causes users to abandon the flow"), and at least one direct quote. The emotional dimension is acknowledged. |
| **5** | Every pain point is documented with: who experiences it (persona or segment), how often it was mentioned, how severe the impact is (with behavioral evidence), at least one verbatim quote, and the emotional response (confusion, frustration, anxiety, etc.). Pain points are prioritized by a combination of frequency and severity. The analysis connects behavioral observations ("what users do") to emotional insights ("how users feel"), following the Read-Relate pattern. |

---

### 3. jtbd_framing

**What it measures**: Are findings framed as jobs-to-be-done (functional, emotional, social)?

The JTBD framework focuses on what users are trying to accomplish rather than what they say they want. Strong analysis identifies the underlying job, not just the surface request.

| Score | Criteria |
|-------|----------|
| **1** | No JTBD framing. Findings are presented as feature requests or problem statements without identifying the underlying user job. |
| **2** | Jobs are implied but not explicitly stated. The analysis describes what users struggle with but not what they are trying to achieve. No distinction between functional, emotional, and social jobs. |
| **3** | At least one job is explicitly framed using JTBD language (e.g., "When [situation], I want to [motivation], so I can [outcome]"). The functional job is identified but emotional and social dimensions are missing. |
| **4** | Multiple jobs are identified and explicitly framed. The analysis distinguishes between functional jobs (what the user needs to accomplish), emotional jobs (how the user wants to feel), and at least acknowledges the social dimension. Jobs are connected to specific interview evidence. |
| **5** | Jobs are comprehensively mapped across functional, emotional, and social dimensions. Each job is framed with situation-motivation-outcome structure and linked to specific interviewee statements. The analysis identifies importance and satisfaction gaps (where the job matters most but current solutions fail). Jobs are prioritized by opportunity score or similar framework. The framing enables direct translation into product requirements. |

---

### 4. confidence_calibration

**What it measures**: Is the confidence rating justified and consistent with the evidence strength?

Every insight has a confidence field (low, medium, high). This dimension checks whether that rating is honest and well-reasoned, not inflated.

| Score | Criteria |
|-------|----------|
| **1** | No confidence rating is provided, or the rating is present with no justification. |
| **2** | A confidence rating is assigned but contradicts the evidence. For example, "high confidence" based on a single interview, or "low confidence" despite strong multi-source evidence. No explanation of how confidence was determined. |
| **3** | The confidence rating is present and roughly appropriate. A brief justification is given (e.g., "medium confidence — based on 3 interviews"). The reasoning is thin but not contradictory. |
| **4** | The confidence rating is well-justified. The analysis explains what evidence supports the rating and what would change it (e.g., "medium confidence: consistent across 4 interviews but all from the same user segment; would increase to high with cross-segment validation"). Limitations are acknowledged. |
| **5** | Confidence is precisely calibrated with explicit criteria. The analysis states: number of supporting sources, diversity of sources (segments, roles, contexts), consistency of the signal, and what contradictory evidence exists. The insight identifies specific next steps to increase confidence (e.g., "validate with quantitative data from cohort X" or "test with late-majority users"). The rating demonstrates intellectual honesty — high confidence is reserved for strong, multi-source, cross-segment evidence. |

---

### 5. actionability

**What it measures**: Does the insight suggest clear next steps — further research, PRD candidates, or experiments?

An insight that does not lead to action is trivia. This dimension evaluates whether the analysis bridges observation to recommendation, following the Recommend step of the Data Detective Framework.

| Score | Criteria |
|-------|----------|
| **1** | No next steps or recommendations are provided. The analysis ends with findings and leaves the reader to figure out implications. |
| **2** | Next steps are mentioned but are vague (e.g., "we should look into this further" or "consider improving the onboarding flow"). No specificity about what to do, who should do it, or how to validate. |
| **3** | At least one concrete next step is provided (e.g., "create a PRD for flaky test quarantine system" or "run 3 additional interviews with new joiners"). The recommendation is reasonable but lacks a hypothesis or success criteria. |
| **4** | Multiple next steps are provided and categorized (e.g., further research needed, ready for PRD, experiment candidates). Recommendations include a hypothesis structure: "If we [action], then [expected outcome], because [evidence from this analysis]." Priority is indicated. |
| **5** | Next steps are specific, prioritized, and tied to evidence. Each recommendation includes: the proposed action, a testable hypothesis, success metrics, and the evidence basis. The analysis distinguishes between what can be acted on now versus what needs further validation. Recommendations reference specific artifact types to create next (PRD, experiment, additional interviews). The path from insight to product decision is clear and auditable. |
