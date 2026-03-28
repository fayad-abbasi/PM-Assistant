# Platform-as-Product Frameworks — Proposal

## Problem

The PM Assistant is built as a generic PM workflow. But the actual role is **Developer Experience / Engineering Enablement** — a PM discipline with its own mental models, metrics, and patterns. Without these baked in, the assistant can produce generically good PM artifacts that miss the specific dynamics of platform work:

- Engineers are your customers, but they're also colleagues who can ignore you
- Adoption is voluntary — you can't mandate usage, you must earn it
- "The right way" must also be "the easy way" (golden paths)
- Past rollout failures create institutional skepticism
- Success is measured in developer productivity, not revenue

Additionally, **AI is reshaping the developer workflow itself**. Code review, code generation, test writing, and documentation are increasingly AI-assisted. The metrics and mental models that defined DevEx in a human-only workflow are shifting — some traditional metrics become noise, new ones emerge, and the PM's job evolves from "make developers faster at writing code" to "make developers better at directing and reviewing AI-generated work."

The PM Assistant needs to encode these patterns so that every artifact it produces reflects platform-as-product thinking — and is forward-looking about how AI changes the game.

---

## What This Adds

Five capabilities:

1. **DevEx Metrics Framework** — structured metrics taxonomy with baselines, targets, and health indicators, including AI-era metrics
2. **Adoption Playbook** — patterns and anti-patterns for driving voluntary adoption of platform tools
3. **Platform Context Injection** — DevEx-specific context woven into existing commands
4. **Judgment Prompts** — challenge questions that sharpen PM decision quality after artifact generation
5. **Blind Spot Surfacing** — proactive scenario generation to expand the PM's field of vision

---

## 1. DevEx Metrics Framework

### The Standard Metrics

Based on industry frameworks (DORA, SPACE, DX Core 4), tailored for platform PM work:

#### Velocity Metrics (How fast can engineers ship?)

| Metric | What It Measures | Good | Warning | Critical |
|--------|-----------------|------|---------|----------|
| **CI/CD Pipeline Time** | Median time from push to deploy-ready | < 15 min | 15-30 min | > 30 min |
| **PR Review Cycle Time** | Median time from PR open to merge | < 8 hours | 8-24 hours | > 24 hours |
| **New Hire Onboarding** | Time to first meaningful commit | < 1 day | 1-3 days | > 3 days |
| **Local Dev Setup** | Time from clone to running locally | < 30 min | 30-120 min | > 2 hours |
| **Deploy Frequency** | Deploys per developer per week | > 2 | 1-2 | < 1 |

#### Quality Metrics (How reliable is the platform?)

| Metric | What It Measures | Good | Warning | Critical |
|--------|-----------------|------|---------|----------|
| **Platform Availability** | Uptime of internal tools and services | > 99.9% | 99.5-99.9% | < 99.5% |
| **Incident Frequency** | Platform-caused incidents per month | < 2 | 2-5 | > 5 |
| **MTTR (Platform)** | Mean time to resolve platform issues | < 1 hour | 1-4 hours | > 4 hours |
| **Flaky Test Rate** | % of CI failures that are flaky (not real) | < 2% | 2-10% | > 10% |
| **Rollback Rate** | % of deploys that require rollback | < 2% | 2-5% | > 5% |

#### Adoption Metrics (Are engineers using what we build?)

| Metric | What It Measures | Good | Warning | Critical |
|--------|-----------------|------|---------|----------|
| **Tool Adoption Rate** | % of eligible teams actively using a tool | > 80% | 50-80% | < 50% |
| **Voluntary Adoption** | % adopting without mandate or nudging | > 60% | 30-60% | < 30% |
| **Retention (30-day)** | % still using 30 days after first use | > 85% | 70-85% | < 70% |
| **NPS (Platform)** | Platform team NPS from engineer surveys | > 40 | 20-40 | < 20 |
| **Support Ticket Volume** | Tickets per 100 engineers per month | < 10 | 10-30 | > 30 |

#### Efficiency Metrics (Is the platform cost-effective?)

