# Quality Check

Post-generation quality checker that validates an artifact's structural integrity and content quality. Can be run standalone or is called automatically by generation commands.

## Usage

- **Standalone**: `/quality-check {artifact-id or file path}` — check a specific artifact
- **Auto**: Called by `/discover`, `/prd`, `/gtm`, `/ux` after generating artifacts

## Process

### 1. Structural Validation

Read the artifact and check:

- **Frontmatter completeness**: All required fields present per schema in CLAUDE.md
  - `id` exists and follows the `{type}-{date}-{NNN}` pattern
  - `title` exists and is non-empty
  - `created_at` exists and is valid ISO datetime
  - Type-specific required fields are present (e.g., `linked_insights` for PRDs, `linked_interviews` for insights)
- **Tag validity**: All tags in `tags` array exist in `data/meta/tags.json`
- **Cross-link integrity**: All IDs in link fields (`linked_interviews`, `linked_insights`, `okr_ids`, `roadmap_ids`, `prd_id`, `linked_outcomes`) resolve to existing files
- **Status validity**: Status value matches the allowed enum for the artifact type
- **Workflow rules**:
  - PRDs must have at least one linked insight
  - Insights must have at least one linked interview
  - Acceptance criteria must use Given/When/Then format (PRDs only)
  - GTM drafts must have a `prd_id`

### 2. Content Quality (if rubric exists)

If the artifact type has a rubric, run an eval:

| Artifact Type | Rubric |
|---------------|--------|
| Insight | `prompts/evals/rubric-interview.md` |
| PRD | `prompts/evals/rubric-prd.md` |
| GTM Draft | `prompts/evals/rubric-gtm.md` |
| Journey Map | `prompts/evals/rubric-journey.md` |

- Read the rubric and `prompts/evals/judge-prompt.md`
- Score each dimension (1-5 scale)
- Calculate average score

### 3. Report

```
QUALITY CHECK — {artifact ID}

STRUCTURE: {PASS | FAIL}
  {list any structural issues, or "All required fields present"}

LINKS: {PASS | FAIL}
  {list any broken links, or "All {n} cross-links verified"}

TAGS: {PASS | FAIL}
  {list any invalid tags, or "All {n} tags valid"}

RULES: {PASS | FAIL}
  {list any rule violations, or "All workflow rules satisfied"}

CONTENT QUALITY: {score}/5
  {dimension scores and top improvement suggestion}

VERDICT: {PASS | NEEDS FIXES}
```

### 4. Auto-Fix (when called by generation commands)

When called as part of a generation pipeline (not standalone):
- If STRUCTURE, LINKS, TAGS, or RULES fail → fix automatically and re-write the file
- If CONTENT QUALITY average < 3.5 → fix the lowest-scoring dimensions and re-write
- Re-run the check after fixes to confirm pass
- Maximum 2 fix iterations — if still failing after 2 rounds, present to user with issues flagged

## Rules

- Use `Explore` subagent for read-only checks when run standalone
- When called by generation commands, the generating subagent handles fixes inline
- Always save eval results to `data/evals/` when content quality is scored
- Read and update `data/meta/counters.json` when saving eval results
- Be honest — the point is quality improvement, not rubber-stamping
