# `/simulate` Command — Proposal

## Problem

When facing a product decision (add a workflow step, change a feature, adjust a process), there's no structured way to think through how that decision might play out. We lack forward-looking decision exploration in the PM Assistant workflow.

This gap also extends to **build-vs-buy decisions** — a recurring task for any PM managing a platform or tooling portfolio. Evaluating vendor options against building in-house requires structured analysis across cost, risk, DX, and strategic fit dimensions that differ from standard product decisions.

## What `/simulate` Does

You describe a product decision, and it systematically explores how it plays out across multiple dimensions — producing a scored scenario artifact that links into the existing traceability chain (PRDs, OKRs, insights). The dimensions adapt based on the **product family** selected.

---

## The 10-Dimension Decision Analysis Framework

Every product decision gets analyzed through these lenses (default "General" family):

| # | Dimension | Core Question |
|---|-----------|---------------|
| 1 | **Frequency** | Should this happen every time, periodically, or on-demand? |
| 2 | **Exceptions** | What edge cases or exceptions exist? |
| 3 | **Role-based** | Does this vary by user role or persona? |
| 4 | **Parallelization** | Can this run in parallel with other activities? |
| 5 | **Feature flags** | Should this be gated for incremental rollout? |
| 6 | **Metrics & experimentation** | What to measure and how to test? |
| 7 | **Compliance & risk** | Regulatory, security, or legal implications? |
| 8 | **Resources** | Effort, cost, dependencies, timeline? |
| 9 | **Assumptions** | What must be true for this to succeed? |
| 10 | **Competitive response** | How might competitors react or how does this compare? |

Each dimension gets a **1-5 favorability score** plus a narrative explanation.

---

## Sub-Actions

The command has 6 modes:

### 1. Create Scenario
**Input**: Describe a decision (e.g., "Add mandatory peer review step before PRD approval")
**Output**: Full dimension analysis saved as a scenario artifact in `data/strategy/scenarios/`

### 2. Compare Scenarios
**Input**: Two or more existing scenario IDs
**Output**: Side-by-side comparison with dimension-by-dimension deltas and an ASCII radar chart

### 3. Sensitivity Analysis
**Input**: An existing scenario + "What if assumption X is wrong?"
**Output**: Re-scored dimensions showing how the picture changes

### 4. Recommend
**Input**: Compared scenarios
**Output**: Final recommendation with rationale, risks, and suggested next steps

### 5. List Scenarios
**Input**: Optional filters (date, tags, status)
**Output**: Table of existing scenarios

### 6. Promote to PRD
**Input**: A scenario ID
**Output**: Converts the chosen scenario into a draft PRD, pre-filling linked context (insights, OKRs, assumptions become acceptance criteria)

---

## Scenario Artifact

Each scenario is saved as a Markdown file with YAML frontmatter:

```yaml
id: scenario-{date}-{NNN}
title: "Add peer review gate to PRD workflow"
decision: "Require peer review before PRD status can move to 'approved'"
family: general | build-vs-buy | internal-tooling | customer-facing | platform-api | compliance-driven
status: draft | compared | promoted
linked_prds: [prd-2026-03-10-001]
okr_ids: [okr-2026-q1-001]
tags: [simulation, scenario-analysis]
created_at: 2026-03-13T10:00:00Z
```

**Body sections**:
- Decision Context
- One section per dimension (score + narrative)
- Summary: overall assessment, go/no-go lean, key risks, recommended next steps

---

## Quality Gate

After generating a scenario, it auto-runs a self-eval against a rubric (same pattern as `/prd` and `/discover`):

| Rubric Dimension | What It Checks |
|-----------------|----------------|
| Completeness | All applicable dimensions addressed with substance |
| Specificity | Concrete details, not generic platitudes |
| Assumption clarity | Assumptions explicitly stated and testable |
| Actionability | Clear next steps and decision criteria |
| Traceability | Linked to existing PRDs/OKRs/insights |

**Threshold**: 3.5/5. Below threshold triggers auto-fix (max 2 iterations).

---