| Metric | What It Measures | Good | Warning | Critical |
|--------|-----------------|------|---------|----------|
| **Cost per Developer** | Infrastructure cost / active developers | Trending down | Flat | Trending up |
| **Self-Service Rate** | % of requests resolved without platform team | > 80% | 50-80% | < 50% |
| **Toil Ratio** | % of platform team time on manual/repetitive work | < 20% | 20-40% | > 40% |
| **Automation Coverage** | % of common workflows that are automated | > 80% | 50-80% | < 50% |

#### AI-Augmented Workflow Metrics (How well are developers leveraging AI?)

As AI becomes embedded in the development process — code generation, code review, test writing, documentation — traditional metrics shift. Some become noise (deploy frequency inflates artificially), some become more critical (judgment quality), and entirely new categories emerge.

| Metric | What It Measures | Good | Warning | Critical |
|--------|-----------------|------|---------|----------|
| **AI Suggestion Acceptance Rate** | % of AI suggestions accepted without modification | 40-70% | > 70% (rubber-stamping?) | < 20% (tool not useful) |
| **Edit-After-Accept Rate** | % of accepted AI code modified within 24 hours | < 10% | 10-25% | > 25% (accepting bad code) |
| **AI-Assisted Defect Rate** | Post-deploy defect rate in AI-generated vs human-written code | Equal or lower | 1.5x human rate | > 2x human rate |
| **Pre-Commit Catch Rate** | % of issues caught by AI before reaching CI pipeline | > 60% | 30-60% | < 30% |
| **Review Depth (AI-assisted PRs)** | Avg time humans spend reviewing AI-flagged PRs | > 5 min | 2-5 min | < 2 min (rubber-stamping) |
| **AI Tool NPS** | Developer satisfaction with AI coding tools specifically | > 40 | 20-40 | < 20 |

**Why the warning thresholds are different**: Note that AI Suggestion Acceptance Rate has a *ceiling* warning, not just a floor. An acceptance rate above 70% may indicate developers are rubber-stamping AI output rather than exercising judgment. Similarly, Review Depth warns when it's too *low* — fast reviews of AI-generated code suggest insufficient human oversight. These metrics encode the principle that **AI leverage without human judgment is a risk, not an efficiency gain**.

**How traditional metrics shift in an AI-augmented world**:

| Traditional Metric | How It Changes | What Replaces or Supplements It |
|-------------------|----------------|--------------------------------|
| **PR Review Cycle Time** | Compresses dramatically (AI does first pass) | Review *quality* — are humans catching what AI misses? |
| **CI/CD Pipeline Time** | Less critical if AI catches issues pre-commit | Pre-commit catch rate; pipeline *failure rate* (should drop) |
| **Deploy Frequency** | Inflates (AI-assisted PRs ship faster) | *Meaningful* deploy frequency — deploys that deliver user value, not just code churn |
| **New Hire Onboarding** | AI pair programming compresses ramp-up | Time to first *independent architectural decision* — can they reason about the system, not just produce code? |
| **Lines of Code** | Becomes meaningless (AI generates at scale) | *Decision density* — ratio of judgment calls to code volume |
| **DORA Lead Time** | Bottleneck shifts from coding to review/approval | Time from *decision to deploy* (includes the thinking, not just the typing) |

**Implication for the DevEx PM**: The job shifts from "make developers faster at writing code" to "make developers better at directing and reviewing AI-generated work." Platform investments should be evaluated not just on "does this save time?" but on "does this maintain or improve judgment quality as AI takes over more execution?"

### How Metrics Integrate

These metrics feed into multiple commands:

| Command | How Metrics Are Used |
|---------|---------------------|
| `/strategy suggest-okrs` | Suggests OKRs based on metrics in warning/critical state |
| `/prd` | Includes baseline metric and target in PRD context |
| `/outcomes` | Compares actual metric movement against PRD expectations |
| `/simulate` | Uses metric baselines to ground scenario scoring |
| `/pm-dash` | Shows metric health dashboard alongside artifact status |
| `/next` | Flags degrading metrics as action items |

### Storage

Metric definitions stored in `data/meta/devex-metrics.json`:

```json
{
  "categories": [
    {
      "name": "velocity",
      "metrics": [
        {
          "key": "ci_pipeline_time",
          "name": "CI/CD Pipeline Time",
          "unit": "minutes",
          "direction": "lower_is_better",
          "thresholds": { "good": 15, "warning": 30 },
          "source": "manual | grafana | datadog"
        }
      ]
    }
  ]
}
```

