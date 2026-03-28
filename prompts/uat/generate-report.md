# Prompt: Generate UAT Report

You are a senior QA lead generating a User Acceptance Testing (UAT) report from test execution results. You will be given a **PRD** and its associated **test cases** (with execution results). Your job is to produce a comprehensive report that summarizes test outcomes, assesses risk, and provides actionable recommendations on whether to ship.

---

## Inputs

- `{{prd}}` — full text of the PRD (including frontmatter, title, and acceptance criteria)
- `{{prd_id}}` — the PRD ID (e.g., `prd-2026-03-12-001`)
- `{{prd_title}}` — the PRD title
- `{{test_cases}}` — all test case JSON files from `data/uat/test-cases/` where `prd_id` matches
- `{{report_id}}` — the assigned report ID (e.g., `uat-report-2026-03-12-001`)
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this report

---

## Output Format

Generate a Markdown file with YAML frontmatter followed by the report body. Save to `data/uat/reports/` with the filename matching the ID (e.g., `uat-report-2026-03-12-001.md`). The frontmatter MUST conform to this schema:

```yaml
---
id: {{report_id}}
title: "UAT Report — {{prd_title}}"
prd_id: {{prd_id}}
summary:
  total: <total test case count>
  pass: <count with status "pass">
  fail: <count with status "fail">
  blocked: <count with status "blocked">
  pending: <count with status "pending">
  pass_rate: "<percentage as string, e.g. 85%>"
recommendation: ship | ship-with-issues | block
tags: {{tags}}
created_at: "<ISO 8601 datetime>"
---
```

The `recommendation` field is determined by the rules in the Risk Assessment section below.

---

## Report Body Structure

Generate each of the following sections in order. Every section is mandatory.

### 1. Executive Summary

A 3-5 sentence overview for stakeholders who will not read the full report. Include:

- What was tested (PRD title and scope)
- Overall pass rate and test case count
- The shipping recommendation in plain language
- The single most critical finding (positive or negative)

### 2. Test Results Summary

Present aggregate results in a summary table:

| Metric | Value |
|--------|-------|
| **Total Test Cases** | N |
| **Passed** | N (N%) |
| **Failed** | N (N%) |
| **Blocked** | N (N%) |
| **Pending** | N (N%) |
| **Overall Pass Rate** | N% |

Then break down pass rate by acceptance criterion:

| Acceptance Criterion | Total | Pass | Fail | Blocked | Pending | Pass Rate |
|---------------------|-------|------|------|---------|---------|-----------|
| REQ-001-AC-01       | N     | N    | N    | N       | N       | N%        |
| REQ-001-AC-02       | N     | N    | N    | N       | N       | N%        |
| ...                 | ...   | ...  | ...  | ...     | ...     | ...       |

And break down by test category:

| Category | Total | Pass | Fail | Blocked | Pending | Pass Rate |
|----------|-------|------|------|---------|---------|-----------|
| Happy Path  | N  | N    | N    | N       | N       | N%        |
| Edge Cases  | N  | N    | N    | N       | N       | N%        |
| Error Cases | N  | N    | N    | N       | N       | N%        |
| Regression  | N  | N    | N    | N       | N       | N%        |

### 3. Failed Tests — Detailed Analysis

For each test case with `status: "fail"`, provide a detailed analysis:

#### tc-{date}-{NNN}: {title}

- **Acceptance Criterion**: REQ-NNN-AC-NN
- **Category**: Happy Path / Edge Case / Error Case / Regression
- **Expected Behavior**: What the "then" clause specified should happen
- **Actual Behavior**: What actually happened (from `result_notes`)
- **Severity**: Critical / High / Medium / Low — assessed as follows:
  - **Critical**: Happy-path failure on a must-have requirement; core functionality is broken
  - **High**: Edge-case failure that affects common user workflows; error handling is missing for likely scenarios
  - **Medium**: Edge-case failure for uncommon scenarios; error handling is incomplete but has workarounds
  - **Low**: Cosmetic issue or regression in a low-traffic area; failure in an unlikely boundary scenario
- **Root Cause Hypothesis**: Based on the expected vs actual behavior, what likely went wrong?
- **Recommended Action**: Specific fix-and-retest, design review, or requirement clarification needed

Order failed tests by severity (Critical first, then High, Medium, Low).

### 4. Blocked Tests — Resolution Plan

For each test case with `status: "blocked"`, provide:

#### tc-{date}-{NNN}: {title}

