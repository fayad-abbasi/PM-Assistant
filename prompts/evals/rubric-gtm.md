# GTM Draft Evaluation Rubric

**Artifact type**: `gtm`
**Rubric name**: `rubric-gtm`

Use this rubric with the judge prompt to evaluate Go-to-Market draft messaging documents.

---

## Dimensions

### 1. audience_fit

**What it measures**: Is the tone, language, and framing appropriate for the target audience? Would it resonate with the intended reader?

Each audience has distinct expectations:
- **Developer** (IC Engineer): Technical, precise, show-don't-tell. Includes code examples, CLI commands, integration steps. No corporate speak.
- **Engineering Manager**: Team impact focused — productivity gains, reduced toil, team satisfaction. Concrete metrics their team will see.
- **Tech Lead / Architect**: Architecture fit, migration path, backward compatibility, extensibility. Technical depth with system-level thinking.
- **Engineering Leadership** (VP/Director): Strategic alignment, org-wide ROI, headcount efficiency, competitive positioning for talent. Scannable in 2 minutes.
- **Executive** (general): Business impact, budget justification, risk posture. High-level, decision-oriented.
- **Compliance**: Thorough, risk-aware, regulatory. Documents data flows and gaps. No downplaying of risk.
- **Finance**: Quantitative, ROI-focused, conservative. Tables and numbers over prose. Includes scenarios.

| Score | Criteria |
|-------|----------|
| **1** | The messaging reads as generic product copy with no audience adaptation. A developer brief reads like a press release. An executive brief is buried in technical details. The audience would dismiss it immediately. |
| **2** | Some audience awareness is present, but the framing is inconsistent. A developer brief mentions APIs but wraps them in marketing language. An executive brief includes ROI but also lengthy technical architecture sections. The document tries to serve multiple audiences. |
| **3** | The tone is mostly appropriate for the audience. A developer brief is technical; an executive brief is strategic. However, there are lapses — a developer brief uses phrases like "unlock value" or an executive brief includes unnecessary implementation details. The core framing is right but the execution is uneven. |
| **4** | The messaging is well-tailored to the audience throughout. Tone, vocabulary, level of detail, and framing are consistently appropriate. A developer would find it credible; an executive would find it actionable. Minor misalignments exist but do not undermine the overall quality. |
| **5** | The messaging is precisely calibrated to the audience. Every section serves the reader's specific decision-making needs. A developer brief includes working code examples and integration details. An executive brief is scannable in 2 minutes with a clear decision point. A compliance brief surfaces every regulatory implication. A finance brief has scenario-modeled projections. The reader would feel this was written by someone who understands their role. |

---

### 2. prd_fidelity

**What it measures**: Does the messaging accurately represent the product as defined in the PRD? No overclaiming or underclaiming?

| Score | Criteria |
|-------|----------|
| **1** | The messaging describes a product that does not match the PRD. Features are invented, capabilities are fabricated, or the scope is dramatically misrepresented. The reader would form an inaccurate understanding of the product. |
| **2** | The messaging is loosely based on the PRD but takes significant liberties. Key features are exaggerated ("real-time" when the PRD specifies batch processing) or important limitations are omitted. Some claims cannot be traced back to the PRD. |
| **3** | The messaging is generally accurate. Core features and capabilities align with the PRD. However, some details are imprecise — metrics are rounded aggressively, timelines are vague where the PRD is specific, or non-functional requirements (performance, scale) are overstated. |
| **4** | The messaging faithfully represents the PRD. Features, capabilities, limitations, and timelines are accurately conveyed. Claims are traceable to specific PRD sections. Minor omissions exist (e.g., a secondary feature is not mentioned) but nothing is misrepresented. |
| **5** | The messaging is a precise translation of the PRD for the target audience. Every claim maps to a specific PRD section. Limitations and risks are honestly represented, not hidden. Metrics and targets match the PRD's success criteria. The reader could cross-reference the messaging against the PRD and find no discrepancies. |

---

### 3. adoption_awareness

**What it measures**: Does the messaging address the right adoption curve segment? Does it consider the adoption stages (Awareness, Interest, Evaluation, Trial, Adoption)?

