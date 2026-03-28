---
id: journey-2026-03-27-001
title: "Raj Mehta — Backend Engineer CI Pipeline Journey"
persona: "Raj Mehta — Senior Backend Engineer"
linked_interviews:
  - interview-2026-03-05-001
linked_prds:
  - prd-2026-03-27-001
tags:
  - ci-cd
  - developer-friction
  - outer-loop-speed
  - backend-engineer
  - pain-point
  - toil-reduction
  - testing-infrastructure
  - build-systems
  - reliability
  - time-saving
created_at: 2026-03-27T14:00:00Z
---

# Raj Mehta — Backend Engineer CI Pipeline Journey

## 1. Persona Context

- **Name and Role**: Raj Mehta, Senior Backend Engineer on the Payments Team. Mid-to-senior individual contributor working on a critical business domain, responsible for shipping backend service changes and mentoring new hires.
- **Job to Be Done**: "When I push a backend code change, I want to get reliable CI feedback in under 15 minutes, so I can iterate quickly and ship multiple changes per day without losing flow state."
- **Adoption Curve Segment**: **Early Adopter** -- Raj has already diagnosed the CI problem in detail, quantified its cost (11 hours/sprint, 100 eng-hours/day org-wide), and articulated the desired solution (sub-15-minute builds, flaky test quarantine). He has deep domain knowledge of the root causes (shared staging DBs, hardcoded sleeps, broken Bazel cache) and will adopt any credible improvement immediately. Evidence: he independently calculated the ROI, frames the problem with urgency ("you need a fire truck"), and has tried workarounds (auto-retry scripts) -- all hallmarks of an Early Adopter who has exhausted self-service options (ref: interview-2026-03-05-001).
- **Current State Summary**: Raj pushes code to a monorepo CI pipeline that takes 45 minutes per run. Approximately half of all CI runs fail on flaky tests unrelated to his change, triggering a team-normalized retry loop of up to three re-runs per PR. The remote Bazel build cache misses constantly, forcing full rebuilds. His weekly time budget loses 11+ hours to CI waiting alone -- more than a full workday consumed by a broken feedback loop that the team has accepted as normal.

> **I am** a senior backend engineer on the Payments team who ships multiple code changes per week to a critical business service
> **I'm trying to** get fast, reliable feedback on my code changes so I can iterate confidently and maintain flow state
> **but** the CI pipeline takes 45 minutes per run and fails on flaky tests half the time, forcing me to re-run and wait again
> **because** integration tests share mutable staging databases, contain hardcoded timing assumptions, the remote build cache is broken and unowned, and nobody has the authority or accountability to fix these systemic issues
> **which makes me feel** frustrated that my time is not valued, exasperated that the team has normalized dysfunction, and urgently concerned that the organization is hemorrhaging 100 engineering hours per day on a solvable problem

## 2. Journey Stages Table