Metric snapshots stored in `data/analytics/snapshots/` (ties into the Quantitative Analysis proposal once tooling is determined).

---

## 2. Adoption Playbook

### The Core Problem

Platform teams build tools that engineers can choose to ignore. The #1 failure mode isn't building the wrong thing — it's building the right thing and failing to drive adoption. This playbook codifies patterns for earning adoption.

### Adoption Patterns (What Works)

#### 1. The Golden Path
**Pattern**: Make the recommended approach the easiest approach. Don't just build a better tool — make it the path of least resistance.

**Application**: When `/prd` generates a PRD for an internal tool, include a "Golden Path" section:
- What's the current path? (how do engineers do this today)
- What's the new path? (how should they do it with this tool)
- What friction does the new path remove?
- Is the new path actually easier, or just "better in theory"?

**Anti-pattern**: Building a tool that's objectively better but requires more steps, config, or mental overhead than the status quo.

#### 2. Champions Network
**Pattern**: Seed adoption through respected engineers who try the tool early, provide feedback, and advocate to peers. Peer recommendation > top-down mandate.

**Application**: When `/gtm` generates a rollout plan, include a Champions section:
- Which teams/individuals should pilot first? (pick by influence, not seniority)
- What makes a good champion? (respected, vocal, from a high-visibility team)
- How will champions be supported? (direct Slack channel, fast bug fixes, input on roadmap)
- How do we amplify champion success? (demos, Slack posts, metrics from their team)

**Anti-pattern**: Pilot with the most senior team (they're often the most set in their ways) or pilot with the team that "needs it most" (they'll attribute their struggles to the new tool).

#### 3. Data-Driven Nudging
**Pattern**: Show engineers how the tool benefits them specifically, with their data. "Your PR review time dropped from 18h to 6h since enabling the AI reviewer" is more compelling than "average review time improved."

**Application**: When `/outcomes` tracks post-launch metrics, generate per-team or per-cohort impact summaries that can be shared back with those teams.

**Anti-pattern**: Only publishing org-wide averages, which no individual engineer identifies with.

#### 4. Opt-Out > Opt-In
**Pattern**: Default-on with easy opt-out drives higher adoption than opt-in. But only if the tool is genuinely low-friction — defaulting a painful tool to "on" creates backlash.

**Application**: `/simulate` scenarios for internal tools should evaluate "Is this tool good enough to default on?" as a readiness gate before switching from opt-in to opt-out.

**Anti-pattern**: Mandating usage. Engineers find workarounds, adoption numbers look good but satisfaction craters, and the next tool you ship starts with negative trust.

#### 5. Respect the Skeptics
**Pattern**: The engineers who push back hardest often have the most useful feedback. Engage them as design partners, not obstacles. If a senior engineer says "I don't need this," understand why before dismissing their view.

**Application**: When `/discover` analyzes interview feedback, flag dissenting voices as high-signal rather than noise. When `/gtm` plans a rollout, include a "Skeptic Engagement" section.

**Anti-pattern**: Treating low adoption as a marketing problem. If engineers aren't using the tool after a good-faith rollout, the tool may have a product problem.

### Adoption Anti-Patterns (What Fails)

| Anti-Pattern | Why It Fails | What To Do Instead |
|-------------|-------------|-------------------|
| **The Mandate** | Engineers find workarounds; breeds resentment; erodes trust for future tools | Make the tool so good they choose it; use opt-out instead of mandate |
| **The Big Bang** | Too many changes at once; can't attribute problems; overwhelms support | Phased rollout; one team at a time; measure before expanding |
| **Build It and They Will Come** | No launch plan; engineers don't know it exists or why to care | Dedicated GTM plan even for internal tools |
| **The Metrics Trap** | Optimizing for adoption % instead of developer satisfaction | Track NPS and retention alongside adoption; high adoption + low NPS = trouble |
| **The Design System Problem** | Built without input from users; doesn't fit actual workflows | Co-design with 2-3 teams before building; validate golden path is actually golden |
| **Ignoring the Graveyard** | Not acknowledging past tool failures; "this time it's different" | Explicitly address what went wrong before and how this avoids those mistakes |

### Playbook Integration

The adoption playbook doesn't live as a standalone command. Instead, it's woven into existing commands:

