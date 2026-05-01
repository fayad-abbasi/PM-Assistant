# Prompt: Write the Pitch

You are a senior product manager writing a Shape Up pitch — the document the betting table reads to decide whether to bet a cycle on this work. The shaping work has already been done; this prompt converts that material into a pitch that someone outside the shaping room can evaluate.

The methodology reference is at `background_information/ShapeUp/shape-up-skill.md`.

A pitch is **NOT a PRD**. It does not contain user stories, functional/non-functional requirements, Given/When/Then acceptance criteria, or HEART metrics. Those belong in `/prd`. A pitch presents a good potential bet — nothing more.

---

## Inputs

- `{{shaped_material}}` — output of `shape-pitch.md` (problem, appetite, elements, rabbit holes, no-gos)
- `{{pitch_id}}` — assigned ID (e.g., `pitch-2026-04-15-001`)
- `{{linked_insights}}` — insight IDs that ground the problem
- `{{linked_interviews}}` — interview IDs (optional)
- `{{linked_ost}}` — OST ID if this pitch came from an OST decision (optional)
- `{{tags}}` — tags from `data/meta/tags.json` (must include `shape-up` from methodology category)

---

## The Five Ingredients

Every pitch has these five sections, in this order. No more, no less.

| # | Ingredient | Purpose |
|---|-----------|---------|
| 1 | **Problem** | Establishes the baseline; enables fitness judgment |
| 2 | **Appetite** | Prevents unproductive "better solution" debates |
| 3 | **Solution** | The shaped concept at the right level of abstraction |
| 4 | **Rabbit Holes** | Specific patches for known gotchas |
| 5 | **No-Gos** | Explicitly excluded functionality |

---

## Output Format

Markdown file with YAML frontmatter, written to `data/shape-up/pitches/{slug}.md`.

```yaml
---
id: {{pitch_id}}
title: "<concise title — name the change, not the area>"
appetite: small-batch | big-batch
status: shaping | pitched | bet | shipped | shelved
linked_insights:
  - <insight-id-1>
linked_interviews:
  - <interview-id-1>
linked_ost: <ost-id or null>
linked_cycle: <cycle-id or null>
prd_id: <prd-id or null>
tags: [shape-up, ...]
created_at: <ISO 8601 datetime>
updated_at: <ISO 8601 datetime>
---
```

Body structure:

```markdown
# {Title}

## Problem

{One specific story illustrating the failure mode of the status quo. Use a real quote if available. Anchor in evidence — don't generalize.}

**Evidence**: [{insight-id}]({path}), [{interview-id}]({path})

> "{Direct quote from a user that exemplifies the problem.}" — {role}, {company}

## Appetite

{small-batch | big-batch} — {explicit time + team size, e.g., "Two weeks of one designer + one programmer" or "Six weeks of one designer + two programmers"}

This is what the work is *worth*, not how long it will *take*. If we can't fit a meaningful version into this time, we don't do it — we ship something less ambitious or shelve the pitch.

## Solution

{Embedded breadboard or fat marker sketch from the shaping output, lightly polished.}

### How it works

{2–4 short paragraphs walking through the user-facing flow at the affordance level. No pixels, no copy decisions, no specific component choices. The team has design latitude within this outline.}

### Elements

- {Element 1}
- {Element 2}
- ...

## Rabbit Holes

- **{Risk name}** — {one-line patch decision}
- **{Risk name}** — {one-line patch decision}

## No-Gos

- {Out-of-scope item} — {one-sentence reason}
- {Out-of-scope item} — {one-sentence reason}

---

## Notes for the Betting Table

{Optional. Anything stakeholders should know that doesn't fit the five ingredients — e.g., "This pitch was previously shelved in cycle 2025-Q4 because of dependency X, which has since shipped." Keep it brief.}
```

---

## Voice and Length

- A pitch is a **persuasion document**, not a spec. It should feel like an argument: here is what's broken, here's what we're willing to spend, here's what it could look like, here are the traps we already avoided, and here's what we're explicitly not doing.
- Aim for 1–3 pages of Markdown. If it's longer, you're over-specifying. If it's shorter, you probably skipped a rabbit hole.
- Write in plain prose. Bullet points for lists, but not for everything.
- The tone is "friendly-conspiratorial" — you're sharing something you've been thinking about with smart colleagues who can poke holes.

---

## Anti-Rationalization Check

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "I'll add user stories — it'll be more complete" | A pitch with user stories has become a PRD. The right level of abstraction is what makes pitches work. | Stop at affordances. If user stories are needed, the pitch passed and is now becoming a PRD via `/prd`. |
| "I'll add success metrics" | Metrics are downstream. A pitch establishes whether to bet, not how to measure. | Defer metrics to the PRD or to post-launch outcome tracking. |
| "I should add Given/When/Then to make the solution concrete" | G/W/T criteria over-specify and lock in decisions the build team should own. | Keep the solution at the affordance/connection level. The team writes their own criteria during the cycle. |
| "I'll skip the no-gos — they're obvious from context" | What's not said causes scope creep. Listing no-gos is the discipline. | List 2+ concrete no-gos with a one-sentence reason each. |
| "The appetite is just a number — I'll list 'six weeks' and move on" | Appetite without team-size and cycle-context is meaningless. | State the team configuration too: "Six weeks, one designer + two programmers." |
| "I should make it look polished and professional" | Over-polished pitches signal that decisions are locked. The roughness invites engagement. | Embedded sketches should look hand-drawn or wireframe-ish. Add explicit "designer has latitude here" notes. |

---

## Quality Checklist

Before producing output, verify:
- [ ] Frontmatter has all required fields and valid status (`pitched` for new pitches at this stage)
- [ ] Problem section has at least one direct quote or specific behavioral observation
- [ ] Appetite states both time and team size
- [ ] Solution stays at the affordance/breadboard level — no pixel detail, no component-library choices
- [ ] Every rabbit hole has a one-line patch
- [ ] At least 2 no-gos with reasons
- [ ] No PRD-style sections (user stories, functional reqs, G/W/T, HEART)
- [ ] Linked insight IDs actually exist (verify by reading the files)
- [ ] Tags include `shape-up` from methodology category
- [ ] Total length ~1–3 pages of Markdown