## Integration Points

| Existing Command | Integration |
|-----------------|-------------|
| `/prd` | Suggest "Run `/simulate` first?" when creating a PRD for a significant decision |
| `/strategy` | Add `/simulate` as a next-step suggestion after OKR/roadmap work |
| `/next` | Flag draft scenarios not yet compared as low-priority items |
| `/pm-dash` | Show scenario count and status breakdown |
| `/eval` | Support scenario artifacts with the scenario rubric |

---

## Example Usage

### General Product Decision

```
You: /simulate
Claude: What decision would you like to explore?
You: Adding a mandatory data privacy review step before any PRD can move to "approved" status

Claude: What product family does this fall under?
  1. General (all 10 dimensions)
  2. Build vs Buy (vendor evaluation — 10 dimensions)
  3. Internal Tooling (8 dimensions — skips feature flags, competitive)
  4. Customer-Facing (13 dimensions)
  5. Platform/API (13 dimensions)
  6. Compliance-Driven (12 dimensions)
  Or describe a custom set.

You: 1

Claude generates a full 10-dimension analysis:
- Frequency: Every time (score: 4/5) — privacy review should gate all PRDs
- Exceptions: Internal-only tools with no PII could skip (score: 3/5)
- Role-based: Legal/compliance team owns the review (score: 4/5)
- Parallelization: Can run alongside UAT prep (score: 5/5)
- Feature flags: Start with high-priority PRDs only (score: 4/5)
- Metrics: Track review cycle time, rejection rate (score: 4/5)
- Compliance: Strong alignment with GDPR/CCPA requirements (score: 5/5)
- Resources: Need 0.5 FTE from legal team (score: 2/5)
- Assumptions: Legal team has capacity; review template exists (score: 3/5)
- Competitive: Industry moving this direction anyway (score: 4/5)

Overall: 38/50 — Lean GO with mitigation for resource constraint

Lowest scores: Resources (2/5), Exceptions (3/5), Assumptions (3/5)
→ Run `/simulate improve` on any dimension to get actionable guidance.
```

### Build vs Buy Decision

```
You: /simulate
Claude: What decision would you like to explore?
You: We need a secret scanning and detection solution — evaluate build vs buy options

Claude: What product family does this fall under?
You: 2 (Build vs Buy)

Claude: How many options are you evaluating?
You: Three — GitGuardian (SaaS vendor), GitHub Advanced Security (platform add-on),
     and building our own with TruffleHog (open source)

Claude generates a Build vs Buy analysis:

OPTION COMPARISON: Secret Scanning Solution

                    GitGuardian    GHAS    DIY TruffleHog
                    -----------    ----    --------------
TCO (Year 1)           $62K       $54K        $45K
TCO (Year 3)          $174K      $150K       $165K
Implementation Speed    4/5        3/5         2/5
DX & Friction           5/5        4/5         2/5
Coverage Breadth        5/5        3/5         3/5
Vendor Lock-in Risk     2/5        3/5         5/5
Maintenance Burden      5/5        4/5         1/5
Strategic Fit           4/5        3/5         2/5
Compliance Alignment    4/5        3/5         2/5
Scalability             4/5        4/5         3/5

Weighted Score:         8.6        7.2         4.8

RECOMMENDATION: GitGuardian
Rationale: Best detection coverage, fastest time-to-value, lowest
maintenance burden. Premium justified by DX and breadth.

Key risks:
- Vendor dependency (mitigate: contractual data portability clause)
- Cost scales with seat count (mitigate: negotiate multi-year pricing)

Assumptions to validate:
- Security team has capacity for triage workflow setup
- Current GitHub Enterprise plan supports webhook integration

→ Run `/simulate improve` on any dimension
→ Run `/simulate sensitivity` — "What if headcount doubles in 18 months?"
→ Run `/simulate promote` to convert to a PRD
```

---

## Drill-down: `/simulate improve`

After reviewing scores, you can drill into any dimension:

