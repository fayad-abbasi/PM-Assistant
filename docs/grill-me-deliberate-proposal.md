# `/grill-me` Redesign — Three-Mode Workflow with Board Deliberation

## Problem

The current `/grill-me` command has two modes (default stress-test and `--conversation`), but the workflow dead-ends after the stress test. There's no structured path from "I've pressure-tested my thinking" to "I have a decision memo I can feed into a PRD." The user has to manually bridge that gap — reformulating their grilled idea into a problem statement, re-articulating the perspectives they already explored, and losing the nuance from the conversation.

Additionally, the current mode names don't clearly signal intent. `--conversation` undersells its purpose (collaborative idea construction), and the bare default doesn't distinguish itself from the new deliberation mode.

## Proposal

Redesign `/grill-me` into a three-stage workflow with renamed modes and a new `--deliberate` mode that runs a multi-agent board deliberation entirely within Claude Code (no Pi, no Bun — zero extra dependencies).

---

## The Three Modes

### Mode 1: `--brainstorm` (renamed from `--conversation`)

**Purpose**: Collaborative idea development. Meet the user where they are — vague hunch, rough concept, or emerging strategy — and build the idea together.

**Behavior**: No changes from current `--conversation` mode. Rename only.

### Mode 2: `--debate` (renamed from default)

**Purpose**: Stress-test the idea. Walk down each branch of the decision tree, challenge assumptions, poke holes.

**Behavior**: No changes from current default grill mode. Rename only.

### Mode 3: `--deliberate` (new)

**Purpose**: Run a multi-agent board deliberation that produces a structured decision memo. The memo is designed to feed directly into the `/prd` workflow.

**Behavior**: See detailed design below.

### Bare `/grill-me` (no flag)

When invoked without a flag, present a mode picker:

```
Which mode?
  1. Brainstorm — flesh out a half-formed idea collaboratively
  2. Debate — stress-test a plan or design relentlessly
  3. Deliberate — run a board of advisors and produce a decision memo
```

---

## `--deliberate` Mode — Detailed Design

### Flow

1. **Brief synthesis** — Analyze the current conversation context (from prior `--brainstorm` and/or `--debate` sessions, or a fresh problem statement). Synthesize a structured brief with four sections:
   - **Situation** — what is happening, stated as facts
   - **Stakes** — upside if we get it right, downside if we get it wrong
   - **Constraints** — budget, timeline, capacity, technical, regulatory
   - **Key Question** — the single most important question for the board

2. **User confirmation** — Present the synthesized brief to the user. Allow edits before proceeding. The brief quality determines the deliberation quality.

3. **Board deliberation** — Spawn board members as parallel Claude Code subagents (using the Agent tool). Each receives the brief + their persona system prompt + any relevant context files from `data/insights/`, `data/prds/`, `data/strategy/`.

4. **Round 1 — Opening positions** — All board members respond with their initial position in parallel.

5. **Orchestrator synthesis** — The main conversation (acting as PM Lead) reads all positions, identifies tensions and disagreements, and formulates targeted follow-up questions.

6. **Round 2-3 — Targeted follow-ups** — Spawn targeted subagent calls to resolve specific tensions (e.g., "User Advocate and Engineering Reality disagree on feasibility — address each other's concerns"). Limit to 2-3 rounds to keep cost bounded.

7. **Final statements** — Each board member delivers a closing position. Contrarian speaks last (enforced).

8. **Memo synthesis** — The orchestrator produces the decision memo (see output format below).

### Board Composition (PM-Relevant)

| Member | Role | Perspective | Time Horizon |
|--------|------|-------------|--------------|
| **PM Lead** | Orchestrator (main conversation) | Frames the decision, drives rounds, synthesizes | This quarter |
| **User Advocate** | Subagent | Real user behavior, adoption friction, JTBD, workflow fit | Next user session |
| **Data Analyst** | Subagent | Evidence gaps, measurement plans, metric rigor, what the data says vs. doesn't say | Metrics cycle |
| **Engineering Reality** | Subagent | Feasibility, technical cost, hidden complexity, system durability | 6-18 months |
| **Business Strategist** | Subagent | Revenue impact, market timing, competitive positioning, GTM | This quarter |
| **Contrarian** | Subagent | Attacks assumptions, surfaces blind spots, stress-tests consensus (always speaks last) | Variable |

