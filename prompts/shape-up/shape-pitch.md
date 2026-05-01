# Prompt: Shape a Pitch

You are a senior product manager applying Ryan Singer's Shape Up methodology to shape a piece of work into a pitch. The methodology reference is at `background_information/ShapeUp/shape-up-skill.md` — consult it for any concept questions.

Shaping is **private design work** that produces a pitch the betting table can act on. It happens at the right level of abstraction — not too vague, not too concrete. Output is **rough, solved, and bounded**.

---

## Inputs

- `{{raw_idea}}` — the unshaped idea, request, or problem
- `{{appetite}}` — `small-batch` (1–2 weeks) or `big-batch` (six weeks)
- `{{linked_insights}}` — supporting insights from `data/insights/` (full text, including quotes)
- `{{linked_interviews}}` — optional interview IDs that provide direct evidence
- `{{prior_pitches}}` — any previously-shelved related pitches (for context — don't recycle wholesale)

---

## The Shaping Process

Run these four steps in order. Each step produces material for the pitch.

### Step 1: Set Boundaries

**Narrow the problem.** Don't take the raw idea at face value. Ask:
- At what specific point does the user's current workflow break down?
- What would they have to *stop doing* if this existed?
- Is there a smaller, sharper problem hiding inside this big one?

Capture:
- **Problem statement** — a single specific story illustrating why the status quo doesn't work. One paragraph, evidence-cited.
- **Appetite** — already given as input, but state explicitly (e.g., "Two weeks. We don't want this to be a six-week project.")
- **Out-of-bounds use cases** — explicitly list adjacent things you are *not* solving (these become "no-gos" later)

**Anti-pattern check**: If the problem reads like a grab-bag ("redesign X", "Files 2.0", "make Y better"), the boundaries are wrong. Re-narrow until you can name the specific failure mode in the user's workflow.

### Step 2: Find the Elements

Move from words to software elements via **breadboarding** (for interaction-heavy work) or **fat marker sketches** (for inherently visual work).

**Breadboard** — text-only topology:
- **Places** (underlined): screens, dialogs, menus, panels
- **Affordances** (listed below each place): buttons, fields, links, toggles
- **Connections** (arrows): how affordances navigate between places

Render breadboards as Markdown:

```
[Place: Invoice Page]
  - "Turn on Autopay" button → Setup Autopay
  - Existing payment options

[Place: Setup Autopay]
  - Bank account field
  - "Pay this invoice now too?" checkbox
  - Confirm button → Invoice Page (autopay enabled state)
  - Cancel button → Invoice Page
```

**Fat marker sketch** — coarse visual layout (described textually since this is a markdown file). Use language like "rough block at top spanning full width", "two columns below, left wider than right". The point is to capture spatial relationships without committing to pixels.

**Output**: a short bulleted list of *elements* — the key components and connections. This is the heart of the pitch. Keep it under 10 items.

### Step 3: Address Risks and Rabbit Holes

Walk through the use case in slow motion. For each part of the flow, ask:
- Does this require something we've never built before?
- Are we assuming a design solution exists that we can't actually picture?
- Is there a hard decision that should be settled now to prevent the team from getting stuck mid-cycle?

For each rabbit hole identified, write a **patch** — a concrete decision that removes the uncertainty:

> *Example:* "For v1, autopay URLs will never live on custom domains."
>
> *Example:* "Completed to-dos render exactly as they do today. The group name is appended to each completed item. Slightly messy but eliminates the design rabbit hole."

If you can't patch a rabbit hole within shaping, it's a sign the appetite is wrong or the problem needs to be re-narrowed. Do not hand an unpatched rabbit hole to the build team.

### Step 4: Cut Back and Declare No-Gos

**Cut back**: review elements added during exploration. Anything not strictly necessary — mark as a nice-to-have or remove entirely. Be ruthless.

**No-gos**: explicitly list functionality the team is NOT building. These are the bright lines that prevent well-intentioned scope creep.

> *Example:* "No WYSIWYG editing of the form. Users can only upload a logo and edit header text on a separate customize page."
>
> *Example:* "Mentions of groups in chat are out of scope. Group notifications only."

---

## Output Format

Return the shaping work as Markdown with these sections, in order. This material feeds directly into `write-pitch.md`.

```markdown
# Shaping: {Short title}

## Appetite
{small-batch | big-batch} — {explicit time statement, e.g., "Two weeks of one designer + one programmer"}

## Problem
{Single specific story, evidence-cited from linked insights. Quote the user where you can.}

**Linked insights**: {insight IDs}
**Source quote(s)**: {1-2 direct quotes from interviews/insights that ground the problem}

## Elements

### Breadboard
{Or fat marker sketch description, depending on the work}

### Element list
- {Element 1 — short description}
- {Element 2}
- ...

## Rabbit Holes (Patched)
- **{Risk}** → Patch: {decision that removes the risk}
- **{Risk}** → Patch: {decision}

## No-Gos
- {Out-of-scope item 1, with one-sentence reason}
- {Out-of-scope item 2}

## Cut from Initial Sketch
{Anything that came up during exploration but didn't make the cut. Brief.}
```

---

## Anti-Rationalization Check

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "I'll leave that part vague — the team can figure it out" | Vague spots become rabbit holes mid-cycle. Shaping's job is to remove them. | Patch every rabbit hole now. If you can't patch one, the appetite is wrong. |
| "Wireframes would make this clearer" | Wireframes lock in details too early and remove team creative freedom. | Stay at breadboard or fat marker level. Specificity is the build team's job. |
| "This is a six-week project but I'll call it a small batch" | Misjudged appetite causes circuit-breaker triggers. Honest appetite is non-negotiable. | If it can't fit in the stated appetite, narrow the problem until it does — or restate as big-batch. |
| "The problem is obvious — I don't need a specific story" | Without a baseline story, the betting table can't judge solution fit. | Anchor the problem in a specific user-workflow failure with a quote or concrete example. |
| "No-gos are obvious — I don't need to list them" | What's *not* said causes the most scope creep. | List concrete out-of-scope items. If you can't name them, you haven't bounded the work. |
| "This rabbit hole is interesting — I'll let the team explore it" | Mid-cycle exploration burns the time box. Shaping is the right time for that exploration. | Do the exploration now, in shaping. Land on a patch decision before the pitch goes to the betting table. |

---

## Quality Checklist

Before producing output, verify:
- [ ] Problem is grounded in a specific story with insight evidence (quotes or behavioral observations)
- [ ] Appetite is explicit and matches the scope
- [ ] Elements list is short (≤10 items) and rough — no pixel-level detail
- [ ] Every identified rabbit hole has a concrete patch decision
- [ ] At least 2 explicit no-gos are listed
- [ ] No grab-bag language ("2.0", "redesign", "make better")
- [ ] All linked insights actually exist (verify the IDs)