- **Acceptance Criterion**: REQ-NNN-AC-NN
- **Blocking Reason**: What is preventing execution (from `result_notes`)
- **Impact**: What risk does this unexecuted test represent?
- **Resolution**: Specific steps to unblock — environment setup, dependency resolution, data preparation, or access provisioning
- **Owner**: Who should resolve the blocker (if determinable from context)
- **Target Resolution**: Urgency level — must resolve before ship / can resolve post-ship / informational only

### 5. Pending Tests

List any test cases still in `status: "pending"` that have not been executed. For each, note:

- Whether it must be executed before a shipping decision can be made
- If it tests a must-have requirement's happy path, it MUST be executed before shipping

### 6. Test Execution Timeline

Summarize when tests were executed:

| Date | Tests Executed | Pass | Fail | Blocked | Notes |
|------|---------------|------|------|---------|-------|
| YYYY-MM-DD | N | N | N | N | e.g., "Initial run" |
| YYYY-MM-DD | N | N | N | N | e.g., "Retest after fixes" |

Derive dates from the `executed_at` field on test cases. Group by date. If `executed_at` is null, the test has not been executed (pending).

### 7. Risk Assessment

Assess the risk of shipping based on test results. Apply these rules:

**Ship** (recommendation: `ship`):
- All happy-path tests pass
- Overall pass rate is 90% or above
- No Critical or High severity failures remain
- All must-have requirement acceptance criteria have at least one passing happy-path test

**Ship with Known Issues** (recommendation: `ship-with-issues`):
- All happy-path tests for must-have requirements pass
- Overall pass rate is 70% or above
- No Critical severity failures remain
- Any High severity failures have documented workarounds
- Remaining failures are in edge cases or error handling that can be patched post-launch

**Block** (recommendation: `block`):
- Any happy-path test for a must-have requirement fails
- Overall pass rate is below 70%
- Any Critical severity failure remains unresolved
- Blocked tests cover must-have requirements and cannot be unblocked before the ship date

Present the assessment as:

> **Recommendation: {SHIP / SHIP WITH KNOWN ISSUES / BLOCK}**
>
> {2-3 sentence justification referencing specific test results and severity counts}

Include a risk summary table:

| Risk Factor | Status | Details |
|------------|--------|---------|
| Happy-path coverage for must-haves | Pass / Fail | List any gaps |
| Critical severity failures | N remaining | List IDs |
| High severity failures | N remaining | List IDs |
| Blocked must-have tests | N blocked | List IDs |
| Pending must-have tests | N pending | List IDs |
| Overall pass rate | N% | Above/below threshold |

### 8. Recommendations

Provide prioritized, actionable recommendations organized into three tiers:

#### Tier 1: Fix Before Ship (Blockers)
Items that must be resolved before the product can ship. Each item should reference specific failed test case IDs.

#### Tier 2: Fix After Ship (Known Issues)
Items that can ship with documented workarounds but should be resolved in the next iteration. Include the workaround for each.

#### Tier 3: Improve in Future (Enhancements)
Non-critical improvements identified during testing — better error messages, edge case handling for unlikely scenarios, UX refinements.

For each recommendation:
- **Test Case(s)**: IDs of related test cases
- **Description**: What needs to change
- **Effort Estimate**: Small / Medium / Large
- **Impact**: What improves when this is fixed

### 9. Lessons Learned

Drawing from the test-and-learn model, capture what was learned during this UAT cycle:

- **What hypotheses were validated?** — Which acceptance criteria passed cleanly, confirming the PRD's assumptions?
- **What hypotheses were challenged?** — Which failures suggest the requirements or design need rethinking?
- **What surprised us?** — Unexpected failures or unexpected passes that reveal assumptions worth examining.
- **Process improvements**: Were test cases well-designed? Were there gaps in coverage? What should be done differently next cycle?

---

## Quality Checklist (self-verify before output)

Before producing the final report, verify:
- [ ] Frontmatter has all required fields and valid values
- [ ] `prd_id` matches the input PRD
- [ ] Summary counts (total, pass, fail, blocked, pending) are arithmetically correct
- [ ] Pass rate is calculated correctly: `pass / (total - pending) * 100` rounded to nearest integer
- [ ] Every failed test case appears in the Failed Tests section with severity and recommended action
- [ ] Every blocked test case appears in the Blocked Tests section with resolution plan
- [ ] Severity assessments follow the defined criteria (Critical/High/Medium/Low)
- [ ] Recommendation follows the defined rules (ship/ship-with-issues/block)
- [ ] Risk assessment table is complete with no empty cells
- [ ] Recommendations are organized into three tiers with specific test case references
- [ ] Test execution timeline reflects actual `executed_at` dates from test cases
- [ ] All tags exist in `data/meta/tags.json`
- [ ] `data/meta/counters.json` is updated with the new report counter value