Board composition is configurable. Members can be added, removed, or swapped by editing the board roster file (see Files section). The system should be designed so adding a new persona requires only creating a new markdown prompt file and adding an entry to the roster.

### Memo Output Format

The memo must contain all the information needed to initiate a `/prd` workflow. Structure:

```yaml
---
id: memo-{date}-{NNN}
title: "<decision title>"
status: draft
brief_question: "<the key question from the brief>"
board_members: [PM Lead, User Advocate, Data Analyst, Engineering Reality, Business Strategist, Contrarian]
tags: []
created_at: <ISO datetime>
---
```

#### Memo Body Sections

1. **Decision Summary** — 2-3 sentence verdict. What the board recommends and why.

2. **Ranked Recommendations** — #1, #2, #3 options with:
   - Description
   - Board support (which members favor this and why)
   - Key risk

3. **Problem Statement** — Synthesized from the deliberation. Grounded in evidence surfaced by the board. *This section maps directly to PRD Section 1.*

4. **Hypothesis** — Framed in I BELIEVE THAT / WILL / FOR / BECAUSE format, derived from the winning recommendation. *This section maps directly to PRD Section 2.*

5. **User Impact** — User Advocate's assessment: who is affected, how behavior changes, adoption friction. *Feeds PRD Sections 3 (Personas), 4 (User Stories), 10 (Adoption Strategy).*

6. **Feasibility Assessment** — Engineering Reality's assessment: technical cost, dependencies, complexity, system risks. *Feeds PRD Sections 5 (Functional Reqs), 6 (Non-Functional Reqs), 11 (Dependencies), 12 (Risks).*

7. **Business Case** — Business Strategist's assessment: revenue impact, market timing, competitive positioning. *Feeds PRD Sections 8 (Success Metrics), 10 (Adoption Strategy).*

8. **Evidence Gaps** — Data Analyst's assessment: what we know, what we don't, what we need to measure. *Feeds PRD Section 8 (Success Metrics).*

9. **Board Stances** — Per-member summary: position, reasoning, key concern.

10. **Dissent & Unresolved Tensions** — What the board could not agree on. What assumptions remain untested. *Feeds PRD Section 12 (Risks), 13 (Out of Scope).*

11. **Scope Recommendation** — What's in MVP vs. deferred, based on board consensus. *Feeds PRD Section 9 (MVP Scope), 13 (Out of Scope).*

12. **Next Actions** — Concrete next steps, owners, and decision criteria.

13. **PRD Readiness Checklist** — Explicit checklist of what's ready to flow into `/prd` and what still needs work:
    - [ ] Problem statement grounded in evidence
    - [ ] Hypothesis is falsifiable and measurable
    - [ ] Target personas identified
    - [ ] MVP scope defined (not too basic, not too complex)
    - [ ] Success metrics identified with thresholds
    - [ ] Key risks and mitigations documented
    - [ ] Dependencies identified

### Memo Storage

Save to `data/deliberations/` (create directory if needed).

---

## Integration with `/prd`

The memo is designed as a **PRD input artifact**. The integration should work as follows:

1. After `--deliberate` produces a memo, suggest: *"Ready to generate a PRD from this memo? Run `/prd` and reference memo `memo-2026-03-31-001`."*