```
You: /simulate improve scenario-2026-03-13-001 exceptions
Claude:

IMPROVE: Exceptions (currently 3/5)

Current state: "Internal-only tools with no PII could skip"
Gap: The exception criteria are vague — what qualifies as "internal-only"?
     No process defined for who decides if an exception applies.

To reach 4/5:
1. Define explicit exception criteria (e.g., "No PII, no external users,
   no third-party data, internal tooling team only")
2. Create a lightweight exception request form (owner, justification,
   data classification)
3. Assign a single approver for exception grants (e.g., Privacy Lead)

To reach 5/5:
4. Automate exception eligibility — tag PRDs with data classification
   at creation, auto-skip review for PRDs tagged "no-PII/internal"
5. Add quarterly audit of granted exceptions to catch drift

Effort: ~2 days to define criteria + form, ~1 sprint to automate
Risk if skipped: Ad-hoc exceptions erode the review gate over time
```

This gives PMs a concrete improvement path for any weak dimension, not just a score.

---

## Product Families

The 10 dimensions are a **general-purpose starting set**. Not every product type needs all 10, and some product types need additional dimensions. Product families define which dimensions apply and which extras to add.

### How It Works

A product family is a JSON profile stored in `data/meta/product-families/`:

```json
{
  "id": "internal-tooling",
  "name": "Internal Tooling",
  "description": "Internal tools used by employees, no external users",
  "dimensions": {
    "include": ["frequency", "exceptions", "role_based", "metrics", "resources", "assumptions"],
    "exclude": ["feature_flags", "competitive_response"],
    "additional": [
      {
        "key": "internal_adoption",
        "name": "Internal Adoption",
        "question": "How will we drive adoption across teams?"
      }
    ]
  }
}
```

### Starter Families

| Family | Drops | Adds |
|--------|-------|------|
| **General** (default) | — | — (all 10 dimensions) |
| **Build vs Buy** | Frequency, Exceptions, Parallelization, Feature flags | TCO Analysis, Implementation Speed, DX & Friction, Coverage/Capability, Vendor Lock-in, Maintenance Burden, Scalability |
| **Internal Tooling** | Feature flags, Competitive response | Internal adoption, Migration path |
| **Customer-Facing** | — | Data privacy, Accessibility, Internationalization |
| **Platform/API** | — | Backwards compatibility, Rate limiting, Developer experience |
| **Compliance-Driven** | Feature flags | Audit trail, Regulatory timeline, Cross-jurisdiction |

### Build vs Buy Family — Deep Dive

The Build vs Buy family replaces generic product dimensions with evaluation-specific ones, because vendor selection has fundamentally different concerns than product design decisions.

**Dimensions (10 total):**

| # | Dimension | Core Question | Scoring Guide |
|---|-----------|---------------|---------------|
| 1 | **TCO Analysis** | What is the total cost of ownership over 1 and 3 years? | 5 = cheapest viable option, 1 = significantly more expensive than alternatives |
| 2 | **Implementation Speed** | How fast can we go from decision to value? | 5 = days/weeks, 1 = quarters |
| 3 | **DX & Friction** | How does this affect the developer experience day-to-day? | 5 = invisible/delightful, 1 = painful/disruptive |
| 4 | **Coverage / Capability** | Does this solve the full problem or just part of it? | 5 = complete coverage, 1 = significant gaps |
| 5 | **Vendor Lock-in Risk** | How hard is it to switch later? | 5 = easy exit (open standards), 1 = deeply locked in |
| 6 | **Maintenance Burden** | Who maintains this and how much effort? | 5 = fully managed, 1 = heavy internal maintenance |
| 7 | **Strategic Fit** | Does this align with our platform direction and team skills? | 5 = natural fit, 1 = misaligned |
| 8 | **Compliance & Risk** | Does this meet regulatory and security requirements? | 5 = exceeds requirements, 1 = gaps that need mitigation |
| 9 | **Scalability** | Will this grow with us (headcount, volume, complexity)? | 5 = scales effortlessly, 1 = will hit limits soon |
| 10 | **Assumptions** | What must be true for this option to succeed? | 5 = few/validated assumptions, 1 = many untested assumptions |