| Command | Adoption Awareness |
|---------|-------------------|
| `/prd` | "Golden Path" section added to PRD template for internal tools |
| `/gtm` | Champions, skeptic engagement, past failure lessons added to rollout plans |
| `/simulate` | "Internal Adoption" dimension in Internal Tooling family; "DX & Friction" in Build vs Buy |
| `/outcomes` | Track adoption rate, retention, NPS alongside functional metrics |
| `/retro` | Adoption-specific retro questions: "What drove adoption? What created resistance?" |
| `/discover` | Flag dissenting feedback as high-signal; weight skeptic interviews |

---

## 3. Platform Context Injection

### Session Context Enhancement

The session-start hook (`scripts/session-context.sh`) should include a platform context block when DevEx data exists:

```
PLATFORM HEALTH:
  CI/CD: 22 min median (WARNING — target < 15 min)
  PR Review: 14 hours (WARNING — target < 8 hours)
  Platform NPS: 35 (WARNING — target > 40)
  Tool Adoption: 72% avg (OK)

ACTIVE ADOPTION EFFORTS:
  AI Code Review: Week 6 of 12 — 45% adoption, pilot complete
  Self-Service DB: Pre-launch — PRD in review
```

This ensures every session starts with awareness of the platform's current state.

### Prompt Template Enhancement

Existing prompt templates should be aware of the platform-as-product context. When an artifact is being generated for an internal/platform tool:

- PRDs should include: golden path, adoption strategy, migration plan from current state
- GTM plans should include: champion network, phased rollout, skeptic engagement
- OKRs should reference: DevEx metrics with baselines and targets
- Retrospectives should include: adoption curve analysis, what drove/blocked adoption

This doesn't require separate commands — it requires updating prompt templates to conditionally include platform-specific sections when the context is internal/platform tooling.

---

## 4. Judgment Prompts

### The Problem They Solve

The PM Assistant generates artifacts — PRDs, GTM plans, scenarios, roadmaps. The natural instinct is to review the output, make minor tweaks, and move on. But the real value a PM adds isn't in producing the artifact — it's in the **judgment applied to it**. Shreyas Doshi's Product Sense framework (empathy, simulation, strategic thinking, taste, creative problem-reframing) describes the skills that make a PM's judgment valuable. The assistant should actively exercise these skills, not bypass them.

Judgment prompts are **challenge questions** presented after artifact generation, before the quality check. They force the PM to engage critically with the output rather than accept it.

### How It Works

After any generation command (`/prd`, `/gtm`, `/simulate`, `/strategy`) produces an artifact, the assistant presents 2-3 targeted questions before running the quality check:

```
ARTIFACT GENERATED: prd-2026-04-01-003 — "Self-Service Database Provisioning"

Before we finalize, consider:

1. TASTE: You chose self-service over a managed request process.
   What specifically makes self-service the right model here, and
   for which teams might it actually be worse?

2. EMPATHY: The PRD targets "all engineering teams." But the team
   that files the most DB requests (Payments) has different needs
   than the team that files the fewest (Mobile). How does this
   serve both?

3. REFRAME: Instead of making database provisioning easier, is there
   an approach that reduces the need for new databases altogether?

→ Type your reflections, or say "proceed" to skip to quality check.
```

### Question Categories

Each question maps to one of Doshi's Product Sense skills (adapted for DevEx):

| Category | Skill | What It Challenges |
|----------|-------|-------------------|
| **Taste** | Great Taste | "Given this recommendation, is it actually the *right* choice? Why this over alternatives?" |
| **Empathy** | Strong Empathy | "Who specifically benefits? Who might be harmed or overlooked? What do *they* think?" |
| **Reframe** | Simulation + Creative Problem-Reframing | "What if the premise is wrong? What's the non-obvious approach?" |
| **Blind spot** | Simulation | "What scenario haven't you considered? What assumption are you making unconsciously?" |
| **Strategy** | Strategic Thinking | "How does this differentiate your platform? What does this make possible (or impossible) next?" |

### Question Generation Logic

Questions are not random. They're generated based on the artifact content:

- **Taste questions** trigger when the artifact makes a clear choice between alternatives (build vs buy, this approach vs that)
- **Empathy questions** trigger when the artifact targets a broad audience ("all engineers", "all teams") without segmentation
- **Reframe questions** trigger when the artifact optimizes an existing process rather than questioning whether the process should exist
- **Blind spot questions** trigger always — there's always something unconsidered
- **Strategy questions** trigger when the artifact doesn't connect to the broader platform direction or OKRs

