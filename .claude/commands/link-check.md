# Link Check

Verify all cross-links across the entire `data/` directory. Reports broken links, orphaned artifacts, and missing connections. No questions — runs immediately.

## Process

Launch an `Explore` subagent to scan all data files and verify every cross-reference.

### 1. Scan All Artifacts

Read every non-.gitkeep file in `data/` (excluding `data/meta/` and `data/evals/golden/`). Parse frontmatter (YAML for .md, JSON for .json).

### 2. Check Forward Links

For every link field, verify the target exists:

| Source Field | Expected Target |
|-------------|-----------------|
| `linked_interviews: [ID]` | File in `data/interviews/` with matching `id` |
| `linked_insights: [ID]` | File in `data/insights/` with matching `id` |
| `linked_prds: [ID]` | File in `data/prds/` with matching `id` |
| `prd_id: ID` | File in `data/prds/` with matching `id` |
| `okr_ids: [ID]` | File in `data/strategy/okrs/` with matching `id` |
| `roadmap_ids: [ID]` | File in `data/strategy/roadmap/` with matching `id` |
| `linked_outcomes: [ID]` | File in `data/outcomes/records/` with matching `id` |

Report any ID that doesn't resolve to an existing file.

### 3. Check Tag Validity

Read `data/meta/tags.json`. For every `tags` field in every artifact, verify each tag exists in the taxonomy.

### 4. Check Orphans

Find artifacts with no inbound links:
- Insights not referenced by any PRD's `linked_insights`
- Interviews not referenced by any insight's `linked_interviews`
- PRDs not referenced by any GTM draft's `prd_id`, test case's `prd_id`, or roadmap item's `linked_prds`

### 5. Check Workflow Rule Compliance

- PRDs with empty `linked_insights` (violates rule #1)
- Insights with empty `linked_interviews` (violates rule #2)
- PRDs missing Given/When/Then in body (violates rule #3)

## Output

```
LINK CHECK — {date}

BROKEN LINKS ({n})
  {artifact ID} → {field}: {broken ID} (target not found)
  ...

INVALID TAGS ({n})
  {artifact ID}: tag "{tag}" not in tags.json
  ...

ORPHANED ARTIFACTS ({n})
  {artifact ID} — {type} — no inbound links
  ...

RULE VIOLATIONS ({n})
  {artifact ID} — {violation description}
  ...

ALL CLEAR: {n} artifacts checked, {n} links verified, {n} issues found
```

## Rules

- Use an `Explore` subagent (read-only)
- Skip `.gitkeep` files
- Skip `data/meta/` and `data/evals/golden/`
- Report issues grouped by severity: broken links first, then invalid tags, then orphans, then rule violations
- If everything is clean, say so clearly
