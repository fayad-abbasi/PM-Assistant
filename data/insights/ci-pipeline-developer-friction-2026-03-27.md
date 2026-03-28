---
id: insight-2026-03-27-001
title: "CI Pipeline Friction: Slow Builds and Flaky Tests Drain Engineering Productivity"
type: single
linked_interviews:
  - interview-2026-03-05-001
themes:
  - "CI pipeline bottleneck"
  - "Flaky test normalization"
  - "Local environment fragility"
  - "Broken build cache infrastructure"
  - "Onboarding time sink"
confidence: high
impact: high
tags:
  - ci-cd
  - developer-friction
  - inner-loop-speed
  - outer-loop-speed
  - pain-point
  - toil-reduction
  - backend-engineer
  - testing-infrastructure
  - build-systems
  - local-dev-environment
  - developer-onboarding
  - reliability
  - time-saving
status: active
created_at: 2026-03-27T10:00:00Z
---

## Fragment Card

### Tensions
- **Speed vs. safety**: Raj wants fast CI feedback but cannot skip or delete flaky tests because they may guard critical paths for other teams. The desire to move quickly conflicts with shared ownership of the test suite.
- **Caching promise vs. caching reality**: Remote Bazel caching was adopted to speed builds, but constant cache misses mean engineers run full builds anyway, negating the investment.
- **Individual velocity vs. shared infrastructure**: A single engineer's productivity is held hostage by shared staging databases, shared test suites, and shared cache infrastructure that no one owns.

### Friction
- **45-minute CI builds** for even one-line backend changes, with frequent re-runs due to flaky tests.
- **11 hours per sprint** personally spent waiting for CI — more than a full workday per week.
- **Local environment setup takes 2-3 days** for existing engineers and up to a full week for new hires. The 400-line docker-compose file breaks regularly.
- **Broken remote build cache**: Bazel remote cache misses constantly, forcing full local builds. No clear owner.
- **Flaky test triage is impossible**: Engineers cannot determine if a flaky test guards critical functionality for another team, so they default to re-running rather than investigating.

### Contradictions
- **Stated process vs. actual behavior**: The team has Bazel remote caching that is "supposed to save time," yet half the team has abandoned it and runs full builds locally. The tool meant to solve the problem has become part of the problem.
- **Re-run culture**: The team has an "unofficial rule" to re-run CI up to three times before investigating, effectively codifying a broken process as standard practice. Some engineers have even automated the retries with scripts — automating a workaround for a broken system rather than fixing the system.

### Surprises
- **Quantified waste at scale**: Raj calculated that saving 30 minutes per engineer per day across 200 engineers equals 100 engineering hours per day. This is not a team-level complaint — it is an organization-level productivity crisis with a concrete cost envelope.
- **Onboarding as "hazing ritual"**: A new hire's first PR did not land until day 8, with the entire first week consumed by environment setup. Raj frames this not as a nuisance but as a cultural failure.
- **#build-cache-woes Slack channel**: The existence of a dedicated channel for venting about build cache failures signals a systemic, widely-recognized problem that has not been escalated to a decision-maker.

### Real Needs
- Engineers need a CI pipeline that provides reliable, fast feedback (under 15 minutes) so they can iterate confidently without losing hours to waiting and retries.
- Engineers need flaky tests to be quarantined from the critical path so that non-deterministic failures do not block unrelated PRs.
- Engineers need a local development environment that can be stood up reliably in minutes, not days, with stable service dependencies.
- Engineers need build cache infrastructure that actually works and has a clear owner accountable for its reliability.

## Thread-Pulling Analysis

### Echo
- **"Flaky"** — Raj uses this word repeatedly, signaling it is the most emotionally loaded concept in his CI experience. Flakiness is not a minor annoyance; it represents unpredictability and loss of control.
- **"Nobody owns"** — Repeated for both flaky tests ("nobody owns the flaky tests") and cache infrastructure ("nobody knows who owns the cache infra"). Ownership vacuum is a recurring frustration.
- **Time quantification** — Raj repeatedly quantifies wasted time (45 minutes, 11 hours, day 8, 100 hours/day), indicating he has internalized the cost and views it as objectively unreasonable.

### Tell Me More
- When asked "what makes the tests flaky?" Raj gave a detailed, multi-cause answer (shared staging DB, hardcoded sleeps, unclear ownership). This depth suggests he has spent significant time diagnosing the problem himself — a sign of high engagement and deep domain knowledge on this pain point.

