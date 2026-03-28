# Refresh

Re-inject session context on demand. Same data as the session-start hook, but runnable mid-session to get a fresh snapshot after making changes.

## Process

Run the session-context hook script and display the output:

1. Read `data/meta/learnings.md` — accumulated corrections
2. Scan `data/strategy/okrs/` — active OKR status and key result progress
3. Scan `data/prds/` — PRD statuses and priorities
4. Scan `data/stakeholder/decisions/` — recent decisions (last 5)
5. Scan `data/stakeholder/meetings/` — open commitments with aging (flags >3 days old)
6. Scan `data/stakeholder/people/` — count of tracked stakeholder profiles

## Output

Present a concise context summary directly in the conversation:

```
SESSION CONTEXT REFRESHED — {date}

LEARNINGS: {n} corrections logged
OKRs: {n} active — {brief status}
PRDs: {n} total ({n} draft, {n} review, {n} approved)
RECENT DECISIONS: {list last 3}
OPEN COMMITMENTS: {n} total, {n} overdue (>3 days)
STAKEHOLDERS: {n} profiles tracked

{any overdue commitments listed with aging}
```

## When to Use

- After a long session where you've created/updated multiple artifacts
- When switching focus areas mid-session (e.g., from discovery to strategy)
- Before starting a new task to confirm current state
- Anytime you want to see where things stand without opening `/pm-dash`

## Rules

- No questions — runs immediately
- Lighter than `/pm-dash` — context summary only, no data quality flags or traceability health
- Read-only — does not modify any files