| Score | Criteria |
|-------|----------|
| **1** | No consideration of adoption dynamics. The messaging assumes the reader is already convinced and ready to use the platform tool. There is no awareness-building, no evaluation support, and no path from interest to trial. The adoption curve is not referenced or considered. |
| **2** | Minimal adoption awareness. The messaging mentions a target audience but does not consider where they are in the adoption journey. A developer brief lists features but does not explain how to get started. An engineering leadership brief describes benefits but not how adoption will unfold across teams over time. |
| **3** | Basic adoption awareness is present. The messaging considers one or two adoption stages (e.g., it builds awareness and interest but does not support evaluation or trial). The adoption curve segment is implied but not explicitly addressed. There is a call to action but it is generic. The risk of abandonment of the platform tool in favor of old workarounds is not addressed. |
| **4** | Good adoption awareness. The messaging addresses the target adoption curve segment (Innovators, Early Adopters, etc.) and guides the reader through multiple adoption stages. A developer brief includes a "Getting Started" path (Trial). An engineering leadership brief frames the timeline around adoption milestones. Adoption-specific concerns for the target segment are addressed. The risk of engineers reverting to old tools is acknowledged. |
| **5** | Sophisticated adoption awareness. The messaging is deliberately designed for a specific adoption curve segment with tailored appeals: Innovators get early access and extensibility hooks; Early Adopters get proof of scale and reliability. The messaging maps to the full funnel (Awareness through Adoption) with stage-appropriate content. Continuous onboarding is considered. Chasm-crossing strategy is referenced where relevant. The messaging addresses the risk of mandated adoption creating resentment versus organic adoption through demonstrated value. The messaging would accelerate the reader's movement through the adoption stages. |

---

### 4. clarity_and_persuasion

**What it measures**: Is the message clear, compelling, and actionable? Does it include a call to action or decision point?

| Score | Criteria |
|-------|----------|
| **1** | The messaging is confusing, disorganized, or contradictory. The reader cannot determine what the product does, why it matters, or what they should do next. Key points are buried or missing. |
| **2** | The messaging conveys basic information but is not persuasive. It reads as a feature list or data dump without a narrative thread. There is no clear call to action. The reader understands what the product is but not why they should care or what to do about it. |
| **3** | The messaging is clear and logically structured. The reader can follow the argument from problem to solution to benefit. A call to action exists but is weak or buried. The messaging informs but does not compel. |
| **4** | The messaging is clear, well-structured, and persuasive. The narrative flows logically and builds a compelling case. Evidence supports claims. The call to action is specific and prominent. The reader knows exactly what to do next and has reason to act. |
| **5** | The messaging is exceptionally clear and compelling. It anticipates the reader's objections and addresses them proactively. The narrative arc is tight: problem, evidence, solution, proof, action. Every sentence earns its place. The call to action is impossible to miss and creates appropriate urgency. The reader feels informed, convinced, and ready to act. |

---

### 5. completeness

**What it measures**: Are all required sections for that audience type present and substantive?

Required sections by audience:
- **Developer** (IC Engineer): Problem, Solution, How It Works, Integration Guide, Getting Started, Adoption Curve Considerations, FAQ
- **Engineering Manager**: Executive Summary, Team Impact Analysis, Adoption Timeline, Migration Plan for Teams, Success Metrics, Decision Required
- **Tech Lead / Architect**: Architecture Overview, Integration Guide, Migration Path, Backward Compatibility, Performance Characteristics, Extensibility, FAQ
- **Engineering Leadership** (VP/Director): Strategic Summary, Org-Wide Impact, ROI/Headcount Analysis, Risk Assessment, Adoption Roadmap, Decision Required
- **Executive** (general): Executive Summary, Key Benefits, Strategic Fit, ROI/Impact, Timeline, Decision Required
- **Compliance**: Change Summary, Regulatory Impact Assessment, Data Handling Changes, Risk Assessment, Audit Trail & Monitoring, Compliance Checklist, Approval Workflow
- **Finance**: Investment Summary, Cost Breakdown, Revenue/Savings Impact, ROI Analysis, Risk-Adjusted Projections, Sensitivity Analysis, Funding Request

| Score | Criteria |
|-------|----------|
| **1** | Fewer than half of the required sections are present. The document is a stub or incomplete draft. Critical sections for the audience are missing entirely. |
| **2** | Most sections are listed but several are stubs, contain only a sentence or two, or use placeholder text ("TBD", "to be determined"). The document has the right structure but lacks substance. |
| **3** | All required sections are present. Most have meaningful content, but 1-2 sections are thin — for example, an FAQ with only 2 questions, a risk assessment with a single risk, or a cost breakdown missing OPEX. Functional as a first draft. |
| **4** | All sections are present with substantive content. Each section addresses its purpose with specific details derived from the PRD. Minor gaps remain — for example, a sensitivity analysis covers 2 variables instead of 3-5, or the compliance checklist is present but not pre-populated with PRD-specific items. |
| **5** | Every required section is thorough and audience-appropriate. Content is specific, not generic. Tables are populated with real data from the PRD. Checklists are customized. Code examples compile (developer). Scenarios have distinct assumptions (finance). Regulatory frameworks are identified and assessed (compliance). No section reads as boilerplate. |
