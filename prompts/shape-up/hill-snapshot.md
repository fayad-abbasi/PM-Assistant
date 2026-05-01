# Prompt: Capture a Hill-Chart Snapshot

You are capturing a point-in-time snapshot of every scope's position on the hill chart. Snapshots are immutable — each is a separate file. Comparing snapshots over time gives the **time-lapse view** that makes hill charts powerful: a dot that moves means progress; a dot stuck in place is a raised hand for "something's wrong here."

The methodology reference is at `background_information/ShapeUp/shape-up-skill.md` (§6.4).

---

## The Hill Metaphor

Every piece of work has two phases:

**Uphill** — figuring it out. Unknown territory. Open questions. Problem-solving mode. You don't yet know what you don't know.

**Downhill** — executing. Everything visible. All remaining steps known. The feeling shifts from "I'm not sure what I'm doing" to "I know exactly what to do."

The **top of the hill** is the moment all unknowns are resolved and only execution remains.

---

## Position Values

Each scope is positioned 0–100 along the hill arc:

| Position | Meaning |
|---|---|
| **0–15** | Just started. Lots of unknowns. Nothing built yet. |
| **15–40** | Some direction. Approach is forming. Still problems to solve. Real work starting. |
| **40–60** | Approaching the top. Most uncertainty resolved. A working slice or strong prototype exists. |
| **60–80** | Over the hill. Approach validated through actual building. Just execution left. |
| **80–95** | Most execution done. Final polish, edge cases, integration. |
| **95–100** | Done. Merged, deployed, demoable. |

**Rule** (§6.4 "Build Your Way Uphill"): Don't declare a scope past 50 based on thinking alone. Validate the approach by building. Reaching the top of the hill should mean "I've built enough that I don't believe there are other unknowns."

---

## Inputs

- `{{cycle_id}}` — the active cycle
- `{{scope_map}}` — current scope map from `data/shape-up/cycles/{cycle-id}.md`
- `{{prior_snapshot}}` — the most recent snapshot file in `data/shape-up/hill-charts/` for this cycle (for comparison)
- `{{user_updates}}` — the user's verbal/text update on each scope

---

## The Process

### Step 1: For each scope, ask three questions

For every scope in the current scope map (excluding chowder), prompt the user:

1. **Where is this scope on the hill right now?** (0–100, or qualitative — "still uphill", "just over the top", "almost done")
2. **What changed since the last snapshot?** (one sentence — what progress, what got cut, what got discovered)
3. **Anything stuck?** (a scope that hasn't moved in two snapshots is a raised hand — surface the underlying problem)

### Step 2: Compare to the prior snapshot

For each scope, compute the delta:
- **Moved forward** ✓ — progress, no flags
- **Moved backward** ⚠ — uphill regression. Usually means a hidden unknown surfaced. Common, healthy when it happens early.
- **Stuck (no movement)** 🛑 — first stuck snapshot is a yellow flag, second is red. Surface the problem, name what's needed to unstick.

A backward move is *not* a failure — it's the system working. The whole point of the hill chart is that hidden uncertainty surfaces visibly. Hidden unknowns become explicit when the dot slides back.

### Step 3: Sequence check

Look at the overall pattern. Per §6.4 "Solve in the Right Sequence":
- The **scariest, most novel** scopes should be moving uphill *first*. Push uncertainty over the top early.
- **Routine, well-understood** scopes can stay at the bottom early in the cycle — they'll move fast once started.
- If routine work is far along but the novel scope hasn't moved off the bottom, the team is sequencing backwards. Flag it.

### Step 4: Time-budget check

Where you are in the cycle should match the hill positions:

| Cycle progress | Healthy hill positions |
|---|---|
| Week 1 | At least one scope moving up; novel scopes prioritized |
| Week 3 (mid-cycle) | All scopes at least started; novel scopes near or over the top |
| Week 5 | All scopes downhill or close to it |
| Week 6 | Everything 80+; final polish |

If you're in week 5 and a scope is still uphill, the project is in trouble. Either scope-hammer aggressively, cut the scope entirely, or accept that the circuit breaker may fire.

---

## Output Format

Each snapshot is a new file at `data/shape-up/hill-charts/hill-{cycle-id}-{ISO-date}.json`:

```json
{
  "id": "hill-{cycle-id}-{YYYY-MM-DD}",
  "cycle_id": "{cycle-id}",
  "snapshot_at": "{ISO 8601 datetime}",
  "week_of_cycle": 1,
  "scopes": [
    {
      "name": "{scope name}",
      "position": 35,
      "phase": "uphill",
      "delta_from_prior": "+15",
      "note": "{one-sentence note from the user about what changed}",
      "flag": null
    },
    {
      "name": "{scope name}",
      "position": 20,
      "phase": "uphill",
      "delta_from_prior": "0",
      "note": "Stuck on data model question — not sure if we need a join table.",
      "flag": "stuck"
    }
  ],
  "sequence_check": "{healthy | novel-work-deferred | routine-ahead-of-novel}",
  "time_budget_check": "{healthy | behind-schedule | at-risk}",
  "user_summary": "{1–3 sentence narrative of where the cycle stands}"
}
```

After writing, also generate a human-readable summary the user can drop into a status update:

```markdown
## Hill Chart — {Cycle Title} — Week {N} of 6 ({date})

| Scope | Position | Phase | Δ | Flag |
|---|---|---|---|---|
| {name} | 35 | uphill | +15 | — |
| {name} | 20 | uphill | 0 | 🛑 stuck |
| {name} | 70 | downhill | +25 | — |

**Sequence**: {assessment}
**Time budget**: {assessment}

**Notes**:
- {Per-scope notes from the user, one bullet each}

**What needs attention**: {specific call-out — usually about a stuck scope}
```

---

## Anti-Rationalization Check

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "I think this scope is past the top — I've thought it through" | Top of hill = validated by building, not by thinking. Common cause of false confidence. | Cap thinking-only progress at 50. Past 50 requires actual built artifacts. |
| "This dot didn't move — I'll just nudge it up a little" | Sandbagging the chart hides the real signal. The whole value is in surfacing stuck work. | Leave the dot where it is. Name what's stuck. The hill chart is a feedback mechanism, not a morale chart. |
| "Backward movement is bad — let's avoid it" | Backward movement = a hidden unknown surfaced. That's the system working. | Treat backward movement as healthy *when it happens early*. It's only alarming if it happens in week 5+. |
| "Routine scopes go up first, novel scopes later" | Backwards sequencing. Novel work is where the unknowns are — it must go first. | Push the scariest scope uphill first. Save routine work for the back half. |
| "We're at week 5 and one scope is still at 30 — but it'll move fast once we start" | Famous last words. If it hasn't moved by week 5, the cycle will overrun. | Either cut the scope, scope-hammer it down, or surface the circuit-breaker risk to the betting table now. |

---

## Quality Checklist

- [ ] Every non-chowder scope has a position
- [ ] Position 50+ is justified by built artifacts, not just thinking
- [ ] Each scope has a delta from the prior snapshot (or "first snapshot" if none)
- [ ] Stuck scopes are flagged and the underlying issue is named
- [ ] Sequence check evaluates whether novel work is ahead of routine work
- [ ] Time-budget check compares cycle week to expected hill positions
- [ ] Output saved as a *new* file (not overwriting prior snapshots)