2. When `/prd` is invoked with a linked memo, it should be able to pre-populate:
   - Problem Statement (from memo Section 3)
   - Hypothesis (from memo Section 4)
   - Personas and User Stories seeds (from memo Section 5 — User Impact)
   - Functional/Non-Functional Requirements seeds (from memo Section 6 — Feasibility)
   - Success Metrics seeds (from memo Sections 7-8 — Business Case + Evidence Gaps)
   - MVP Scope (from memo Section 11)
   - Risks (from memo Section 10 — Dissent + Section 6 — Feasibility)
   - Out of Scope (from memo Sections 10-11)

3. The PRD still goes through its full generation and self-eval process — the memo provides a head start, not a bypass. The PRD subagent enriches and formalizes the memo's seeds using linked insights.

> **Note**: The exact `/prd` integration (how it detects and ingests a memo) is deferred to implementation. The memo structure above is designed to make that integration straightforward — each memo section maps to specific PRD sections.

---

## The Full Workflow

```
/grill-me --brainstorm     → flesh out a half-formed idea collaboratively
         |
         v
/grill-me --debate         → stress-test your reasoning, walk the decision tree
         |
         v
/grill-me --deliberate     → board deliberates, produces decision memo
         |
         v
/prd (with linked memo)    → generate a full PRD pre-populated from the memo
```

Each mode builds on the prior conversation context. The user can enter at any stage — `--deliberate` works standalone with a fresh problem statement, or it can synthesize from a prior `--brainstorm` / `--debate` conversation.

---

## Implementation Notes

- **No external dependencies** — runs entirely in Claude Code using the Agent tool for subagents. No Pi, no Bun, no custom TUI.
- **No live streaming TUI** — the user gets progress updates between rounds ("Round 1 complete — 3 tensions identified, running follow-ups...") rather than watching agents respond in real-time.
- **No persistent sessions** — each subagent call is one-shot. Prior round context is passed forward in the prompt. This uses more tokens but works within Claude's 1M context.
- **Cost bounded** — deliberation is limited to 2-3 rounds. No time/budget constraint engine needed; the round limit keeps cost predictable.
- **Board prompts stored as markdown** — one file per persona in a dedicated directory (e.g., `.claude/agents/board/`). Adding a member = new markdown file + roster entry.

---

## Files That Would Be Created

| File | Purpose |
|------|---------|
| `.claude/agents/board/user-advocate.md` | User Advocate persona prompt |
| `.claude/agents/board/data-analyst.md` | Data Analyst persona prompt |
| `.claude/agents/board/engineering-reality.md` | Engineering Reality persona prompt |
| `.claude/agents/board/business-strategist.md` | Business Strategist persona prompt |
| `.claude/agents/board/contrarian.md` | Contrarian persona prompt |
| `data/deliberations/.gitkeep` | Memo output directory |

## Files That Would Be Modified

| File | Change |
|------|--------|
| `.claude/commands/grill-me.md` | Add `--deliberate` mode, rename `--conversation` to `--brainstorm`, rename default to `--debate`, add bare mode picker |
| `.claude/commands/prd.md` | Add memo ingestion path (deferred to implementation) |
| `data/meta/counters.json` | Add `"memo": 0` counter |
| `data/meta/tags.json` | Add `"deliberation"` tag |
| `CLAUDE.md` | Document new mode and memo schema |

---

## Open Questions

1. **Context carryover** — When `--deliberate` follows a `--brainstorm`/`--debate` session, how much of the prior conversation should be summarized into the brief vs. passed raw? Summarization loses nuance; raw context burns tokens.
2. **Board member expertise persistence** — Should board members accumulate expertise across deliberations (like CEO Agents' scratch pads), or start fresh each time? Persistence adds complexity but improves quality over time.
3. **Memo versioning** — If the user runs `--deliberate` multiple times on the same topic, should memos be versioned (v1, v2) or independent artifacts?
4. **PRD auto-link** — Should the memo frontmatter include `linked_insights` if insights were referenced during brainstorm/debate, so the PRD inherits them automatically?
5. **Custom board rosters** — Should the user be able to pass a roster flag (e.g., `--deliberate --board=technical`) for different board compositions, or is one default roster sufficient for now?
