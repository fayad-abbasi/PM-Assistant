# Assumptions as Code — Proposal

## Problem

The PM Assistant captures **insights** (patterns and themes from research) but has no structured way to capture **assumptions** — falsifiable claims about a specific user group, often with a quantitative estimate, that the org relies on when prioritizing and scoping work.

Without this layer, three failure modes recur:

1. **Conflict** — two teams hold contradictory assumptions about the same user group and don't discover it until a project is scoped.
2. **Invisible** — an assumption exists in one team's head (or one interview) but is never surfaced when another team starts related work.
3. **Stale** — an assumption from six months ago silently informs today's decision even though the underlying reality has shifted.

When drafting a PRD, OST, or GTM message, there's no recall mechanism that says *"here's what we already believe about this user group — do you still agree?"*

## Origin

Based on the "assumptions as code" framework developed by Mina Tawadrous (Associate Director, Platform Engineering) and Eleanor Millman (Senior Staff PM) at SiriusXM. Public sources describe the *why* and the *consumption pattern* but do not publish the schema, file format, or extraction pipeline. We are designing our own version.

### External references

- [DX newsletter write-up](https://newsletter.getdx.com/p/assumptions-as-code-siriusxms-approach)
- [Podcast episode page](https://getdx.com/podcast/assumptions-as-code-siriusxm-approach-to-platform-prioritization/) / [YouTube](https://youtu.be/V-3Cv0LUYa4)
- [Eleanor Millman — Platform Engineering Oslo, Sept 2025](https://youtube.com/live/5Vr8zUlpWEQ) — solo talk on the prioritization framework. **Watch before finalizing the schema** — her slides may expose field structure not in any written source.
- [Jared Wolinsky — earlier DX episode](https://getdx.com/podcast/siriusxm-revamped-platform-developer-experience/) — confirms the prioritization weights and 7-factor model
- [DX Annual 2026 session](https://dxannual.com/) — "Prioritization as Code" (April 16, 2026) — recording not yet published as of this writing

**Name note**: DX's published materials use "Wolinsky"; the podcast audio arguably says "Wilensky." Use **Wolinsky** when citing.

---

## Proposal

Introduce **`assumption`** as a new artifact type alongside `insight`, stored as markdown + frontmatter under `data/assumptions/`.

### Why a new artifact vs. extending insights

Insights describe **patterns** ("developers are frustrated with local iteration"). Assumptions are **testable, scoped claims** ("~30% of backend developers spend >15 min/day waiting on local builds"). The two differ in:

| Dimension | Insight | Assumption |
|-----------|---------|------------|
| Shape | Narrative theme | Falsifiable claim + scope + estimate |
| Lifecycle | Active → superseded → archived | Active → stale → invalidated or revalidated |
| Consumed by | Evidence for PRDs | Recall during drafting; conflict detection |
| Granularity | One per research batch | Many per research batch |

Separating them keeps insights useful as research evidence and gives assumptions their own lifecycle (staleness, validation, conflict).

This is a **leaning decision**, not final — see open questions.

### File storage

- `data/assumptions/*.md` — one file per assumption
- ID: `assumption-{YYYY-MM-DD}-{NNN}`
- Counter: `assumption` in `data/meta/counters.json`

### Draft schema

```yaml
---
id: assumption-2026-04-17-001
title: string                          # short human-readable handle
claim: string                          # the falsifiable statement
user_group: string                     # who the claim is about
estimate:                              # optional quantitative anchor
  value: number
  unit: string
  basis: string                        # how the number was derived
confidence: low | medium | high
source_type: interview | survey | dx-metric | slack-poll | analytics | inferred
linked_interviews: [interview-IDs]
linked_insights: [insight-IDs]
linked_prds: [PRD-IDs]
tags: [from tags.json]
status: active | stale | invalidated | superseded
last_validated_at: ISO-date
superseded_by: assumption-ID or null
created_at: ISO-datetime
updated_at: ISO-datetime
---
```

### Body sections

1. **Claim detail** — the full statement with nuance
2. **Evidence** — what supports it, with source pointers
3. **Known conflicts** — other assumptions that disagree, if any
4. **How to invalidate** — what observation would falsify this
5. **Notes** — history, caveats, discussion

---

## Workflow Integration

### Authoring — how assumptions get into the repo

**1. From interviews** — new command `/discover extract-assumptions <interview-id>`
- A `general-purpose` subagent reads the interview transcript
- Proposes candidate assumption records (claim, user_group, estimate if extractable, confidence)
- Human reviews, edits, commits
- Runs quality-check before finalizing

**2. From PRD/OST drafting** — during `/prd` or `/ost`, the assistant surfaces existing assumptions for the relevant user_group and asks the user to validate, contradict, or enrich. Validations update `last_validated_at`. Contradictions either create a new assumption or mark the old one `invalidated`.

**3. Manual** — `/discover add-assumption` for one-off capture.

### Recall — where assumptions get surfaced

- `/prd` — during problem statement and personas sections, surface relevant assumptions for the target user_group
- `/ost` — during opportunity and assumption-test branches
- `/grill-me --deliberate` — board members receive relevant assumptions with their brief
- `/gtm` — when drafting audience-specific messages, show audience-relevant assumptions
- `/next` — flag stale assumptions that should be re-validated

### Staleness

- `last_validated_at` older than **N days** → `status: stale`, flagged in `/link-check` and `/pm-dash`
- N is an open question (see below). Default candidate: 90 days, overridable per assumption

### Three execution modes (mirrors SiriusXM)

- **Rapid**: silently surface top-3 relevant assumptions during drafting, no interaction required
- **Standard**: conversational — agent asks *"I see an assumption from 2026-02-14 stating X. Still true?"*
- **Deep-dive**: full re-extraction run on a new user group or new initiative where we suspect coverage is thin

---

## Open Questions to Evaluate

### Design

1. **Separate artifact vs. extend insights** — proposal leans separate. Revisit after authoring the first 5–10 assumption records to see if the distinction holds in practice.

2. **Extraction aggressiveness** — how many assumption records should the AI propose per interview? Under-extraction misses the point; over-extraction produces noise that drowns the recall signal. Worth calibrating on real interviews.

3. **Quantitative threshold** — does an assumption without a numeric estimate still qualify, or is that just a specially-tagged insight? If yes, what distinguishes it from an insight in practice?

4. **Deduplication** — how does the system detect semantic overlap between assumptions? Exact tag match is easy; semantic similarity is harder. Options: manual-only at first, then add embedding-based suggestions if the corpus grows.

5. **Conflict detection** — should the system auto-flag when two assumptions about the same `user_group` contradict, or is that discovered by humans during drafting? Auto-detection requires structured conflict rules (e.g., overlapping `estimate` ranges).

6. **Staleness TTL** — 90 days default? Varies by `source_type` (a DX metric might stale faster than an interview-derived claim)? Per-assumption override?

7. **`invalidated` vs. `superseded`** — separate states or collapse to one? Superseded implies a replacement exists; invalidated doesn't. Keeping both is cleaner but more fields to maintain.

### Integration

8. **Relationship to OST assumption tests** — OSTs already have `assumption-test` as a concept scoped to a solution branch. Assumption records are broader and cross-cutting. Are OST tests a *subset* (a test that validates a specific assumption record) or *parallel* (project-scoped vs. org-scoped)? Likely: OST tests should reference assumption records by ID when applicable.

9. **Backend skill packaging** — does the recall mechanism live in each command's prompt, in a shared `prompts/assumptions/recall.md`, or eventually in an MCP server? Start with shared prompt; escalate only if reuse patterns demand it.

10. **Interview transformation prompt** — the quality of the extraction pipeline is the whole ballgame. The extraction prompt needs to distinguish claims from anecdotes, attach a `user_group` scope, and honestly mark `confidence`. First pass: hand-craft the prompt and evaluate against 2–3 real interviews before committing to the command.

### Process

11. **Timing** — building this before there are 10+ interviews in `data/interviews/` may be premature. Assumption-recall has value only when the recall corpus is non-trivial. Possible sequencing: finish discovery through week 4–5 first, then build assumptions-as-code once there's enough raw material to test extraction against.

12. **Watch the Oslo talk first** — 45 minutes of Eleanor's solo talk may expose schema details not in any written source. Worth watching before locking the schema.

---

## Files That Would Be Created

| File | Purpose |
|------|---------|
| `.claude/commands/assumption.md` *(or extend `/discover`)* | Command for extract / add / validate / invalidate |
| `prompts/assumptions/extract-from-interview.md` | Prompt for the interview → assumption extraction subagent |
| `prompts/assumptions/recall.md` | Shared prompt for surfacing relevant assumptions during drafting |
| `prompts/assumptions/validate.md` | Prompt for the standard-mode conversational validation loop |
| `data/assumptions/.gitkeep` | Directory seed |
| `rubrics/assumption.md` | Quality rubric for eval scoring |

## Files That Would Be Modified

| File | Change |
|------|--------|
| `data/meta/counters.json` | Add `"assumption": 0` |
| `data/meta/tags.json` | Add `"assumption"`, `"stale"`, `"conflict"` tags |
| `.claude/commands/prd.md` | Call assumption recall during problem statement + personas |
| `.claude/commands/ost.md` | Call assumption recall at opportunity and assumption-test branches; cross-link OST tests to assumption IDs |
| `.claude/commands/gtm.md` | Surface audience-relevant assumptions when drafting |
| `.claude/commands/grill-me.md` | `--deliberate` mode passes relevant assumptions into each board member's brief |
| `.claude/commands/discover.md` | Add `extract-assumptions` and `add-assumption` subcommands |
| `.claude/commands/next.md` | Surface stale assumptions as recommended re-validations |
| `.claude/commands/pm-dash.md` | Add assumption count, staleness breakdown, conflict count |
| `.claude/commands/link-check.md` | Validate `linked_interviews` / `linked_insights` on assumptions |
| `CLAUDE.md` | Document the new artifact type, schema, and workflow rules |

---

## Minimum Viable Version

If fully wiring every command is too much for a first pass, a viable MVP is:

1. `data/assumptions/` directory, schema, counter, tag
2. `/discover extract-assumptions <interview-id>` command + extraction prompt
3. `/discover add-assumption` for manual capture
4. A single shared recall prompt called manually from `/prd` during problem-statement drafting
5. Staleness flag in `/pm-dash`

Everything else (auto-recall in GTM, conflict detection, OST integration) can follow once the core loop proves itself.
