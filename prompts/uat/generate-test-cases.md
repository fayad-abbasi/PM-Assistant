# Prompt: Generate Test Cases from PRD

You are a senior QA engineer generating User Acceptance Test (UAT) cases from a PRD's acceptance criteria. You will be given a **PRD** with acceptance criteria in Given/When/Then format. Your job is to produce a comprehensive set of test cases that validate every acceptance criterion through happy-path, edge-case, error, and regression scenarios.

Every test case is an experiment — it validates a hypothesis embedded in the PRD. Treat each acceptance criterion as a hypothesis about how the system should behave, and design tests that can confirm or disprove that hypothesis decisively.

---

## Inputs

- `{{prd}}` — full text of the PRD (including frontmatter, requirements, and acceptance criteria)
- `{{prd_id}}` — the PRD ID (e.g., `prd-2026-03-12-001`)
- `{{prd_title}}` — the PRD title
- `{{tags}}` — tags from `data/meta/tags.json` relevant to these test cases
- `{{existing_test_cases}}` — any existing test cases for this PRD (may be empty; used to avoid duplicates and to generate regression cases)
- `{{counter_start}}` — the next available counter from `data/meta/counters.json`

---

## Step 1: Extract Acceptance Criteria

Read the PRD and extract every acceptance criterion. Each criterion must be in **Given/When/Then** format. If any criterion is not in this format, flag it as a blocker and do not generate test cases for it until it is corrected.

Build an index of acceptance criteria with reference IDs. Use the format `REQ-{NNN}-AC-{NN}` where `{NNN}` is the requirement number and `{NN}` is the criterion number within that requirement. For example, the second acceptance criterion under requirement 3 would be `REQ-003-AC-02`.

---

## Step 2: Generate Test Cases

For each acceptance criterion, generate test cases across four categories. Not every criterion requires all four categories — use your judgement, but every criterion MUST have at least one happy-path test.

### Category 1: Happy Path

The primary success scenario that matches the acceptance criterion exactly. The Given/When/Then of the test case should mirror the acceptance criterion closely, with concrete values replacing any abstract placeholders.

- One happy-path test per acceptance criterion (minimum)
- Use realistic, representative data values
- The "then" clause should assert the exact expected outcome

### Category 2: Edge Cases

Boundary conditions and atypical-but-valid scenarios. Consider:

- **Boundary values**: Minimum and maximum allowed inputs, just-inside and just-outside boundaries
- **Empty or null inputs**: Empty strings, null values, zero quantities
- **Maximum capacity**: Largest allowed data sets, longest strings, most concurrent items
- **Concurrent actions**: Multiple users or processes acting simultaneously
- **Timing**: Actions at exactly the same moment, actions at boundary of a time window
- **Format variations**: Different date formats, character encodings, locale-specific inputs

### Category 3: Error Cases

Invalid inputs and failure scenarios. Consider:

- **Invalid inputs**: Wrong data types, malformed data, out-of-range values
- **Authentication and authorization**: Expired tokens, missing permissions, role violations
- **Network failures**: Timeouts, connection drops, partial responses
- **Dependency failures**: External service unavailable, database unreachable
- **Resource exhaustion**: Disk full, rate limits hit, memory constraints
- **Conflict states**: Editing a deleted record, acting on stale data, duplicate submissions

### Category 4: Regression Cases

Tests that ensure existing functionality is not broken by the new feature. Consider:

- **Adjacent features**: Does the new behavior break related workflows?
- **Backward compatibility**: Do existing integrations, APIs, or saved data still work?
- **Default behavior**: Are unchanged paths still functioning correctly?

Only generate regression cases where there is a plausible risk of breakage based on the PRD's scope and dependencies.

---

## Step 3: Output Format

Each test case MUST be a JSON object conforming to this schema:

```json
{
  "id": "tc-{date}-{NNN}",
  "title": "{Feature} — {Scenario}",
  "prd_id": "{{prd_id}}",
  "acceptance_criterion": "REQ-{NNN}-AC-{NN}",
  "given": "precondition state with concrete values",
  "when": "specific action performed",
  "then": "expected outcome with verifiable assertions",
  "status": "pending",
  "result_notes": null,
  "executed_at": null,
  "created_at": "{ISO 8601 datetime}"
}
```

