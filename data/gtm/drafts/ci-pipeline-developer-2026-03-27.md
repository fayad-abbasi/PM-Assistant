---
id: gtm-2026-03-27-001
title: "CI Pipeline Reliability — Developer Messaging"
prd_id: prd-2026-03-27-001
audience: developer
status: draft
tags:
  - ci-cd
  - build-systems
  - testing-infrastructure
  - reliability
  - developer-friction
  - toil-reduction
  - outer-loop-speed
  - performance
  - automation
created_at: 2026-03-27T14:00:00Z
---

# CI Pipeline Reliability: What's Changing and Why You'll Care

## 1. Problem

Every backend code push triggers a 45-minute CI build. Half of those builds fail on flaky tests that have nothing to do with your change. You re-run. You wait another 45 minutes. You re-run again. Some of you have automated this with retry scripts — which means we've literally automated a broken process instead of fixing it.

The numbers from our own engineering team (ref: insight-2026-03-27-001):

- **45 minutes** per CI run, even for a one-line change
- **~50% of CI failures** are flaky tests — shared staging DBs, hardcoded sleeps, mutable external state
- **11 hours per sprint** per engineer lost to CI waits (that's more than a full workday per week)
- **Bazel remote cache** misses constantly — half the team has abandoned it and runs full local builds
- **#build-cache-woes** exists as a Slack channel. That's the state of things.

Nobody owns the flaky tests. Nobody owns the build cache. The workarounds have become the workflow.

## 2. Solution

We're shipping four changes to the CI pipeline: automatic flaky test detection and quarantine, failure classification in CI results, a fixed Bazel remote cache with actual ownership, and selective test execution based on what you changed. The target is median builds under 15 minutes and a re-run rate below 10%.

## 3. How It Works

### Flaky Test Quarantine

The system tracks pass/fail history for every test over its last 100 runs. Any test with a flake rate above 10% gets flagged and moved to a quarantine lane. Quarantined tests still run, but they do not block your PR from merging.

```
# What you'll see in CI output:

✅ PASSED — 847 tests passed
⚠️  QUARANTINED — 3 tests failed (known flaky, non-blocking)
   - payments/integration/test_settlement_timing.py  [flake rate: 23%]
   - growth/e2e/test_onboarding_flow.py              [flake rate: 14%]
   - infra/test_cache_invalidation.py                 [flake rate: 31%]
❌ FAILED — 0 tests failed (change-related)

PR status: ✅ Ready to merge
```

Quarantine decisions are logged and reversible. A test that passes deterministically in 50 consecutive runs is automatically restored to the critical path.

### Failure Classification

Every CI failure is now categorized:

| Label | Color | Meaning | Blocks merge? |
|-------|-------|---------|---------------|
| **Change-related failure** | Red | Your code broke a test | Yes |
| **Known flaky test** | Yellow | Non-deterministic, quarantined | No |
| **Infrastructure failure** | Gray | CI infra issue (network, runner, etc.) | No |

The PR status check only reflects change-related failures. If all your failures are flaky or infrastructure, your PR is green.

### Build Cache Fix

The Bazel remote cache is being audited and fixed. Target: 80%+ cache hit rate for unchanged build targets, with response times under 500ms per artifact. A designated owner (on-call rotation) will maintain it going forward. Monitoring and alerts fire when hit rate drops below 70%.

### Selective Test Execution

Instead of running the entire test suite on every push, CI now analyzes the dependency graph of your changed files and runs only affected tests. If you change 3 files in the payments service, you run payments tests — not the entire monorepo suite.

```
# CI run summary shows what was selected:

Build scope: payments/api/settlement.py (+2 related files)
Tests selected: 142 of 4,831 total (via dependency graph analysis)
Tests skipped: 4,689 (not in dependency path of changed files)
Quarantined: 3 (non-blocking)

Total time: 8m 42s
```

## 4. Integration Guide

**What integrates with what:**
- CI pipeline (Jenkins/GitHub Actions) — configuration change, not a new tool
- Bazel remote cache — existing infrastructure, fixed configuration + new monitoring
- PR status checks — updated to reflect failure classification labels
- Source control (GitHub/GitLab) — standard PR status API, no changes to your git workflow

**What changes in your workflow:**
- Nothing on your end. You push code. CI runs. The results are now faster and more honest.
- CI status labels will look different — read the classification (red/yellow/gray) instead of just pass/fail.
- You can stop re-running on flaky failures. If it's yellow, it's quarantined and non-blocking.
- Retire your auto-retry scripts. They're no longer needed.

**Breaking changes:**
- None. This is a pipeline configuration change. Your code, tests, and push workflow are unchanged.
- Rollback: one-command revert per repository if anything goes wrong.

**Migration:**
- Repository-by-repository. Your repo gets migrated by the DevEx team — no action required from you.
- Starting with the 3 highest-traffic repositories, then expanding over 8 weeks.

## 5. Getting Started

1. **Do nothing.** When your repository is migrated, the new pipeline activates automatically on your next push.
2. **Push a PR** as you normally would.
3. **Read the CI output.** You'll see the new failure classification labels (red/yellow/gray) and the test selection summary.
4. **Merge faster.** If all failures are yellow (quarantined flaky) or gray (infrastructure), your PR is green.
5. **Report issues** in #ci-improvements on Slack. The DevEx team monitors it during rollout.

Time to first value: your literal next `git push` after migration.

## 6. Adoption Curve Considerations

### For Innovators (SREs, Platform Engineers)

You'll have direct access to the flaky test detection data and cache health metrics. The CI health API (post-MVP, FR-7) will expose build time, flake rate, and cache hit rate data for custom dashboards and automation. If you want to build tooling on top of this — alerting, team-level reports, remediation bots — the data will be there.

The quarantine system is configurable: flake rate thresholds, quarantine window sizes, and reversal criteria can all be tuned per-repository.

### For Early Adopters (Engineers Who've Been Complaining)

You know who you are. You tracked 11 hours of CI waste last sprint. You have opinions about the build cache. Here's your proof it works:

- **Target**: median build time under 15 minutes (from 45)
- **Target**: re-run rate below 10% (from ~50%)
- **Target**: cache hit rate above 80% (from "misses constantly")
- **Pilot**: 3 highest-traffic repos for 2 weeks, with published before/after metrics
- **Rollback**: one-command revert if the new pipeline introduces regressions

You'll see the pilot results before your repo is migrated. If the numbers don't hold, we don't expand.

## 7. FAQ

**Q: What happens if a quarantined flaky test is actually catching a real bug?**
A: Quarantined tests still run and results are logged. Tests with a failure rate above 50% get manual review before remaining quarantined. If a production incident correlates with a quarantined test, the system auto-escalates. The quarantine removes blocking, not execution.

**Q: How does selective test execution know which tests to run?**
A: It uses dependency graph analysis from the Bazel build graph, at the module/service level for MVP. If your change touches `payments/api/settlement.py`, it runs all tests that transitively depend on that file. The selected test set is shown in the CI run summary so you can verify. A weekly full-suite run acts as a safety net.

**Q: Will this work for frontend changes too?**
A: Yes. Selective test execution applies to all code in the monorepo. Frontend changes will no longer trigger unrelated backend test suites. Frontend-specific build optimizations (webpack/Vite) are a separate initiative.

**Q: What are the system requirements?**
A: None from your side. This is a CI pipeline configuration change. No new CLIs, no new dependencies, no environment variable changes. Your local development workflow is unchanged.

**Q: What if the new pipeline introduces new failure modes?**
A: Canary rollout: 3 repos for 2 weeks before expanding. One-command rollback per repository. Published before/after metrics for each migration. If median build time does not drop below 15 minutes or re-run rate does not drop below 10% during the pilot, expansion stops and root cause analysis happens.

**Q: When does my repo get migrated?**
A: The 3 highest-traffic repositories go first. Remaining repositories migrate over 8 weeks. Check #ci-improvements for the migration schedule. No engineer action is required — migration is a configuration change applied by the DevEx team.
