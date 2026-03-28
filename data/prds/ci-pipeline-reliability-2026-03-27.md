---
id: prd-2026-03-27-001
title: "CI Pipeline Reliability: Fast Builds, Flaky Test Quarantine, and Build Cache That Works"
status: draft
priority: high
linked_insights:
  - insight-2026-03-27-001
  - insight-2026-03-27-004
okr_ids:
  - okr-2026-Q2-001
roadmap_ids:
  - roadmap-2026-Q2-001
tags:
  - ci-cd
  - build-systems
  - testing-infrastructure
  - reliability
  - developer-friction
  - toil-reduction
  - outer-loop-speed
  - pain-point
  - time-saving
  - automation
  - performance
created_at: 2026-03-27T11:00:00Z
updated_at: 2026-03-27T12:00:00Z
---

# CI Pipeline Reliability: Fast Builds, Flaky Test Quarantine, and Build Cache That Works

## 1. Problem Statement

Internal engineers across the organization are losing significant productivity to a broken CI/CD pipeline. The evidence from discovery research paints a consistent picture of systemic dysfunction:

**Build times are unacceptably long.** Every backend code push triggers a 45-minute CI build, even for one-line changes. A senior backend engineer on Payments (Raj Mehta) tracked 11 hours in a single sprint spent waiting for CI — more than a full workday per week consumed by waiting (ref: insight-2026-03-27-001). Extrapolated across 200 engineers, this represents approximately 100 engineering hours per day of lost productivity.

**Flaky tests block unrelated PRs with no quarantine mechanism.** Approximately 50% of CI failures are caused by non-deterministic test failures — integration tests that share staging databases, contain hardcoded timing assumptions, or depend on mutable external state. Engineers cannot determine whether a flaky test guards critical functionality for another team, so the default behavior is to re-run the entire pipeline up to three times before investigating. Some engineers have automated this retry loop with scripts, effectively codifying a broken process as standard practice. As Raj put it: *"We've normalized a broken feedback loop. That should terrify someone."* (ref: insight-2026-03-27-001).

