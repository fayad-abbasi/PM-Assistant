# Next

"What should I work on next?" — Analyzes data quality flags, workflow gaps, and stale artifacts to recommend the highest-impact next action. No questions — runs immediately.

## Process

Launch an `Explore` subagent to scan all `data/` directories and generate prioritized recommendations.

### 1. Scan for Issues

Check the same data quality flags as `/pm-dash`:

**High priority (blocking):**
- Broken cross-links (broken traceability chain)
- PRDs with empty `linked_insights` (violates workflow rules)
- Invalid tags not in `data/meta/tags.json`

**Medium priority (quality gaps):**
- **Overdue commitments** — action items from meetings older than 3 days with status "open" (check `data/stakeholder/meetings/` action_items)
- Unanalyzed interviews (`status: raw`) — insights waiting to be extracted
- Draft PRDs older than 7 days — stale, need review or advancement
- PRDs without test cases — untested requirements
- PRDs without GTM drafts — no go-to-market plan
- Active OKRs without outcome records — no progress tracking
- Insights not linked to any PRD — unused research

**Low priority (opportunities):**
- PRDs without journey maps — user experience not mapped
- Completed PRDs/periods with no retrospective
- Artifacts never evaluated by `/eval`
- Insights exist but no OST in `data/strategy/ost/` — discovery opportunity missed
- OST with `status: testing` has pending assumption tests — tests waiting for results
- OST with `status: testing` where all assumption tests are completed — ready to pick a winner

### 2. Score and Rank

For each issue found, assign a priority score:
- **Blocking issues**: 100 points each
- **Overdue commitments (>3 days)**: 90 points (promises made to people — trust at stake)
- **Unanalyzed interviews**: 80 points (raw data losing context over time)
- **Stale draft PRDs**: 70 points (momentum loss)
- **PRDs without test cases**: 60 points (quality risk)
- **Missing GTM**: 50 points (launch readiness gap)
- **Unused insights**: 40 points (wasted research)
- **Insights without an OST**: 45 points (jumping to PRD without structured exploration)
- **OST with pending assumption tests**: 75 points (active experiment needs data)
- **OST with all tests completed**: 85 points (decision bottleneck — winner ready to pick)
- **Missing journeys/retros/evals**: 20 points each

### 3. Present Top 3 Recommendations

```
NEXT — What needs attention

1. [HIGH] Analyze 2 raw interviews
   → Run `/discover` on initech-data-analyst-2026-03-07 and globex-engineering-lead-2026-03-06
   Why: Raw interviews lose context over time. These are {n} days old.

2. [MEDIUM] Create PRD from batch insight
   → Run `/prd` linked to insight-2026-03-12-001
   Why: 1 high-impact insight has no PRD yet — research sitting unused.

3. [LOW] Evaluate existing PRDs
   → Run `/eval` on prd-2026-03-10-001
   Why: Never scored — unknown quality risk.

4. [MEDIUM] Build an Opportunity Solution Tree
   → Run `/ost`
   Why: You have insights but no Opportunity Solution Tree — run `/ost` to explore solutions before jumping to a PRD.

5. [MEDIUM] Record assumption test results
   → Run `/discover test-assumption` on {OST title}
   Why: You have assumption tests to run on {OST title} — use `/discover test-assumption` to record results.

6. [HIGH] Pick a winning solution
   → Run `/ost resume` on {OST title}
   Why: All assumption tests recorded on {OST title} — run `/ost resume` to pick a winner and generate a PRD.

Quick wins: `/link-check` (verify data integrity) | `/weekly` (generate status report)
```

> **Note**: Items 4–6 are OST-specific recommendations. Include them only when the corresponding condition is detected. The numbered example above is illustrative — actual output shows exactly 3 recommendations, ranked by score.

## Rules

- Use an `Explore` subagent (read-only)
- Always show exactly 3 recommendations, ranked by priority score
- Each recommendation must include the specific command to run and the specific artifact(s) to act on
- Include a "Why" line explaining the urgency
- End with 1-2 "quick wins" — fast commands the user can run immediately
- Skip `.gitkeep` files and `data/meta/`, `data/evals/golden/`