**Output format differences:**
- Generates a **comparison table** across all options (not just one scenario)
- Includes a **weighted score** (user can adjust weights or accept defaults)
- Default weights: TCO 15%, Implementation Speed 15%, DX & Friction 15%, Coverage 15%, Vendor Lock-in 10%, Maintenance 10%, Strategic Fit 5%, Compliance 5%, Scalability 5%, Assumptions 5%
- TCO section includes **Year 1** and **Year 3** cost breakdowns (licensing + implementation + maintenance + hidden costs)
- Summary includes a clear **recommendation** with the top option called out

**Artifact differences:**
- Frontmatter includes `options: [{name, type: vendor|build|hybrid}]` to track what was evaluated
- Body includes an Option Details section before the dimension scoring
- Each dimension scores **per option**, not just overall

### Usage

```
You: /simulate
Claude: What decision would you like to explore?
You: Adding a self-service dashboard for internal ops teams

Claude: What product family does this fall under?
  1. General (all 10 dimensions)
  2. Build vs Buy (vendor evaluation — 10 dimensions)
  3. Internal Tooling (8 dimensions — skips feature flags, competitive)
  4. Customer-Facing (13 dimensions)
  5. Platform/API (13 dimensions)
  6. Compliance-Driven (12 dimensions)
  Or describe a custom set.

You: 2
```

Families are **additive over time** — as we encounter new product types, we add a new family profile. No code changes needed, just a new JSON file.

---

## Files That Would Be Created

| File | Purpose |
|------|---------|
| `.claude/commands/simulate.md` | Main command (~250 lines) |
| `prompts/strategy/simulate-scenario.md` | Prompt for scenario generation |
| `prompts/strategy/simulate-build-vs-buy.md` | Prompt for build-vs-buy evaluations |
| `prompts/strategy/compare-scenarios.md` | Prompt for comparison |
| `prompts/strategy/improve-dimension.md` | Prompt for dimension drill-down |
| `prompts/evals/rubric-scenario.md` | Self-eval rubric |
| `data/strategy/scenarios/.gitkeep` | Artifact directory |
| `data/meta/product-families/general.json` | Default family (all 10 dimensions) |
| `data/meta/product-families/build-vs-buy.json` | Vendor evaluation family |
| `data/meta/product-families/internal-tooling.json` | Internal tools family |
| `data/meta/product-families/customer-facing.json` | Customer-facing family |
| `data/meta/product-families/platform-api.json` | Platform/API family |
| `data/meta/product-families/compliance-driven.json` | Compliance family |

## Files That Would Be Modified

| File | Change |
|------|--------|
| `data/meta/counters.json` | Add `"scenario": 0` |
| `data/meta/tags.json` | Add `"simulation"`, `"scenario-analysis"`, `"build-vs-buy"` |
| `CLAUDE.md` | Add command, schema, status enums |
| `PM_ASSISTANT_CLAUDE_NATIVE.md` | Add to command docs + inventory |
| Existing commands | Add cross-reference suggestions |

---

## Open Questions

1. **Scope**: Should `/simulate` only handle product decisions, or also process/workflow decisions? (The 10 dimensions work for both.)
2. **Depth**: Should the default be a quick analysis (~500 words) with an option for deep-dive (~2000 words), or always full depth?
3. **Historical tracking**: Should we track how simulated assumptions actually played out post-launch? (Could tie into `/outcomes`.)
4. **Family evolution**: Should product families be user-editable via a command (e.g., `/simulate manage-families`), or is manual JSON editing sufficient for now?
5. **Improve tracking**: When you run `/simulate improve` and act on the guidance, should the scenario artifact be versioned (v1, v2) or updated in place?
6. **Build vs Buy weights**: Should the default TCO/Speed/DX weighting be adjustable per-run, or should we define weight presets (e.g., "cost-sensitive", "speed-first", "DX-first")?
7. **Multi-option limit**: Should Build vs Buy cap at a maximum number of options (e.g., 5) to keep comparisons readable?