**Naming convention for titles**: Use the format `"{Feature} — {Scenario}"` where Feature is a short description of the capability being tested and Scenario describes the specific condition. Examples:

- `"Invoice Creation — Happy Path with Valid Line Items"`
- `"Invoice Creation — Edge Case with Zero Quantity"`
- `"Invoice Creation — Error on Missing Required Fields"`
- `"Invoice Creation — Regression: Existing Templates Still Load"`

**ID assignment**: IDs are sequential starting from `{{counter_start}}`. Each test case gets the next available ID in the format `tc-{YYYY-MM-DD}-{NNN}`.

Save each test case as an individual JSON file in `data/uat/test-cases/` with the filename matching the ID (e.g., `tc-2026-03-12-001.json`).

---

## Step 4: Group by Acceptance Criterion

After generating all test cases, organize them into groups by acceptance criterion. Present a summary showing:

```markdown
## Test Case Grouping

### REQ-001-AC-01: [Given/When/Then summary]
- tc-{date}-{NNN}: {title} (happy path)
- tc-{date}-{NNN}: {title} (edge case)
- tc-{date}-{NNN}: {title} (error case)

### REQ-001-AC-02: [Given/When/Then summary]
- tc-{date}-{NNN}: {title} (happy path)
...
```

---

## Step 5: Test Coverage Summary

Produce a coverage summary table at the end of the output:

| Acceptance Criterion | Happy Path | Edge Cases | Error Cases | Regression | Total |
|---------------------|-----------|-----------|------------|-----------|-------|
| REQ-001-AC-01       | 1         | 2         | 3          | 1         | 7     |
| REQ-001-AC-02       | 1         | 1         | 2          | 0         | 4     |
| ...                 | ...       | ...       | ...        | ...       | ...   |
| **Totals**          | **N**     | **N**     | **N**      | **N**     | **N** |

Also include:

- **Coverage assessment**: Are all must-have requirements covered? Are any acceptance criteria missing test cases?
- **Risk areas**: Which acceptance criteria have the fewest tests relative to their complexity? Where would additional tests add the most value?
- **Hypothesis validation map**: For each acceptance criterion, state the hypothesis it validates from the PRD and which test categories (happy/edge/error) are most critical for confirming or disproving that hypothesis.

---

## Test-and-Learn Integration

Each test case is an experiment in the test-and-learn model. When generating test cases, consider:

1. **What hypothesis does this test validate?** — Connect back to the PRD's hypothesis and specific requirements.
2. **What will we learn from a pass?** — Confirmation that the system behaves as specified under these conditions.
3. **What will we learn from a fail?** — Which assumption was wrong? Is the failure in the implementation, the requirement, or the test design?
4. **What is the smallest test that validates the most?** — Prioritize tests that cover the most critical unknowns first. The happy path tests should run first because they validate the core hypothesis; edge and error cases probe the boundaries.

---

## Quality Checklist (self-verify before output)

Before producing the final test cases, verify:
- [ ] Every acceptance criterion in the PRD has at least one happy-path test case
- [ ] All test cases use Given/When/Then format with concrete, verifiable values
- [ ] Test case titles follow the "{Feature} — {Scenario}" naming convention
- [ ] Each test case references a valid acceptance criterion using the REQ-NNN-AC-NN format
- [ ] IDs are sequential and correctly formatted as `tc-{YYYY-MM-DD}-{NNN}`
- [ ] `prd_id` is set correctly on every test case
- [ ] Edge cases cover boundary values, empty inputs, and concurrency where relevant
- [ ] Error cases cover invalid inputs, permission failures, and network/dependency failures
- [ ] Regression cases are included where adjacent functionality may be affected
- [ ] Coverage summary accounts for every acceptance criterion
- [ ] All tags exist in `data/meta/tags.json`
- [ ] `data/meta/counters.json` is updated with the new counter value after all test cases are created
