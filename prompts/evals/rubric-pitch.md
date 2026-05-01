# Pitch Evaluation Rubric

**Artifact type**: `pitch`
**Rubric name**: `rubric-pitch`

Use this rubric with the judge prompt to evaluate Shape Up pitches. A pitch is **not** a PRD — do not penalize a pitch for lacking user stories, functional requirements, Given/When/Then criteria, or HEART metrics. Those belong in PRDs. A good pitch is **rough, solved, and bounded**, presenting a credible bet at the right level of abstraction.

Methodology reference: `background_information/ShapeUp/shape-up-skill.md`.

---

## Dimensions

### 1. problem_grounding

**What it measures**: Is the problem articulated as a specific story with evidence from real users, not as a generic claim?

A pitch with no concrete problem cannot be evaluated for fit — debates devolve into aesthetic preference. The pitch must establish a clear baseline: what specifically breaks in the user's current workflow, and why does that matter now?

| Score | Criteria |
|-------|----------|
| **1** | No problem stated, or stated only as "we should build X." No baseline of current user behavior. No evidence. The pitch is solution-first. |
| **2** | A problem is named in general terms ("users struggle with onboarding") but no specific story, no quotes, no observed behavior. `linked_insights` may be present but the body doesn't draw on them. |
| **3** | A specific scenario is described and at least one insight is referenced, but the linkage is weak — the problem could exist without the cited evidence supporting it specifically. |
| **4** | A specific user story illustrates the failure mode of the status quo. At least one direct quote or behavioral observation from a linked insight grounds the problem. The reader can picture the user. |
| **5** | The problem is anchored in a concrete, named scenario with a direct quote AND the pitch explains *why now* — what makes this baseline insufficient at this moment. The reader can both visualize the user and predict who else hits this. Multiple insights converge. |

---

### 2. appetite_fit

**What it measures**: Is the appetite explicit, justified, and matched to the scope of the proposed solution?

Appetite is the foundational shaping discipline: time is fixed, scope is variable. A pitch that names a small-batch appetite while sketching a six-week solution has miscalibrated. A pitch that names appetite vaguely ("a few weeks") gives the betting table no real constraint.

| Score | Criteria |
|-------|----------|
| **1** | No appetite stated, or stated as "however long it takes." No team-size context. |
| **2** | Appetite is named (small-batch / big-batch) but with no rationale, no team configuration, and the scope appears mismatched (e.g., big-batch labeled but only 2 elements, or small-batch labeled but 12+ elements with deep complexity). |
| **3** | Appetite and team size are stated. Scope roughly fits, though a careful reader could plausibly question whether it's achievable. |
| **4** | Appetite is explicit (small-batch or big-batch), team configuration is named (e.g., "1 designer + 2 programmers"), and the proposed elements credibly fit within that envelope. The pitch acknowledges what would happen if it doesn't fit ("if X is harder than expected, we cut Y"). |
| **5** | Appetite, team config, and scope fit are clearly justified. The pitch explicitly reasons about *why* this is worth this much time relative to other things — the pitch defends the appetite, not just states it. Trade-offs are pre-identified: "if rabbit hole Z opens, we'd cut W and ship a still-meaningful version." |

---

### 3. solution_abstraction_level

**What it measures**: Is the solution at the right level of abstraction — rough enough to leave team latitude, solved enough to give clear direction, bounded enough to constrain scope?

This is the hardest pitch dimension to get right. Wireframes are too concrete (lock in details, kill team creativity). Words alone are too abstract (no fitness test, projects grow without bound). The sweet spot is breadboards or fat marker sketches with explicit elements.

| Score | Criteria |
|-------|----------|
| **1** | Solution is either pure prose with no elements ("build a calendar view") OR fully-specified wireframes/mockups with pixel-level detail. Either too abstract or too concrete. |
| **2** | Some elements are listed but key affordances or connections are missing. OR specific UI components are named (dropdowns, modals, specific icons) when they shouldn't be. The shape of the work is unclear. |
| **3** | A breadboard or sketch is present with most elements identified. Connections are mostly clear. Some details are over-specified (a particular component is named) or under-specified (a key flow is glossed over). |
| **4** | A clean breadboard or fat marker sketch with all major elements and connections. Affordances are described functionally, not visually. The build team has clear direction without being boxed in. Any embedded sketches include a "designer has latitude" note where appropriate. |
| **5** | The solution achieves the rough/solved/bounded triad. Elements are listed concisely (≤10), connections are explicit, no pixel-level commitments, but every key flow is walkable. A senior designer reading this would know exactly where their judgment is wanted and where the boundaries are. The shaping is visible without being prescriptive. |

---

### 4. rabbit_holes_patched

**What it measures**: Are known risks and unknowns explicitly identified and resolved with concrete patch decisions?

The shaping track's primary value is killing rabbit holes before the cycle starts. An unpatched rabbit hole is uncertainty handed to a deadline-bound team — the leading cause of cycle overruns. Pitches must show the rabbit holes the shapers found AND the decisions that closed them.

| Score | Criteria |
|-------|----------|
| **1** | No rabbit holes section, or it says "we'll figure it out during the cycle." Implicit handoff of uncertainty to the build team. |
| **2** | Risks are named but not patched ("auth might be tricky" — without a decision). The team is told what's hard but not what to do about it. |
| **3** | At least one rabbit hole is named with a patch decision, but other obvious risks are not addressed. A reader familiar with the area could name 2–3 risks the pitch missed. |
| **4** | Most foreseeable rabbit holes are named with concrete patch decisions ("for v1, we don't support custom domains"). Each patch is a clear constraint the build team can implement. |
| **5** | All identifiable rabbit holes are patched with specific, defensible decisions. Patches are surprising in places — the pitch made hard calls that the build team would have agonized over mid-cycle (e.g., "completed to-dos render exactly as today, with the group name appended — slightly messy but eliminates the design rabbit hole"). The pitch demonstrably did the work that prevents the build team from getting stuck. |

---

### 5. boundaries_clarity

**What it measures**: Are the no-gos explicit, and is what's NOT being built unambiguously listed?

Scope creep is caused by what's not said. A pitch with no explicit out-of-scope list is a pitch where everyone who reads it brings their own assumptions about scope — and those assumptions diverge.

| Score | Criteria |
|-------|----------|
| **1** | No no-gos section. The reader cannot tell what's excluded. |
| **2** | A no-gos section exists but is vague ("we're not boiling the ocean") or lists obvious non-things. Doesn't constrain scope. |
| **3** | At least 1 specific no-go is listed with a brief reason. Some adjacent areas that *could* be in scope are still ambiguous. |
| **4** | At least 2 specific no-gos with reasons. The reader has a clear picture of what's outside the bet, including some non-obvious exclusions that show the shaper considered them. |
| **5** | No-gos are sharp and pre-empt the most likely scope-creep vectors. They name *concrete adjacent features* that someone might assume are included and explicitly exclude them with one-line reasons. After reading the pitch, two stakeholders would not disagree about what's in or out. |

---

## Notes for the Judge

- A short pitch is not necessarily a low-scoring pitch. Pitches in the 1–3 page range can score 5 across all dimensions. Length is not a quality signal.
- Do not penalize a pitch for lacking PRD-style content. Items like user stories, Given/When/Then acceptance criteria, HEART metrics, or detailed personas should be **absent** from a pitch. Their presence indicates the pitch has drifted into PRD territory and may warrant a lower `solution_abstraction_level` score.
- The pitch is meant to invite engagement, not foreclose it. Over-polished pitches that signal "decisions are locked" should not score 5 on `solution_abstraction_level` even if every element is named — the roughness is the feature.
