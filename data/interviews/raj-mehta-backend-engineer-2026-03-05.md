---
id: interview-2026-03-05-001
title: "1:1 — Raj Mehta, Backend Engineer, Payments Team"
date: 2026-03-05
interviewee: Raj Mehta
role: Senior Backend Engineer
company: Internal — Payments Team
tags: [ci-cd, backend-engineer, developer-friction, inner-loop-speed]
status: analyzed
created_at: 2026-03-05T10:00:00Z
---

# 1:1 — Raj Mehta, Senior Backend Engineer, Payments Team

**Date:** 2026-03-05
**Interviewer:** DevEx PM (onboarding conversations)
**Duration:** 30 minutes
**Format:** Video call

---

**DevEx PM:** Thanks for taking the time, Raj. I'm new to the DevEx team and trying to understand the biggest pain points engineers face day-to-day. What's the thing that frustrates you most about your development workflow?

**Raj Mehta:** The CI pipeline, hands down. Our builds take 45 minutes on average. For a backend service change — even a one-line fix — I push, wait 45 minutes, and half the time it fails on a flaky test that has nothing to do with my change. Then I re-run and wait another 45 minutes. "I've started timing it. Last sprint I spent 11 hours just waiting for CI. That's more than a full day of my week gone."

**DevEx PM:** What makes the tests flaky?

**Raj Mehta:** A mix of things. Some integration tests depend on a shared staging database that other teams are also writing to. So my test passes or fails depending on what data some other team happened to insert. There are also timing-dependent tests — things that wait for async events with hardcoded sleeps. And nobody owns the flaky tests. "When a flaky test blocks my PR, I can't just delete it — I don't know if it's testing something critical for another team. So I just re-run and hope."

**DevEx PM:** How does your team handle this?

**Raj Mehta:** We have an unofficial rule: if CI fails and it looks flaky, re-run up to three times before investigating. Everyone does it. It's become muscle memory — push, fail, re-run, re-run, re-run. Some folks have even written scripts to auto-retry. "We've normalized a broken feedback loop. That should terrify someone."

**DevEx PM:** What about your local development setup?

**Raj Mehta:** Getting the local environment running is its own adventure. Our service depends on seven other microservices, a Kafka cluster, Redis, and Postgres. The docker-compose file is 400 lines and breaks every few weeks when someone updates a service and doesn't update the compose file. New engineers on my team take two to three days to get a working local setup. "I onboarded a new hire last month. She spent her entire first week fighting Docker instead of writing code. Her first PR landed on day eight. That's not an onboarding experience, that's a hazing ritual."

**DevEx PM:** If you could fix one thing, what would it be?

**Raj Mehta:** Fix the CI pipeline. Get build times under 15 minutes and quarantine flaky tests so they don't block PRs. I know it's a big ask, but the ROI is massive. Every engineer in the company waits for CI multiple times a day. "If you save 30 minutes per engineer per day across 200 engineers, that's 100 engineering hours per day. You don't need a business case for that, you need a fire truck."

**DevEx PM:** Anything else on your mind?

**Raj Mehta:** One more thing — our build cache is broken. We're supposed to have remote caching with Bazel, but it misses constantly. Half the team has given up on it and runs full builds locally. Nobody knows who owns the cache infra. There's a Slack channel called #build-cache-woes that's just engineers venting. "The cache was supposed to save us time. Instead it's become another thing that's broken that nobody fixes."
