# Prompt: Map the Scopes

You are helping a Shape Up build team factor an in-progress project into **scopes** — independent, finishable slices of work that reflect the actual structure of the problem (not org structure). Scopes give the team the high-level language of the project and make hill-chart progress visible.

The methodology reference is at `background_information/ShapeUp/shape-up-skill.md` (§6.3).

---

## When to Run This

Scope mapping happens **after** the team has done a few days of real work — long enough to discover what depends on what. Doing this on day 1 produces imagined scopes that turn out wrong. Wait until the team has at least one piece working end-to-end (see "Get One Piece Done", §6.2).

Re-run as needed: scopes evolve. They start fuzzy, sharpen in the first week or two, and may get renamed or reorganized when natural boundaries reveal themselves.

---

## Inputs

- `{{pitch}}` — full text of the shaped pitch
- `{{cycle_id}}` — the active cycle ID
- `{{tasks}}` — the team's running list of imagined + discovered tasks (free-form, may be a brain dump)
- `{{prior_scope_map}}` — the previous scope map for this cycle, if one exists

---

## The Process

### Step 1: Read what's actually been built

Before drawing scopes, look at what exists:
- What's been demoed?
- What end-to-end slices work?
- What tasks did the team discover (vs. imagine) in the first few days?

The discovered tasks reveal the real structure. Use them as the primary input.

### Step 2: Group by structure of the work, NOT by role

**Wrong**: Designer tasks list, Programmer tasks list. These never add up to finished things.

**Right**: Scopes named after the work itself — "Locate Drafts", "Visibility Toggle", "Send Flow", "Setup Page". Each scope contains design + back-end + integration tasks together.

The fundraising-event analogy from §6.3: organizing by "Alice's tasks / Bob's tasks / Carol's tasks" makes it impossible to see if the event is coming together. Organizing by "Food Menu / Venue Setup / Light/Sound" gives a clear picture of what's done and what's outstanding.

### Step 3: Name scopes well

Good scope names:
- **Specific to this project** — "front-end" or "bugs" are grab-bags that can never be declared done
- **Independently completable** — you should be able to ship a scope without finishing other scopes
- **Unique vocabulary** — the names should become the team's natural shorthand for the project

If you can't say a scope is "done" without checking three other scopes, it's not really a scope — it's a layer.

### Step 4: Spot the shapes

Categorize each scope:
- **Layer cake**: front-end and back-end work are roughly proportional. UI surface area is a decent effort proxy. Default for most scopes.
- **Iceberg**: back-end or front-end complexity dominates. Factor the dominant side into its own scope. Always question: is this complexity actually necessary?
- **Chowder**: a list for tasks that don't fit anywhere yet. Keep it short (3–5 items). If chowder grows, an undiscovered scope is hiding inside.

### Step 5: Mark must-haves vs. nice-to-haves

Within each scope, classify every task:
- **Must-have** — blocks the scope from being called done
- **Nice-to-have** — prefix the task with `~`, gets cut if time runs out

The act of marking something `~` is the first act of scope hammering. Be ruthless. Most "improvements" the team thinks of mid-cycle are nice-to-haves.

### Step 6: Sanity checks

Before saving the map, verify:

**Signs scopes are right**:
- You can see the whole project — nothing important hides in the details
- Conversations about the project become natural because scope names are the right vocabulary
- When new tasks come up, you immediately know which scope they belong to

**Signs scopes need redrawing**:
- Hard to say how "done" a scope is — tasks inside are unrelated to each other
- Name isn't unique to this project (grab-bag warning)
- Scope is too large — dozens of tasks means it's a project of its own

---

## Output Format

Save as part of the cycle artifact at `data/shape-up/cycles/{cycle-id}.md` under a `## Scope Map` section, OR as a standalone Markdown block returned to the user for review. Format:

```markdown
## Scope Map (as of {ISO date})

### {Scope Name 1} — {layer-cake | iceberg | chowder}

**Must-haves**:
- [ ] {task}
- [ ] {task}
- [x] {completed task}

**Nice-to-haves** (cut if time runs out):
- [ ] ~{task}
- [ ] ~{task}

---

### {Scope Name 2} — {shape}

**Must-haves**:
- [ ] {task}

**Nice-to-haves**:
- [ ] ~{task}

---

### Chowder (unsorted)
- [ ] {task that doesn't fit a scope yet}
- [ ] {task}

---

### Cut from this cycle
- {item that was originally in scope but got hammered out, with one-line reason}
```

---

## Anti-Rationalization Check

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "Let's organize tasks by who's doing them — designers vs programmers" | Role-based lists don't add up to finished things. The team can't see project progress. | Organize by structure of the work. Mixed-role tasks within each scope. |
| "We can map scopes on day 1" | Imagined scopes from day 1 are usually wrong. Real structure emerges from doing the work. | Wait until the team has shipped at least one end-to-end slice (3–5 days in). |
| "Front-end / Back-end / Bugs are good scopes" | These are grab-bags that can never be done. Bugs especially keep growing. | Use specific, project-unique names. Move bugs into the relevant scope or chowder. |
| "Everything in this scope is a must-have" | Almost never true. Some are vanity polish. | Be ruthless with `~` marks. Default to nice-to-have unless the scope literally cannot ship without it. |
| "This 30-task scope is fine — it's a big area" | A scope with 30 tasks is its own project and has lost the benefit of being trackable. | Break it into 2–3 sub-scopes by sub-structure. |
| "Chowder is normal — let it be 15 items" | Long chowder = undiscovered scope. | Keep chowder ≤5. If it grows, look for the hidden structure. |

---

## Quality Checklist

- [ ] Each scope has a project-specific, non-grab-bag name
- [ ] Scopes are organized by work structure, not by role
- [ ] Each task is marked must-have or `~` nice-to-have
- [ ] Chowder is ≤5 items
- [ ] No scope contains >15 tasks (split if so)
- [ ] Scope shapes are noted (layer-cake / iceberg / chowder)
- [ ] At least one scope can be plausibly demoed independently of the others