| Stage | User Actions | Touchpoints | Think & Feel | Pain Points | Opportunities |
|-------|-------------|-------------|-------------|-------------|---------------|
| **Awareness** | Raj finishes a code change locally and prepares to push to the remote branch, knowing CI will be triggered. He mentally prepares for the wait. He checks Slack to see if anyone has reported CI issues today. | Local IDE, Git CLI, Slack (#build-cache-woes, team channels), PR creation UI | **Think**: "Here we go again. Hopefully it passes this time." **Feel**: Resignation mixed with low-grade dread. He has internalized that CI is a lottery, not a deterministic process. **Hear**: Teammates in Slack venting about flaky tests; the #build-cache-woes channel is a constant background signal that the system is broken. **See**: Other engineers on the team also pushing and waiting, some with auto-retry scripts running. | No pre-push signal about CI health -- Raj cannot know in advance if the pipeline is currently healthy or degraded. He enters the process blind every time. | Provide a CI health status indicator (green/yellow/red) visible before push, so engineers can time their pushes or set expectations. Surface recent flaky test activity to reduce surprise. |
| **Interest** | Raj pushes his code. CI is triggered automatically. He opens the CI dashboard to watch the build start. He checks which tests will run and estimates the wait time based on experience. | Git push, CI dashboard (build queue view), PR status checks, Slack notifications | **Think**: "45 minutes for a one-line fix. This is absurd." **Feel**: Impatience and a sense of wasted potential. He knows the math: 200 engineers times 30 minutes wasted per day equals 100 engineering hours daily. **Say vs. Do**: He says the system is broken, but he continues to use it without escalating -- the workaround (retry) is easier than fighting for a fix. | 45-minute build times for even trivial changes. No intelligent test selection -- the entire test suite runs regardless of what changed. The build cache misses constantly, negating its purpose: "The cache was supposed to save us time. Instead it's become another thing that's broken that nobody fixes" (interview-2026-03-05-001). | Implement selective test execution based on dependency graph analysis so only affected tests run. Fix remote Bazel cache to achieve 80%+ hit rate for unchanged targets. Target median build time under 15 minutes. |
| **Evaluation** | Raj context-switches to another task while waiting. He checks the CI dashboard periodically. When the build completes, he evaluates the result: did it pass, or did it fail? If it failed, he evaluates whether the failure is related to his change or is a flaky test. | CI results page, test failure logs, Git blame (to check test ownership), Slack (asking teammates if they have seen the same flaky test) | **Think**: "Is this failure my fault or another flaky test? I can't tell." **Feel**: Anxiety when a test fails -- he cannot determine if it guards critical functionality for another team, so he cannot safely skip it. Frustration at the ambiguity: "When a flaky test blocks my PR, I can't just delete it -- I don't know if it's testing something critical for another team. So I just re-run and hope" (interview-2026-03-05-001). **Hear**: Teammates advising "just re-run it" as standard counsel. | No failure classification system -- flaky failures look identical to real failures. Raj cannot distinguish his mistakes from infrastructure noise. Shared staging databases cause non-deterministic integration test results. Hardcoded timing assumptions in async tests produce random failures. Nobody owns the flaky tests, so there is no one to ask. | Implement automated CI failure classification: label each failure as "change-related," "known flaky," or "infrastructure." Display classification prominently in CI results so engineers can make informed decisions in seconds rather than minutes of log-reading. |
| **Trial** | When CI fails on what looks like a flaky test, Raj re-runs the pipeline. He follows the team's unofficial rule: re-run up to three times before investigating. Each re-run is another 45-minute wait. Some of his teammates have written auto-retry scripts to automate this loop. | CI re-run button, auto-retry scripts (team-built workaround), Slack (reporting yet another flaky failure), CI dashboard (watching the re-run progress) | **Think**: "We've normalized a broken feedback loop. That should terrify someone" (interview-2026-03-05-001). **Feel**: Exasperation that the organization has codified dysfunction as process. A deep sense that his time is not valued. Also a dark humor about it -- the auto-retry scripts represent engineers applying their skills to automate a workaround rather than fix the root cause. **See**: The entire team doing the same thing. The behavior is contagious and self-reinforcing -- when everyone retries, retrying feels normal. | The retry loop multiplies the 45-minute wait by 2-4x per PR. Last sprint, Raj spent 11 hours waiting for CI -- "That's more than a full day of my week gone" (interview-2026-03-05-001). The unofficial 3-retry rule normalizes broken infrastructure. Auto-retry scripts mask the problem from management visibility. No quarantine mechanism exists to separate flaky tests from the critical path. | Deploy a flaky test quarantine system: automatically identify non-deterministic tests (10%+ flake rate over 100 runs), run them in a non-blocking quarantine lane so they do not block PR merges. Track quarantined test results for safety but remove them from the critical feedback loop. |
| **Adoption** | When CI eventually passes (after one or more retries), Raj merges his PR. He moves on to the next change and repeats the entire cycle. He has adapted his workflow around CI friction: batching changes to reduce push frequency, working on multiple PRs simultaneously to fill wait time, and mentally budgeting 11+ hours per sprint as "CI tax." He onboards new hires into this culture of workarounds. | PR merge button, Jira/task tracker (moving to next ticket), Slack (announcing merge), new hire onboarding sessions | **Think**: "If you save 30 minutes per engineer per day across 200 engineers, that's 100 engineering hours per day. You don't need a business case for that, you need a fire truck" (interview-2026-03-05-001). **Feel**: Residual frustration that this is "just how things are." Embarrassment when onboarding new hires into a broken system: "That's not an onboarding experience, that's a hazing ritual" (interview-2026-03-05-001). Despite adopting the workflow, he has not adopted trust -- he does not trust CI results, the build cache, or the test suite. **Say vs. Do**: He advocates loudly for fixing CI but continues to participate in the retry culture because there is no alternative. | New engineers lose their entire first week to environment setup and CI friction -- first PR lands on day 8 instead of day 1-2. The broken system perpetuates itself: new hires learn the retry culture from day one. Build cache abandonment is widespread -- half the team runs full local builds, negating the infrastructure investment. No ownership of shared infrastructure means problems compound indefinitely. | Establish clear ownership for CI infrastructure, flaky tests, and build cache. Publish CI health metrics (build time, flaky rate, cache hit rate) on an engineering dashboard. Create a streamlined new-hire CI onboarding path where the first push experience demonstrates a working, fast pipeline. Designate a team accountable for build cache reliability with on-call rotation and SLOs. |

## 3. Emotional Arc

| Stage | Emotional State | Indicator |
|-------|----------------|-----------|
| Awareness | Negative | Dread and resignation before even pushing code. Raj has learned to expect failure, which colors the start of every CI interaction with pessimism. The #build-cache-woes Slack channel provides constant ambient negativity. |
| Interest | Negative | Impatience and frustration at the 45-minute wait for a one-line change. The rational knowledge that this waste scales to 100 eng-hours/day intensifies the emotional response from personal annoyance to organizational outrage. |
| Evaluation | Negative | Anxiety and helplessness when facing an ambiguous CI failure. The inability to distinguish flaky failures from real failures creates a decision paralysis that is uniquely demoralizing -- "I just re-run and hope" conveys a loss of agency. |
| Trial | Strongly Negative | This is the emotional low point. Exasperation peaks during the retry loop, where each 45-minute re-run compounds the feeling that the system does not respect the engineer's time. The cultural normalization of retrying ("We've normalized a broken feedback loop") adds a layer of existential frustration beyond the immediate time waste. |
| Adoption | Mixed (Negative with Resigned Acceptance) | Raj has adapted to the system but has not made peace with it. He feels embarrassed when onboarding new hires ("hazing ritual"), frustrated by the organizational inertia, but also energized by the possibility of change -- his "fire truck" comment shows he is ready to champion a solution and sees the opportunity clearly. |

**Overall emotional arc**: The journey is overwhelmingly negative, with sentiment at its lowest during the Trial stage (the retry loop). There is no true positive peak in the current experience. The Awareness stage begins with resigned dread, which deepens through Interest (waste awareness) and Evaluation (ambiguity anxiety), hits bottom during Trial (the compounding retry loop), and settles into a conflicted Adoption state where adaptation coexists with unresolved frustration. The only forward-looking energy comes from Raj's self-calculated ROI and his advocacy for change -- he has not given up, but his patience is running out. The emotional trajectory reveals that the CI pipeline is not just a productivity problem but a morale and trust problem: engineers do not trust their own tools.

## 4. Moments of Truth

### Moment of Truth 1: The First CI Failure After Push
- **Stage**: Evaluation
- **Description**: The moment Raj sees a red CI status on his PR and must determine whether the failure is his fault or a flaky test. This is the point where the feedback loop either builds trust or erodes it.
- **Evidence**: "When a flaky test blocks my PR, I can't just delete it -- I don't know if it's testing something critical for another team. So I just re-run and hope." (interview-2026-03-05-001). The inability to classify failures forces a decision between blind retrying and time-consuming investigation.
- **Current Outcome**: Negative. Raj defaults to re-running because investigation is too costly (reading logs for a test he does not own, in a codebase he may not understand). The feedback loop fails to provide actionable information.
- **Desired Outcome**: Every CI failure is immediately classified as "change-related," "known flaky," or "infrastructure." Raj sees at a glance whether to investigate his code or ignore the noise.
- **Risk Level**: **High** -- This moment determines whether an engineer spends 45 minutes or 3+ hours on a single PR. It is the single highest-leverage intervention point in the journey.

### Moment of Truth 2: The Third Consecutive Retry
- **Stage**: Trial
- **Description**: The moment when Raj hits the re-run button for the third time on the same PR, having now spent 2+ hours waiting for a change that should have taken minutes to validate.
- **Evidence**: "Last sprint I spent 11 hours just waiting for CI. That's more than a full day of my week gone." (interview-2026-03-05-001). The team's unofficial 3-retry rule means this moment occurs regularly -- it is not an edge case but a routine experience.
- **Current Outcome**: Negative. After three retries, Raj may finally investigate, or the build may pass by luck. Either way, 2+ hours have been consumed. The experience reinforces the belief that CI is adversarial.
- **Desired Outcome**: Flaky tests are quarantined. The first CI run succeeds or fails deterministically. Re-runs are rare exceptions, not standard procedure.
- **Risk Level**: **High** -- This is the emotional low point of the journey. Repeated exposure to this moment drives disengagement, cynicism, and ultimately attrition risk for high-performing engineers who have options.

### Moment of Truth 3: The New Hire's First CI Experience
- **Stage**: Adoption
- **Description**: The moment a new engineer on Raj's team pushes their first PR and encounters the 45-minute wait followed by a flaky failure they cannot interpret.
- **Evidence**: "I onboarded a new hire last month. She spent her entire first week fighting Docker instead of writing code. Her first PR landed on day eight. That's not an onboarding experience, that's a hazing ritual." (interview-2026-03-05-001).
- **Current Outcome**: Negative. The new hire's first impression of the engineering culture is one of broken tools and workaround culture. Their confidence is undermined before they have written meaningful code. Raj feels embarrassed.
- **Desired Outcome**: A new hire's first CI run completes in under 15 minutes with a deterministic result. Their first PR lands within 2 days. The onboarding experience demonstrates that the organization values engineering productivity.
- **Risk Level**: **High** -- First impressions shape long-term engagement. A demoralizing onboarding experience affects retention, ramp-up speed, and the new hire's willingness to advocate for the company as an employer.

### Moment of Truth 4: Discovering the Build Cache Is Broken
- **Stage**: Interest
- **Description**: The moment an engineer (new or existing) realizes that the Bazel remote cache -- which is supposed to accelerate builds -- is not working, and no one owns it or is fixing it.
- **Evidence**: "The cache was supposed to save us time. Instead it's become another thing that's broken that nobody fixes." (interview-2026-03-05-001). The existence of #build-cache-woes as a dedicated venting channel confirms this is a widely recognized, unaddressed problem.
- **Current Outcome**: Negative. Engineers lose trust not just in the cache but in the organization's ability to maintain its own infrastructure. Half the team has abandoned remote caching entirely, running full local builds.
- **Desired Outcome**: The build cache reliably hits 80%+ for unchanged targets. Cache health is monitored with alerts. An owner is accountable.
- **Risk Level**: **Medium** -- While the cache is not the primary time sink (flaky tests and raw build time are worse), it represents a trust-eroding signal: "the organization deploys tools but does not maintain them."

### Moment of Truth 5: The "Should I Escalate?" Decision
- **Stage**: Adoption
- **Description**: The recurring moment when Raj considers escalating the CI problem to leadership but decides not to, because the workaround culture has made the dysfunction invisible to management.
- **Evidence**: "We've normalized a broken feedback loop. That should terrify someone." (interview-2026-03-05-001). The word "someone" implies Raj believes a decision-maker should be alarmed but is not, because the problem is masked by workarounds (auto-retry scripts, context-switching).
- **Current Outcome**: Negative. The problem persists because its severity is hidden. Auto-retry scripts, in particular, reduce the visible symptom (repeated manual re-runs) while preserving the underlying cost.
- **Desired Outcome**: CI health metrics are published transparently. The cost of CI friction is quantified and visible to engineering leadership. Engineers like Raj do not need to escalate because the data escalates itself.
- **Risk Level**: **Medium** -- Failure to surface this problem risks losing engineers like Raj who have the insight to diagnose organizational dysfunction and the motivation to fix it. If they conclude the organization will not act, they leave.

## 5. Friction Points and Drop-Off Risks

1. **45-minute build time for trivial changes**
   - **Location**: Interest stage, CI pipeline execution
   - **Description**: Every code push triggers a full 45-minute CI build regardless of change size or scope. No intelligent test selection, no effective caching.
   - **Evidence**: "Our builds take 45 minutes on average. For a backend service change -- even a one-line fix" (interview-2026-03-05-001). Insight-2026-03-27-001 confirms this as the primary CI pipeline bottleneck.
   - **Severity**: High
   - **Drop-Off Risk**: High -- Engineers batch changes to avoid pushing frequently, reducing iteration speed. Some defer pushes to end-of-day to avoid multiple wait cycles, degrading code review turnaround.

2. **Flaky test failures blocking PRs with no classification**
   - **Location**: Evaluation stage, CI results interpretation
   - **Description**: ~50% of CI failures are non-deterministic, caused by shared staging databases and hardcoded timing assumptions. Engineers cannot distinguish flaky failures from real ones.
   - **Evidence**: "Half the time it fails on a flaky test that has nothing to do with my change" (interview-2026-03-05-001). Insight-2026-03-27-001 theme: "Flaky test normalization."
   - **Severity**: High
   - **Drop-Off Risk**: High -- This is the single most demoralizing friction point because it combines time waste with loss of agency. Engineers who cannot trust CI results stop treating CI as a quality gate.

3. **Retry loop consuming 2-4x the base build time**
   - **Location**: Trial stage, CI re-run cycle
   - **Description**: The unofficial 3-retry rule means a single PR can consume 3-4 hours of CI time (3-4 runs at 45 minutes each). Auto-retry scripts automate but do not solve the problem.
   - **Evidence**: "Last sprint I spent 11 hours just waiting for CI" (interview-2026-03-05-001). Insight-2026-03-27-001: "Flaky test triage is impossible."
   - **Severity**: High
   - **Drop-Off Risk**: High -- The compounding effect of retries is the primary driver of the 11 hours/sprint waste figure. This is where engineers are most likely to disengage from caring about CI quality.

4. **Broken remote build cache**
   - **Location**: Interest stage, build execution
   - **Description**: Bazel remote cache misses constantly. Half the team has abandoned it. No owner, no monitoring, no SLO.
   - **Evidence**: "The cache was supposed to save us time. Instead it's become another thing that's broken that nobody fixes" (interview-2026-03-05-001). Dedicated #build-cache-woes Slack channel.
   - **Severity**: Medium
   - **Drop-Off Risk**: Medium -- Does not directly block work but adds 10-20 minutes to builds that could be cached. Erodes trust in platform tooling more broadly.

5. **New hire onboarding blocked by CI and environment friction**
   - **Location**: Adoption stage, first-week experience
   - **Description**: New engineers spend their entire first week on environment setup and CI troubleshooting. First PR lands on day 8 instead of day 1-2.
   - **Evidence**: "Her first PR landed on day eight. That's not an onboarding experience, that's a hazing ritual" (interview-2026-03-05-001). Insight-2026-03-27-001 theme: "Onboarding time sink."
   - **Severity**: Medium
   - **Drop-Off Risk**: Medium -- New hires are unlikely to leave in week one, but the demoralization compounds and contributes to 90-day attrition risk. Also imposes a hidden cost on senior engineers (like Raj) who spend time hand-holding instead of shipping.

6. **No ownership of shared CI infrastructure**
   - **Location**: All stages (systemic)
   - **Description**: Neither flaky tests, the build cache, nor the CI pipeline configuration have designated owners. Problems persist because no one has the authority or accountability to fix them.
   - **Evidence**: "Nobody knows who owns the cache infra" and "I don't know if it's testing something critical for another team" (interview-2026-03-05-001). Insight-2026-03-27-001 theme: "Ownership vacuum."
   - **Severity**: Medium
   - **Drop-Off Risk**: Medium -- This is the root cause that allows all other friction points to persist. Without ownership, improvements are ad hoc and unsustained.

## 6. Improvement Recommendations

| Pain Point | Stage | Recommendation | Expected Impact | Implementation Complexity |
|-----------|-------|----------------|----------------|--------------------------|
| 45-minute build time for trivial changes | Interest | Implement module-level selective test execution: use the Bazel dependency graph to run only tests in the dependency cone of modified files, rather than the full suite. Target median build time under 15 minutes. | High -- directly addresses the hero metric and the single largest time sink. Recovering 30 min/engineer/day across 200 engineers = 100 eng-hours/day. | High -- requires build graph analysis tooling and careful validation that skipped tests are truly unaffected. Start with conservative module-level selection. |
| Flaky test failures blocking PRs | Evaluation | Deploy an automated flaky test detection and quarantine system: track pass/fail history per test over the last 100 runs, flag tests with >10% flake rate, and move them to a non-blocking quarantine lane. Results are logged but do not block merges. | High -- eliminates ~50% of false CI failures, cutting the re-run rate from ~50% to <10%. Restores trust in CI as a deterministic quality gate. | Medium -- requires test result history storage, a classification engine, and CI pipeline integration to separate quarantined results from blocking results. |
| No failure classification in CI results | Evaluation | Add failure classification labels to the CI results UI: "change-related failure" (red), "known flaky test" (yellow), "infrastructure failure" (gray). PR status checks reflect only change-related failures. | High -- transforms the Evaluation stage from anxious log-reading to a 5-second glance. Enables informed decision-making instead of blind retrying. | Low -- once flaky test detection exists, surfacing the classification in the UI is a labeling and display change. |
| Retry loop consuming 2-4x base build time | Trial | The quarantine system (above) eliminates the need for most retries. Additionally, provide a "re-run failed tests only" option that re-executes only the specific failed tests, not the entire suite, reducing re-run time from 45 minutes to 5-10 minutes. | High -- directly reduces the 11 hours/sprint waste by eliminating unnecessary full re-runs. Transforms the retry experience from a 45-minute gamble to a targeted 5-minute verification. | Medium -- requires CI pipeline support for partial re-runs, plus test isolation to ensure re-running a subset is safe. |
| Broken remote build cache | Interest | Audit the Bazel remote cache configuration: fix cache key stability, verify network throughput to the cache cluster, and implement cache health monitoring with alerts when hit rate drops below 70%. Designate a named owner (team + on-call rotation) with an 80% hit rate SLO. | Medium -- improves build times by 10-20 minutes for cached targets. Also sends a trust signal: "we maintain what we deploy." | Medium -- cache debugging can be unpredictable. Time-box the audit to 2 weeks; if fundamental architecture issues emerge, evaluate alternative cache backends. |
| New hire onboarding blocked by CI/environment friction | Adoption | Create a "golden path first push" onboarding script: a single command that sets up the local environment, creates a trivial code change, and pushes it through CI. The new hire's first CI experience should complete in under 15 minutes with a deterministic pass. Pair this with a 30-minute "how CI works here" onboarding session. | Medium -- reduces time-to-first-PR from 8 days to under 3 days. Transforms the emotional first impression from "hazing ritual" to "this team invests in my success." | Low -- once CI is faster and flaky tests are quarantined, the onboarding improvement is primarily a scripting and documentation effort. |
| No ownership of shared CI infrastructure | All stages | Publish a CI infrastructure ownership map: cache owner, flaky test quarantine owner, pipeline configuration owner. Each owner has an SLO, an on-call rotation, and a public dashboard. Escalation paths are documented. Present to VP Engineering with the 100 eng-hours/day cost figure to secure staffing. | High -- this is the systemic enabler for all other improvements. Without ownership, fixes decay and the cycle restarts. | Low -- the organizational decision is simple; the political challenge is securing commitment. The quantified cost (100 eng-hours/day) provides the business case. |

## 7. Interview Evidence Index

| Stage | Interview IDs | Insight IDs | Key Quotes |
|-------|--------------|-------------|------------|
| Awareness | interview-2026-03-05-001 | insight-2026-03-27-001 | Raj checks #build-cache-woes Slack channel before pushing, a behavioral signal that CI health anxiety starts before the build even begins. The channel's existence is documented as a "Surprise" in insight-2026-03-27-001: "The existence of a dedicated channel for venting about build cache failures signals a systemic, widely-recognized problem." |
| Interest | interview-2026-03-05-001 | insight-2026-03-27-001 | "Our builds take 45 minutes on average. For a backend service change -- even a one-line fix -- I push, wait 45 minutes." / "The cache was supposed to save us time. Instead it's become another thing that's broken that nobody fixes." (interview-2026-03-05-001) |
| Evaluation | interview-2026-03-05-001 | insight-2026-03-27-001 | "When a flaky test blocks my PR, I can't just delete it -- I don't know if it's testing something critical for another team. So I just re-run and hope." (interview-2026-03-05-001) |
| Trial | interview-2026-03-05-001 | insight-2026-03-27-001 | "Last sprint I spent 11 hours just waiting for CI. That's more than a full day of my week gone." / "We've normalized a broken feedback loop. That should terrify someone." (interview-2026-03-05-001) |
| Adoption | interview-2026-03-05-001 | insight-2026-03-27-001 | "She spent her entire first week fighting Docker instead of writing code. Her first PR landed on day eight. That's not an onboarding experience, that's a hazing ritual." / "If you save 30 minutes per engineer per day across 200 engineers, that's 100 engineering hours per day. You don't need a business case for that, you need a fire truck." (interview-2026-03-05-001) |