**The remote build cache is broken and unowned.** Bazel remote caching was deployed to accelerate builds but misses constantly. Half the engineering team has abandoned it entirely and runs full local builds. A dedicated Slack channel (#build-cache-woes) exists purely for venting about cache failures. No one owns the cache infrastructure, and no one has the authority or accountability to fix it (ref: insight-2026-03-27-001, insight-2026-03-27-004).

**Ownership vacuums perpetuate the problem.** The batch insight (insight-2026-03-27-004) identifies ownership vacuum as a convergent pattern across all three discovery interviews. Nobody owns flaky tests, nobody owns the build cache, and the workarounds that mask these failures have been normalized rather than escalated. The organization has tools (Bazel cache, CI pipelines) but not the governance structures to maintain them.

**The cost compounds across the entire development lifecycle.** The batch insight scores "golden path absence" as the highest-opportunity gap (Importance: 9, Satisfaction: 2, Opportunity Score: 16). CI friction is the most immediately quantifiable manifestation of this gap, affecting every engineer on every code push.

## 2. Hypothesis

> **I BELIEVE THAT** providing engineers with a CI pipeline that completes in under 15 minutes, automatically quarantines flaky tests from the critical path, and delivers reliable build cache hits
> **WILL** reduce time spent waiting for CI by at least 50% (from ~11 hours/sprint to under 5.5 hours/sprint per engineer) and decrease the CI re-run rate from ~50% to below 10%
> **FOR** all internal engineers who push code to the monorepo (approximately 200 engineers across backend, frontend, and infrastructure teams)
> **BECAUSE** discovery research demonstrates that the primary CI friction comes from the combination of long build times (45 minutes), non-deterministic test failures that block unrelated PRs (~50% of failures), and a broken remote build cache that forces full rebuilds — three problems that compound multiplicatively and that engineers have normalized rather than fixed (insight-2026-03-27-001: "11 hours just waiting for CI"; insight-2026-03-27-004: Opportunity Score 16/18 for golden path absence)

This hypothesis is falsifiable: if median build time does not drop below 15 minutes, or if the re-run rate does not drop below 10%, or if engineers do not report meaningfully increased trust in CI results after 4 weeks of pilot deployment, the intervention has failed and the root cause analysis needs revision.

## 3. User Personas

### 3.1 Raj — Backend Engineer (Payments Team)

- **Role archetype**: Mid-to-senior backend engineer working on a critical business domain
- **Goals**: Ship multiple code changes per day; maintain flow state; mentor new hires effectively
- **Pain points**: Spends 11 hours per sprint waiting for CI; cannot distinguish flaky failures from real failures; onboarded a new hire whose first PR landed on day 8 due to environment and CI friction (ref: insight-2026-03-27-001, "Last sprint I spent 11 hours just waiting for CI")
- **Adoption curve segment**: Early Adopter — Raj has already diagnosed the problem in detail, quantified the cost, and articulated the desired solution (fast CI, flaky quarantine). He will adopt immediately and advocate to peers
- **Adoption funnel stage**: Evaluation — Raj is past awareness and interest; he needs to see a working solution to move to trial

### 3.2 Priya — Frontend Engineer (Growth Team)

- **Role archetype**: Frontend engineer who runs the same CI pipeline for UI changes
- **Goals**: Iterate quickly on UI features; get fast feedback on component changes; avoid blocked PRs
- **Pain points**: CI builds include backend test suites irrelevant to frontend changes; flaky backend integration tests block frontend PRs; cannot selectively run only relevant tests (ref: insight-2026-03-27-004, golden path absence affects all roles)
- **Adoption curve segment**: Early Majority — will adopt once she sees backend teams benefiting, but needs clear evidence it works before changing her workflow
- **Adoption funnel stage**: Interest — aware of the problem, waiting for a credible solution

### 3.3 David — SRE / Platform Engineer

- **Role archetype**: SRE responsible for CI infrastructure and build systems
- **Goals**: Reduce toil; invest time in platform improvements rather than firefighting; provide reliable developer tooling
- **Pain points**: CI infrastructure issues consume his team's capacity; the broken build cache is technically his domain but has no staffed owner; gets pulled into debugging CI failures instead of building automation (ref: insight-2026-03-27-004, "We're stuck in a toil trap")
- **Adoption curve segment**: Innovator — David will be directly involved in building and operating the solution; he has been advocating for this investment for multiple quarters
- **Adoption funnel stage**: Awareness — understands the need deeply but has been unable to secure resources to act

### 3.4 Alex — New Hire (Any Team)

- **Role archetype**: Engineer in their first 30 days at the company
- **Goals**: Ship first PR within the first week; build confidence in the development workflow; feel productive quickly
- **Pain points**: First PR does not land until day 8 due to environment setup and CI friction; CI failures are confusing and demoralizing when you cannot tell if the failure is your fault (ref: insight-2026-03-27-001, "That's not an onboarding experience, that's a hazing ritual")
- **Adoption curve segment**: Early Majority — new hires will use whatever workflow is in place; they have no attachment to the old system
- **Adoption funnel stage**: Trial — will encounter the improved CI immediately upon joining; no adoption barrier if it is the default

## 4. User Stories

1. **As a backend engineer**, I want CI to complete in under 15 minutes for my code changes so that I can iterate multiple times per day without losing flow state. *(ref: insight-2026-03-27-001, theme: "CI pipeline bottleneck"; Raj: "45 minutes for a one-line change")*

2. **As an engineer pushing a PR**, I want flaky tests to be automatically identified and quarantined from the critical path so that non-deterministic failures do not block my merge. *(ref: insight-2026-03-27-001, theme: "Flaky test normalization"; Raj: "I can't just delete it — I don't know if it's testing something critical for another team")*

3. **As an engineer reviewing a CI failure**, I want to immediately see whether a failure is caused by my change or by a known flaky test so that I can decide whether to investigate or proceed. *(ref: insight-2026-03-27-001, JTBD: "Know immediately if a CI failure is my fault or a flaky test")*

4. **As a backend engineer**, I want the remote build cache to reliably provide cached artifacts so that I do not waste time rebuilding unchanged dependencies. *(ref: insight-2026-03-27-001, theme: "Broken build cache infrastructure"; Raj: "The cache was supposed to save us time")*

5. **As a frontend engineer**, I want CI to run only the tests relevant to my changes so that I am not blocked by unrelated backend test failures. *(ref: insight-2026-03-27-004, theme: "golden path absence across the development lifecycle")*

6. **As an SRE**, I want flaky test data to be tracked and reported automatically so that I can prioritize remediation by impact rather than by who complains loudest. *(ref: insight-2026-03-27-004, theme: "ownership vacuum for shared infrastructure")*

7. **As a new hire**, I want my first CI run to succeed or fail deterministically so that I can trust the feedback and learn from real failures, not random noise. *(ref: insight-2026-03-27-001, pain point: "Onboarding time sink"; insight-2026-03-27-004, theme: "onboarding friction as a systemic multiplier")*

8. **As an engineering manager**, I want visibility into CI health metrics (build time, flaky rate, cache hit rate) so that I can make data-driven decisions about infrastructure investment. *(ref: insight-2026-03-27-004, theme: "workaround culture masking platform underinvestment")*

## 5. Functional Requirements

### Must-Have

**FR-1: Flaky Test Detection and Quarantine System**
- Automatically identify tests that produce non-deterministic results by tracking pass/fail history across the last 100 runs per test
- Tests that fail non-deterministically above a configurable threshold (default: 10% flake rate over 100 runs) are flagged as flaky
- Flaky tests are moved to a quarantine lane: they still run but their results do not block PR merges
- Quarantine decisions are logged and reversible
- *Priority*: must-have
- *Traces to*: insight-2026-03-27-001 (flaky test normalization, ~50% false failure rate); User Stories 2, 3, 7
- *Acceptance Criteria*: AC-1, AC-2, AC-3

**FR-2: CI Failure Classification**
- Every CI failure is categorized as: (a) change-related failure, (b) known flaky test, or (c) infrastructure failure
- The classification is displayed prominently in the CI results UI and PR status check
- Engineers can see at a glance whether their PR is blocked by a real failure or a quarantined flaky test
- *Priority*: must-have
- *Traces to*: insight-2026-03-27-001 (JTBD: "Know immediately if a CI failure is my fault or a flaky test"); User Stories 3, 7
- *Acceptance Criteria*: AC-4, AC-5

**FR-3: Build Cache Reliability Improvements**
- Audit and fix the Bazel remote cache configuration to achieve a cache hit rate of at least 80% for unchanged build targets
- Implement cache health monitoring with alerts when hit rate drops below threshold
- Designate an explicit owner (team or role) for cache infrastructure with on-call rotation
- *Priority*: must-have
- *Traces to*: insight-2026-03-27-001 (broken build cache, #build-cache-woes channel); insight-2026-03-27-004 (ownership vacuum); User Story 4
- *Acceptance Criteria*: AC-6, AC-7

**FR-4: Build Pipeline Optimization**
- Implement intelligent test selection: run only tests affected by the changed code paths (using dependency graph analysis or file-change heuristics)
- Parallelize independent test suites to reduce wall-clock time
- Target: median CI build time under 15 minutes for typical changes (currently 45 minutes)
- *Priority*: must-have
- *Traces to*: insight-2026-03-27-001 (45-minute builds); insight-2026-03-27-004 (golden path absence, Opportunity Score 16); User Stories 1, 5
- *Acceptance Criteria*: AC-8, AC-9

### Should-Have

**FR-5: Flaky Test Dashboard and Reporting**
- Provide a dashboard showing: top flaky tests ranked by flake rate and blast radius (number of PRs affected), flaky test trend over time, ownership mapping (which team's tests are flakiest)
- Send weekly automated reports to engineering leads with flaky test statistics for their team
- *Priority*: should-have
- *Traces to*: insight-2026-03-27-004 (ownership vacuum, workaround culture); User Stories 6, 8
- *Acceptance Criteria*: AC-10

**FR-6: Test Ownership Registry**
- Every test file or test suite is mapped to an owning team
- When a flaky test is quarantined, the owning team is automatically notified
- Unowned tests are flagged in the dashboard; tests without an owner for more than 30 days are escalated
- *Priority*: should-have
- *Traces to*: insight-2026-03-27-001 ("nobody owns the flaky tests"); insight-2026-03-27-004 (ownership vacuum); User Story 6

**FR-7: CI Health Metrics API**
- Expose CI health metrics (median build time, p95 build time, flaky rate, cache hit rate, re-run rate) via an internal API and Grafana dashboard
- Historical data retained for at least 90 days for trend analysis
- *Priority*: should-have
- *Traces to*: insight-2026-03-27-004 (workaround culture masking platform underinvestment); User Story 8

### Nice-to-Have

**FR-8: Automatic Flaky Test Remediation Suggestions**
- For quarantined tests, automatically analyze common flake patterns (shared state, timing assumptions, network dependencies) and suggest fixes
- *Priority*: nice-to-have
- *Traces to*: insight-2026-03-27-001 (flaky test triage is impossible)

**FR-9: PR-Level Build Time Estimates**
- Before an engineer pushes, show an estimated CI completion time based on the files changed and historical build data
- *Priority*: nice-to-have
- *Traces to*: insight-2026-03-27-001 (engineers context-switch while waiting); User Story 1

## 6. Non-Functional Requirements

### Performance
- **NFR-1**: Median CI build time must be under 15 minutes for changes touching fewer than 50 files (current baseline: 45 minutes)
- **NFR-2**: P95 CI build time must be under 25 minutes (current baseline: estimated 60+ minutes with retries)
- **NFR-3**: Flaky test detection system must classify a test's flake status within 5 seconds of build completion (no perceptible delay to the engineer)

### Scalability
- **NFR-4**: The system must support the current 200-engineer organization and scale to 500 engineers without architectural changes
- **NFR-5**: Flaky test tracking must handle at least 50,000 test executions per day without degradation

### Reliability and Availability
- **NFR-6**: The flaky test quarantine system must have 99.9% uptime during business hours (failures would revert to blocking all tests, worsening the current experience)
- **NFR-7**: Build cache must maintain 99.5% availability; cache unavailability must gracefully degrade to full builds, not pipeline failures
- **NFR-8**: Remote build cache hit rate must be at least 80% for unchanged build targets

### Security and Compliance
- **NFR-9**: Test result data and flaky test classifications must be accessible only to authenticated internal users
- **NFR-10**: Build cache artifacts must not leak across repository boundaries or expose secrets from other build contexts

### Data Requirements
- **NFR-11**: Test execution history (pass/fail/flake status) must be retained for at least 90 days
- **NFR-12**: Build time metrics must be retained for at least 180 days for trend analysis

### Observability
- **NFR-13**: The CI pipeline itself must have monitoring and alerting: build queue depth, build duration trends, cache hit rate, and quarantine system health

## 7. Acceptance Criteria

### FR-1: Flaky Test Detection and Quarantine System

**AC-1: Flaky test identification**
```
Given a test that has failed non-deterministically in at least 10 of its last 100 runs (10% flake rate)
When the flaky detection system runs its scheduled analysis
Then the test is flagged as "flaky" in the test registry with its calculated flake rate, last flake date, and affected PR count
```

**AC-2: Quarantine enforcement**
```
Given a test that is flagged as "flaky" in the test registry
When that test fails during a CI run for a PR
Then the CI run is marked as "passed with quarantined flaky failures" (not "failed"), the PR is not blocked from merging, and the flaky test failure is logged separately in the quarantine report
```

**AC-3: Quarantine reversal**
```
Given a previously flaky test that has passed deterministically in its last 50 consecutive runs
When the flaky detection system runs its scheduled analysis
Then the test is removed from quarantine, restored to the critical path, and the owning team is notified of the status change
```

### FR-2: CI Failure Classification

**AC-4: Failure categorization display**
```
Given an engineer viewing a failed CI run on their PR
When the CI results page loads
Then each failed test is labeled as one of: "change-related failure" (red), "known flaky test" (yellow), or "infrastructure failure" (gray), and the overall PR status reflects only change-related failures
```

**AC-5: PR status accuracy**
```
Given a PR where all test failures are classified as "known flaky test" or "infrastructure failure"
When the CI status check reports to the source control system
Then the PR status check is reported as "passed" (green) with an informational note listing the quarantined failures, and the PR is eligible for merge
```

### FR-3: Build Cache Reliability

**AC-6: Cache hit rate threshold**
```
Given an engineer running a CI build that includes build targets unchanged since the last successful build
When the build system requests cached artifacts from the remote Bazel cache
Then at least 80% of requests for unchanged targets return a cache hit, and the cache response time is under 500ms per artifact
```

**AC-7: Cache health alerting**
```
Given the remote build cache hit rate drops below 70% over a rolling 1-hour window
When the monitoring system evaluates cache health
Then an alert is sent to the designated cache infrastructure owner within 5 minutes, including the current hit rate, miss rate breakdown by cause, and a link to the cache health dashboard
```

### FR-4: Build Pipeline Optimization

**AC-8: Selective test execution**
```
Given an engineer pushes a change that modifies 3 files in the payments service
When CI determines which tests to run
Then only tests in the dependency graph of the modified files are executed (not the entire test suite), and the set of selected tests is displayed in the CI run summary for transparency
```

**AC-9: Build time target**
```
Given a typical code change (fewer than 50 files modified) submitted to CI
When the build and test pipeline completes
Then the total wall-clock time from submission to final result is under 15 minutes at the median (measured over a rolling 7-day window)
```

### FR-5: Flaky Test Dashboard

**AC-10: Dashboard content and accuracy**
```
Given an engineer or engineering manager navigates to the flaky test dashboard
When the dashboard loads
Then it displays: (a) the top 20 flakiest tests ranked by flake rate, (b) the number of PRs each flaky test has affected in the last 7 days, (c) the owning team for each test, (d) a trend chart of org-wide flake rate over the last 90 days, and all data is no more than 1 hour stale
```

## 8. Success Metrics

| HEART Dimension | Goal | Signal | Metric |
|-----------------|------|--------|--------|
| **Happiness** | Engineers trust CI results and feel their time is respected | Positive sentiment in developer surveys about CI reliability; decrease in #build-cache-woes Slack activity | Developer satisfaction score for CI (quarterly survey) improves from baseline to 4.0+/5.0 within 2 quarters; #build-cache-woes message volume decreases by 70%+ |
| **Engagement** | Engineers interact with CI feedback rather than ignoring or auto-retrying it | Engineers review CI failure classifications; decrease in blind re-runs | CI re-run rate drops from ~50% to below 10%; percentage of engineers who review the failure classification before re-running increases to 80%+ |
| **Adoption** | All engineering teams use the improved CI pipeline and flaky quarantine system | Teams on the new pipeline; engineers opting in to selective test execution | 100% of active repositories migrated to the new pipeline within 8 weeks of launch; 90%+ of engineers have at least one PR processed through the new pipeline within 4 weeks |
| **Retention** | Engineers continue using the new CI workflow without reverting to old workarounds | Auto-retry scripts are retired; engineers do not manually re-run quarantined flaky tests | Auto-retry script usage drops to near zero within 4 weeks; manual re-run rate for quarantined tests stays below 5% |
| **Task Success** | Engineers get fast, deterministic CI feedback that enables rapid iteration | CI completes quickly; first-pass success rate improves | Median build time under 15 minutes (from 45); first-pass CI success rate (excluding flaky tests) improves to 85%+ (from ~50%); build cache hit rate at 80%+ |

**Hero metric**: Median CI build time. Target: under 15 minutes within 4 weeks of full rollout. This is the single most visible indicator of improvement and directly maps to the 100 engineering hours/day waste identified in discovery.

**Secondary hero metric**: CI re-run rate. Target: below 10% within 4 weeks. This validates that the flaky test quarantine is working and engineers trust the results.

## 9. MVP Scope (Goldilocks Principle)

### Too Basic — Would Fail to Validate the Hypothesis
- Only fixing the build cache without addressing flaky tests or build time. Engineers would still experience 50% flaky failure rates and 45-minute builds, so even perfect caching would not meaningfully reduce total wait time.
- A manual flaky test list maintained by engineers. This recreates the current ownership problem — nobody will maintain the list, and it will become stale within weeks.
- Build time reduction without failure classification. Engineers would still not know if a failure is real or flaky, so the re-run problem persists.

### Too Complex — Would Sacrifice Agility
- Full dependency-graph-based test selection with per-file granularity on day one. This requires deep build system integration that could take months to get right.
- Automatic flaky test remediation (FR-8). Interesting but not needed to validate whether quarantine alone solves the re-run and trust problems.
- Integration with Jira for automatic flaky test bug creation. Useful but adds scope and dependencies without validating the core hypothesis.
- PR-level build time estimates (FR-9). Nice but not essential for validating whether faster, more reliable CI changes behavior.

### Just Right — The MVP
The MVP includes the following, and nothing more:

1. **Flaky test detection and quarantine (FR-1)** — Essential. Without quarantine, flaky tests continue to block PRs regardless of build speed. This directly validates whether removing false failures changes engineer behavior and trust.

2. **CI failure classification (FR-2)** — Essential. Engineers need to see why a build passed or failed in the new system. Without classification, the quarantine is invisible and trust cannot be built.

3. **Build cache reliability fix (FR-3)** — Essential. Cache fixes are a prerequisite for meaningful build time reduction. Without a working cache, test selection optimizations have limited impact.

4. **Build pipeline optimization with basic selective test execution (FR-4)** — Essential. Build time is the hero metric. Basic selective execution (at the service/module level, not per-file) is achievable in the MVP timeframe and delivers the biggest time savings.

**Deferred to post-MVP iteration 1**: FR-5 (flaky test dashboard), FR-6 (test ownership registry), FR-7 (CI health metrics API). These are valuable for sustained improvement but not needed to validate the core hypothesis.

**Deferred to post-MVP iteration 2**: FR-8 (auto-remediation suggestions), FR-9 (build time estimates). These optimize the workflow but require the MVP foundation to be in place first.

## 10. Adoption Strategy

### Target Adoption Segment: Early Adopters (then rapid expansion to Early Majority)

The initial release targets **Early Adopters** — engineers like Raj who have already diagnosed the problem, quantified its cost, and articulated the desired solution. These engineers will adopt immediately because they are actively suffering from the pain and have been advocating for a fix.

However, because this is infrastructure, the path from Early Adopter to Early Majority is unusually short. CI is not opt-in — once the pipeline is updated for a repository, every engineer pushing to that repository uses the new system. The adoption challenge is not convincing individuals to change behavior; it is ensuring the rollout does not introduce regressions.

### Onboarding Strategy (Time to First Value)

- **Time to First Value**: The first time an engineer pushes a PR after migration, they will see (a) faster build completion and (b) clear failure classification. No action required from the engineer — the improvement is automatic.
- **Announcement**: Internal engineering blog post and Slack announcement in #engineering explaining the changes, what to expect, and how to read the new CI status labels.
- **Migration path**: Repository-by-repository migration, starting with the 3 highest-traffic repositories. Each migration is a configuration change — no engineer action required.
- **Feedback channel**: Dedicated #ci-improvements Slack channel for questions, issues, and feedback during rollout. Monitored by the DevEx team.

### Continuous Onboarding

- Weekly "CI Health Digest" email (post-MVP, via FR-5 dashboard) showing build time trends, flaky test improvements, and cache hit rates. This keeps the improvement visible and reinforces the value.
- Brown-bag session in week 2 of rollout: "How the New CI Works" — explain flaky quarantine, failure classification, and how to interpret the new CI status labels. Record for async viewing.

### Messaging Alignment

- **For Early Adopters (Raj archetype)**: "We heard you. CI builds are now under 15 minutes. Flaky tests no longer block your PRs. The build cache actually works." Lead with speed and reliability.
- **For Early Majority (Priya archetype)**: "Your PRs now merge faster. Here is what changed and what you need to know." Lead with outcomes, not implementation details.
- **For Engineering Managers**: "Your team is getting back X hours per sprint. Here are the metrics." Lead with quantified impact.

### Crossing the Chasm

The chasm risk is low for infrastructure changes because adoption is repository-level, not individual-level. The primary risk is not adoption resistance but regression anxiety — teams may push back on migration if they fear the new system will introduce new failure modes. Mitigation:
- Canary rollout: first 3 repositories for 2 weeks before expanding
- Rollback plan: one-command revert to the previous CI configuration per repository
- Transparent metrics: publish before/after build times and success rates for each migrated repository

## 11. Dependencies

| Dependency | Owner | Risk if Delayed or Unavailable |
|------------|-------|-------------------------------|
| **Bazel remote cache infrastructure access** | Platform/Infrastructure team | High — build cache fix (FR-3) requires configuration access and possibly hardware changes to the cache cluster. Delay here blocks the biggest build time improvements. |
| **CI pipeline configuration (e.g., Jenkins, GitHub Actions, or equivalent)** | DevEx / Platform team | High — all pipeline changes (selective testing, quarantine integration) require CI configuration access. This should be within the DevEx team's control. |
| **Test execution history data** | CI system (existing data pipeline) | Medium — flaky test detection (FR-1) requires access to historical test results. If this data is not already stored, building the data pipeline adds 2-3 weeks of scope. |
| **Source control integration (PR status API)** | Source control platform (GitHub/GitLab) | Low — failure classification display (FR-2) requires writing custom PR status checks. Standard API, low risk. |
| **Build dependency graph tooling** | Build systems team / Bazel configuration | Medium — selective test execution (FR-4) requires a dependency graph. If the existing Bazel build graph is not queryable at the right granularity, a heuristic approach (module-level selection) may be used as fallback. |
| **Engineering team cooperation for pilot** | Payments team (Raj's team), 2 additional teams | Low — discovery research indicates high willingness to participate. Raj has explicitly advocated for this. |

## 12. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Quarantined flaky tests mask real regressions** — A test that appears flaky is actually catching a real, intermittent production bug. Quarantining it removes a safety net. | Medium | High | Quarantined tests still run and results are logged. Implement a "quarantine review" process: quarantined tests with >50% failure rate are manually reviewed before remaining quarantined. Add production incident correlation — if a production bug maps to a quarantined test, auto-escalate. |
| **Build cache fix is more complex than expected** — The Bazel remote cache issues may stem from fundamental architecture problems (cache key instability, network throughput), not just configuration. | Medium | Medium | Time-box the cache fix to 2 weeks. If the existing cache cannot be fixed within that window, evaluate alternative caching strategies (local persistent cache, different remote cache backend). Do not let cache investigation block the flaky test quarantine work. |
| **Selective test execution misses necessary tests** — Dependency graph analysis may have blind spots, causing real failures to be missed in CI but caught later in production. | Low | High | Start with conservative module-level selection (run all tests in the modified module, not just directly affected tests). Maintain a weekly full-suite run as a safety net. Track any production incidents that could have been caught by the skipped tests. |
| **Engineers distrust the new system and continue re-running manually** — Cultural inertia from years of re-run behavior may persist even after the technical fix. | Medium | Low | Clear communication about how quarantine works. Visible failure classification in the CI UI. Track re-run rate as a metric and follow up with teams that continue manual re-runs to understand why. |
| **Organizational resistance to designating cache/test infrastructure owners** — Assigning ownership requires management buy-in and potentially staffing changes. | Medium | Medium | Present the ownership gap as a finding from discovery research, supported by quantified cost data (100 eng-hours/day). Frame ownership as a prerequisite, not an optional improvement. Escalate to VP Engineering if necessary. |
| **Pilot teams are not representative of the broader org** — Improvements that work for the pilot teams may not generalize to teams with different tech stacks or test patterns. | Low | Medium | Select pilot teams from different domains (backend, frontend, infrastructure) to maximize representativeness. Instrument metrics per-team to detect divergent outcomes early. |

## 13. Out of Scope

1. **Local development environment improvements** — While insight-2026-03-27-001 identifies local environment fragility (400-line docker-compose, multi-day setup) as a significant pain point, it is a separate initiative with different dependencies and solutions. Deferred to a dedicated PRD for local dev environment modernization.

2. **Test suite refactoring or reduction** — This PRD quarantines flaky tests but does not fix them. Flaky test remediation requires test-by-test investigation by owning teams and is better addressed through the test ownership registry (FR-6, post-MVP) and team-level accountability processes.

3. **CI/CD pipeline for deployment (CD)** — This PRD addresses the CI (continuous integration) portion only: build, test, and merge. Deployment pipeline improvements (CD) are a separate concern with different stakeholders and risk profiles.

4. **Frontend-specific build optimizations** — While frontend engineers are affected by CI friction, frontend build tooling (e.g., webpack/Vite optimization, component-level testing) has different characteristics than backend build optimization. Deferred to a frontend-specific initiative.

5. **CI cost optimization** — Faster builds and better caching may reduce CI compute costs, but cost reduction is a secondary benefit, not a goal of this PRD. Cost analysis will be performed post-launch as part of outcomes tracking.

6. **Integration with external tools (Jira, Slack bots)** — Automatic ticket creation for flaky tests or Slack notifications for CI status are valuable but not needed to validate the core hypothesis. Deferred to post-MVP.

7. **Service onboarding and golden path tooling** — The batch insight (insight-2026-03-27-004) identifies service onboarding as a high-opportunity gap (Opportunity Score 14). This is a separate, larger initiative. CI reliability is a prerequisite for — not a substitute for — a comprehensive golden path.