### Specific Instance
- **New hire onboarding**: "I onboarded a new hire last month. She spent her entire first week fighting Docker instead of writing code. Her first PR landed on day eight." This is a concrete, recent, vivid example that grounds the general claim about onboarding friction.
- **11 hours last sprint**: A specific, self-timed measurement from his most recent sprint, not a vague estimate.

### Walk Me Through — Actual CI Workflow
1. Push code change
2. Wait 45 minutes for CI
3. CI fails (often on a flaky test unrelated to the change)
4. Cannot determine if the test is safe to skip
5. Re-run CI (up to 3 times per unofficial team policy)
6. Wait another 45 minutes per re-run
7. If still failing after 3 re-runs, investigate

**Intended workflow**: Push, get feedback in minutes, iterate. The gap between intended and actual is enormous — a 5-minute intended loop has become a multi-hour ordeal.

### Why Ladder
- **Surface complaint**: "CI takes too long"
- **Immediate cause**: 45-minute build times + flaky test failures requiring re-runs
- **Systemic cause**: No flaky test quarantine system, no test ownership model, broken remote build cache, shared mutable staging databases used in integration tests
- **Underlying need**: Deterministic, fast feedback on code changes so engineers can maintain flow state and ship with confidence

### Contrast
- **Cache expectation vs. reality**: "The cache was supposed to save us time. Instead it's become another thing that's broken that nobody fixes." Raj evaluates tools by whether they deliver on their promise — a broken tool is worse than no tool because it adds complexity without value.
- **Onboarding expectation vs. reality**: "That's not an onboarding experience, that's a hazing ritual." The contrast between what onboarding should feel like (productive, welcoming) and what it actually feels like (frustrating, adversarial) reveals a strong emotional response.

## Jobs to Be Done

### Functional Jobs
- "When I push a backend code change, I want to get reliable CI feedback in under 15 minutes, so I can iterate quickly and ship multiple changes per day."
- "When a CI test fails, I want to immediately know whether the failure is related to my change or is a known flaky test, so I can decide whether to investigate or proceed."
- "When I onboard a new engineer to my team, I want them to have a working local environment within hours, so they can start contributing code in their first week."
- "When I run a build locally, I want the remote cache to reliably provide cached artifacts, so I don't waste time rebuilding unchanged dependencies."

### Emotional Jobs
- "I want to feel confident that when CI passes, my code is actually correct — and when it fails, the failure is meaningful."
- "I want to feel respected by my tooling — that the organization values my time enough to invest in reliable infrastructure."
- "I want to feel proud when onboarding new teammates, not embarrassed by a broken setup process."

### Social Jobs
- "I want to be seen as a productive, high-output engineer by my team and management — not someone who spends a full day per week waiting for CI."
- "I want my team to be seen as efficient and well-run — not as a group that has normalized broken processes."

## Themes