### Integration

| Command | Judgment Prompt Behavior |
|---------|------------------------|
| `/prd` | 2-3 questions after PRD generation, before quality check |
| `/gtm` | 2 questions focused on empathy (audience) and reframe (is a GTM plan the right response?) |
| `/simulate` | 1-2 questions after scenario generation, focused on blind spots and assumptions |
| `/strategy` | 2 questions after OKR/roadmap work, focused on taste (right priorities?) and strategy (differentiation) |
| `/retro` | Judgment review: "Looking back, where did your judgment prove right or wrong?" — this is where Doshi's decision journal concept lives naturally |

### What This Is NOT

- Not a quiz or test — the PM can say "proceed" and skip
- Not a quality gate — it doesn't block artifact creation
- Not prescriptive — the questions don't have right answers
- It's a **thinking prompt** that builds the habit of critical engagement with AI-generated output

---

## 5. Blind Spot Surfacing

### The Problem It Solves

When `/simulate` runs a scenario, it explores the dimensions you ask about. But Doshi's "simulation skills" are about the PM's ability to **imagine scenarios unprompted** — to see around corners. The assistant should expand the PM's field of vision by proactively surfacing what they didn't think to ask.

### How It Works

After `/simulate` generates a scenario, it adds a **"What You Might Be Missing"** section with 2-3 proactive scenarios or considerations the PM didn't raise:

```
SCENARIO GENERATED: scenario-2026-04-01-001
"Adopt GitGuardian for secret scanning"

[... full dimension analysis ...]

WHAT YOU MIGHT BE MISSING:

1. SECOND-ORDER EFFECT: If secret scanning catches 95% of leaked secrets,
   engineers may become *less careful* about secret hygiene (moral hazard).
   Have you considered how to maintain security awareness alongside
   automated detection?

2. ADJACENT DECISION: Secret scanning solves detection, but not prevention.
   The real leverage might be in a secrets management platform (Vault, AWS
   Secrets Manager) that makes it hard to have secrets in code at all.
   Should this decision wait until the prevention strategy is clear?

3. STAKEHOLDER BLIND SPOT: The security team will love this. But the
   engineers who are currently "getting away with" poor secret practices
   will experience this as friction. Your rollout plan addresses
   champions and skeptics, but doesn't account for the engineers who
   will feel singled out by initial scan results.

→ Run `/simulate sensitivity` on any of these to explore further.
```

### Generation Logic

Blind spots are generated by examining the scenario through lenses the PM didn't explicitly address:

| Lens | What It Catches |
|------|----------------|
| **Second-order effects** | Behavioral changes caused by the decision itself (incentive shifts, moral hazard, unintended consequences) |
| **Adjacent decisions** | Related decisions that should be made first, simultaneously, or that this decision constrains |
| **Stakeholder blind spots** | Groups affected by the decision who aren't mentioned in the scenario |
| **Temporal blind spots** | "This works now, but what about in 12 months when X changes?" (headcount growth, tech shifts, AI adoption curves) |
| **Failure mode blind spots** | "What does graceful failure look like? What happens if this partially succeeds?" |

### Integration

- **`/simulate`**: Always appended to scenario output (2-3 blind spots)
- **`/prd`**: Optional — appended when the PRD involves a significant platform decision
- **`/strategy`**: Appended to roadmap prioritization — "what are you deprioritizing by implication?"

### Why This Develops PM Skills

Over time, the PM starts anticipating the blind spots before the assistant surfaces them. The pattern trains simulation thinking — "what would the assistant flag here?" becomes internalized as "what am I not seeing?" This is the developmental value: not replacing judgment, but training it.

---

## Files That Would Be Created

| File | Purpose |
|------|---------|
| `data/meta/devex-metrics.json` | Metric definitions, thresholds, and categories (including AI-augmented metrics) |
| `data/meta/adoption-playbook.md` | Reference doc for adoption patterns (readable by Claude and humans) |
| `data/meta/judgment-prompts.json` | Question templates by category (taste, empathy, reframe, blind spot, strategy) |
| `prompts/strategy/suggest-okrs-devex.md` | DevEx-aware OKR suggestion prompt |
| `prompts/strategy/surface-blind-spots.md` | Prompt for generating blind spot scenarios |
| `prompts/gtm/draft-internal-rollout.md` | Internal tool rollout template (champions, skeptics, phased approach) |
| `prompts/prd/generate-prd-platform.md` | Platform tool PRD template (golden path, adoption strategy, migration) |