1. **CI pipeline bottleneck** — 45-minute builds with frequent flaky failures create a multi-hour feedback loop that dominates the engineering day. This is the primary theme, mentioned throughout and quantified precisely.
2. **Flaky test normalization** — The team has institutionalized retrying flaky tests (unofficial 3-retry rule, auto-retry scripts) rather than fixing the root cause. A broken feedback loop has been accepted as normal.
3. **Local environment fragility** — A 400-line docker-compose file with 7+ service dependencies breaks regularly, creating multi-day onboarding delays and ongoing maintenance burden.
4. **Broken build cache infrastructure** — Bazel remote caching misses constantly, half the team has abandoned it, and no one owns the infrastructure. A dedicated Slack channel (#build-cache-woes) exists purely for venting.
5. **Onboarding time sink** — New engineers lose their entire first week to environment setup rather than productive work, with first PRs landing on day 8 instead of day 1-2.
6. **Ownership vacuum** — Neither flaky tests nor build cache infrastructure have clear owners, leading to chronic neglect and workaround culture.

## Pain Points

### 1. Slow CI Builds
- **Description**: CI pipeline takes 45 minutes per run for backend service changes, including trivial one-line fixes.
- **Severity**: High — blocks the core development loop multiple times per day.
- **Frequency**: Constant — every code push triggers this wait.
- **Current workaround**: Engineers context-switch to other tasks while waiting, fragmenting focus and reducing throughput.
- **Supporting quote**: "Last sprint I spent 11 hours just waiting for CI. That's more than a full day of my week gone."

### 2. Flaky Tests Blocking PRs
- **Description**: Integration tests fail non-deterministically due to shared staging databases and hardcoded timing assumptions, blocking unrelated PRs.
- **Severity**: High — multiplies the already-long CI wait by 2-4x per PR.
- **Frequency**: Frequent — "half the time" CI fails on a flaky test.
- **Current workaround**: Re-run CI up to three times (unofficial team rule). Some engineers have written auto-retry scripts.
- **Supporting quote**: "When a flaky test blocks my PR, I can't just delete it — I don't know if it's testing something critical for another team. So I just re-run and hope."

### 3. Fragile Local Development Environment
- **Description**: Local setup requires 7+ microservices, Kafka, Redis, and Postgres via a 400-line docker-compose file that breaks when upstream services change.
- **Severity**: High — completely blocks productivity for new hires; causes recurring disruptions for existing engineers.
- **Frequency**: Occasional for existing engineers (breaks "every few weeks"), constant for new hires (2-3 day setup, up to a full week).
- **Current workaround**: Senior engineers manually help new hires troubleshoot Docker issues; no self-service path.
- **Supporting quote**: "She spent her entire first week fighting Docker instead of writing code. Her first PR landed on day eight. That's not an onboarding experience, that's a hazing ritual."

### 4. Broken Remote Build Cache
- **Description**: Bazel remote caching was deployed but misses constantly, providing no speed benefit and adding complexity.
- **Severity**: Medium — forces full local builds, adding time but not fully blocking work.
- **Frequency**: Constant — cache misses are the norm, not the exception.
- **Current workaround**: Half the team has abandoned remote caching and runs full builds locally.
- **Supporting quote**: "The cache was supposed to save us time. Instead it's become another thing that's broken that nobody fixes."

### 5. No Ownership of Shared Infrastructure
- **Description**: Flaky tests and build cache infrastructure have no designated owner, leading to chronic neglect.
- **Severity**: Medium — root cause of pain points 2 and 4; without ownership, problems compound indefinitely.
- **Frequency**: Constant — structural issue, not episodic.
- **Current workaround**: Engineers vent in #build-cache-woes Slack channel; workarounds proliferate instead of fixes.
- **Supporting quote**: "Nobody knows who owns the cache infra."

## Feature Requests

### Explicit
1. **Reduce CI build time to under 15 minutes** — Direct request; maps to the functional job of fast, reliable feedback. (Functional)
2. **Flaky test quarantine system** — Direct request to isolate flaky tests so they do not block PRs. (Functional)

### Implicit
1. **Test ownership model** — Raj describes not knowing who owns flaky tests as a key blocker. A system that assigns and tracks test ownership would address this. (Functional)
2. **Simplified local development environment** — The docker-compose pain implies a need for a lighter-weight, more resilient local setup (e.g., dev containers, service virtualization, or a managed dev environment). (Functional)
3. **Build cache reliability and ownership** — The abandoned Bazel cache implies a need for either fixing the cache or replacing it with something that works and has a clear owner. (Functional)
4. **Onboarding automation** — The new-hire story implies a need for a streamlined, self-service onboarding path that does not depend on senior engineer hand-holding. (Functional + Emotional)
5. **CI failure triage tooling** — The inability to distinguish flaky failures from real failures implies a need for better CI failure classification and reporting. (Functional + Emotional)

## Key Quotes

1. **"Last sprint I spent 11 hours just waiting for CI. That's more than a full day of my week gone."** — Quantifies the personal cost of slow CI in concrete, relatable terms. Useful for stakeholder communication.

2. **"We've normalized a broken feedback loop. That should terrify someone."** — The most strategically powerful quote. Raj recognizes that the problem is not just the tooling but the cultural acceptance of broken tooling. This reframes the issue from a technical fix to an organizational priority.

3. **"She spent her entire first week fighting Docker instead of writing code. Her first PR landed on day eight. That's not an onboarding experience, that's a hazing ritual."** — Vivid, emotionally resonant story that connects CI/local-dev friction to talent retention and employer brand.

4. **"If you save 30 minutes per engineer per day across 200 engineers, that's 100 engineering hours per day. You don't need a business case for that, you need a fire truck."** — Ready-made executive pitch. Raj has already done the ROI math and framed it with urgency.

5. **"The cache was supposed to save us time. Instead it's become another thing that's broken that nobody fixes."** — Captures the theme of infrastructure solutions that create new problems when deployed without ownership and maintenance commitment.

## Sentiment

- **Overall tone**: Negative — Raj is deeply frustrated with the current state of CI and local development infrastructure.
- **Dominant emotions**: Frustration (with wasted time and broken tools), exasperation (with normalized dysfunction), urgency (wants this fixed now, not eventually).
- **Inflection points**: Sentiment is consistently negative throughout but intensifies when discussing the new hire onboarding experience (shifts from personal frustration to empathetic anger on behalf of the new engineer) and when quantifying the org-wide impact (shifts from complaint to advocacy, framing the case for action).

## Confidence & Impact

- **Confidence**: high — Raj provides multiple specific, quantified examples (11 hours/sprint, 45-minute builds, day-8 first PR, 200 engineers x 30 min/day). He describes concrete workarounds (auto-retry scripts, unofficial 3-retry rule, abandoned cache). His claims are internally consistent and corroborated by behavioral evidence (the existence of #build-cache-woes channel, team-wide retry culture). The only limitation is that this is a single interview from one team (Payments, backend) — cross-team validation would strengthen the signal further.

- **Impact**: high — The pain affects every code push for every backend engineer. Raj estimates the org-wide cost at 100 engineering hours per day. The friction compounds: slow CI leads to fewer iterations per day, flaky tests erode trust in the test suite, broken local environments delay onboarding and hurt retention. There are no good workarounds — retrying is time-expensive and auto-retry scripts just mask the underlying problem. Addressing this would improve developer velocity, onboarding speed, engineering morale, and talent retention.

## Opportunity Statement

> **Engineers need a** faster, more reliable CI pipeline with deterministic test execution
> **because** 45-minute builds combined with flaky tests that no one owns have created a multi-hour feedback loop that engineers have normalized rather than fixed,
> **which results in** 11+ hours per engineer per sprint lost to waiting, multi-day onboarding delays for new hires, and an organizational culture that accepts broken tooling as the cost of doing business.
> **If we solve this, we could** recover an estimated 100 engineering hours per day across 200 engineers, cut new-hire time-to-first-PR from 8 days to under 3, and restore trust in the CI feedback loop — directly improving velocity, retention, and engineering satisfaction.

## Recommended Next Steps

### 1. Validate breadth of CI pain across teams (Priority: High — do first)
- **Action**: Conduct 4-6 additional interviews with engineers from different teams (frontend, SRE, data engineering) to confirm whether CI friction is org-wide or concentrated in backend/Payments.
- **Hypothesis**: If CI pipeline friction is reported by engineers across 3+ teams with similar severity, then this is an organization-level infrastructure problem, not a team-specific one.
- **Success metric**: Cross-team signal consistency (same themes appearing in 60%+ of interviews).
- **Artifact to create**: Batch insight (type: batch) synthesizing cross-team CI friction patterns.

### 2. Quantify CI waste with analytics data (Priority: High — do in parallel with #1)
- **Action**: Pull CI pipeline metrics — median build time, p95 build time, flaky test re-run rate, and time-to-merge — to validate Raj's self-reported numbers with system data.
- **Hypothesis**: If system data confirms 40+ minute median build times and >30% flaky failure rate, then Raj's 11 hours/sprint estimate is representative, not an outlier.
- **Success metric**: Quantitative confirmation of build times and flaky failure rates within 20% of Raj's reported figures.
- **Artifact to create**: Analytics summary (via `/discover analytics`).

### 3. Draft PRD for flaky test quarantine system (Priority: Medium — after validation)
- **Action**: If cross-team interviews and analytics confirm the signal, create a PRD for a flaky test quarantine system as the highest-ROI intervention.
- **Hypothesis**: If flaky tests are automatically quarantined (run but non-blocking), then CI false-failure rate will drop by 50%+, reducing re-runs and saving 15+ minutes per engineer per failed build.
- **Success metric**: Reduction in CI re-run rate from current baseline to <10%; reduction in median time-to-merge.
- **Artifact to create**: PRD (via `/prd generate`), linked to this insight.