## Files That Would Be Modified

| File | Change |
|------|--------|
| `scripts/session-context.sh` | Add platform health section when metric data exists |
| `prompts/prd/generate-prd.md` | Add conditional platform-specific sections |
| `prompts/gtm/draft-developer.md` | Add adoption playbook patterns |
| `prompts/retro/generate-retro.md` | Add adoption-specific retro questions |
| `CLAUDE.md` | Add DevEx metrics schema, adoption playbook reference |
| `PM_ASSISTANT_CLAUDE_NATIVE.md` | Document platform-as-product framework |
| `data/meta/tags.json` | Add `"devex"`, `"adoption"`, `"platform-health"`, `"golden-path"` |

---

## Integration with `/simulate` Product Families

The Internal Tooling product family in `/simulate` should use the adoption playbook:

- "Internal Adoption" dimension scores against the playbook patterns
- "DX & Friction" dimension evaluates the golden path quality
- Sensitivity analysis can test "What if adoption stalls at 40%?"

The Build vs Buy family uses DevEx metrics as grounding:

- "DX & Friction" dimension references current metric baselines
- TCO includes developer time cost (hourly rate × hours saved × headcount)

---

## Influence: Shreyas Doshi's Product Sense Framework

This proposal is informed by Shreyas Doshi's argument that **product sense is the only PM skill that will matter in the AI age**. His five-component decomposition:

1. **Strong Empathy** — figuring out what people need beyond what AI analysis shows
2. **Excellent Simulation** — identifying future possibilities from domain understanding
3. **Stellar Strategic Thinking** — identifying segments and articulating differentiators
4. **Great Taste** — determining optimal choices and explaining reasoning
5. **Creative Execution** — conceiving unique solutions competitors cannot

In a DevEx context, we adapt this:
- **Empathy** → understanding developer pain points at a level deeper than survey data (served by `/discover` + adoption playbook's "respect the skeptics")
- **Simulation** → anticipating how platform decisions play out across teams and over time (served by `/simulate` + blind spot surfacing)
- **Strategic Thinking** → making platform investments that compound rather than just fix immediate pain (served by `/strategy` + DevEx metrics)
- **Taste** → knowing when an AI-generated PRD or roadmap is *right* vs just well-structured (served by judgment prompts)
- **Creative Execution** → reframed as **creative problem-reframing** for DevEx — the innovation isn't novel features, it's seeing that the answer to "slow code reviews" might be "AI handles 80% of review" rather than "faster human reviewers." Less critical than in consumer products, but relevant when rethinking workflows.

The judgment prompts and blind spot surfacing are directly designed to exercise these skills — turning the PM Assistant from a pure execution tool into a **judgment development tool**.

---

## Open Questions

1. **Metric baselines**: Should we capture current baselines immediately (even before `/metrics` exists), or wait for the quantitative analysis capability?
2. **Playbook evolution**: Should the adoption playbook be a static reference doc, or should it grow over time with learnings from actual rollouts tracked in `/retro`?
3. **Template branching**: Should platform-specific prompt templates be separate files (e.g., `generate-prd-platform.md`) or conditional sections within existing templates?
4. **Scoring model**: Should DevEx metrics use the same Good/Warning/Critical thresholds as defined here, or should thresholds be configurable per organization?
5. **DORA in the AI era**: Should we track DORA metrics as a first-class set with the caveat that thresholds will shift, or define new "AI-era DORA" equivalents from the start?
6. **Judgment prompt frequency**: Should judgment prompts fire on every generation, or only for high-stakes artifacts (PRDs, strategy decisions)? Too frequent = fatigue; too rare = no habit formation.
7. **Blind spot calibration**: How do we avoid blind spot surfacing becoming noise? Should it learn from which blind spots the PM engages with vs dismisses?
8. **AI metric collection**: AI-augmented workflow metrics require tooling integration (IDE telemetry, AI tool APIs). Should we define the metrics now and collect manually, or wait until tooling supports automated collection?
