---
id: interview-2026-03-07-001
title: "1:1 — David Okafor, SRE, Platform Team"
date: 2026-03-07
interviewee: David Okafor
role: Senior SRE
company: Internal — Platform Team
tags: [observability, sre, toil-reduction, self-service]
status: analyzed
created_at: 2026-03-07T11:30:00Z
---

# 1:1 — David Okafor, Senior SRE, Platform Team

**Date:** 2026-03-07
**Interviewer:** DevEx PM (onboarding conversations)
**Duration:** 40 minutes
**Format:** Video call

---

**DevEx PM:** David, appreciate you making time. I'm new to DevEx and trying to understand the operational side. What's the biggest pain point for your SRE team?

**David Okafor:** Service onboarding. When a product team wants to launch a new microservice, they come to us. We have a 14-step checklist — create the repo from a template, set up CI, configure monitoring, create dashboards, set up alerts, provision infrastructure, configure service mesh, set up log aggregation, register in the service catalog, configure secrets management, set up deployment pipelines, add runbooks, configure on-call rotation, and do a production readiness review. "It takes two to three weeks to get a new service to production. Two to three weeks before a single line of business logic runs in prod. Teams plan around our backlog, not their roadmap."

**DevEx PM:** How much of that is automated?

**David Okafor:** Maybe 30%. We have Terraform modules for the infra provisioning, and the repo template gets you a skeleton. But the rest is manual — the monitoring setup, the dashboard creation, the alert configuration. Each service has slightly different needs, and our tooling doesn't handle the variance well. So an SRE sits with the team, asks questions, and configures everything by hand. "I'm a highly paid YAML editor. I spend my days copy-pasting Grafana JSON and tweaking Prometheus alert rules. That's not SRE work, that's toil."

**DevEx PM:** What happens when teams try to do it themselves?

**David Okafor:** They get it wrong. Not because they're incompetent — because the process is undocumented and full of gotchas. Last quarter, a team set up their own monitoring and missed configuring the error rate alert. Their service was throwing 500s for six hours before anyone noticed. After that incident, we pulled self-service back and made everything go through us again. "We swung from 'nobody can do anything without us' to 'let teams do it themselves' back to 'nobody can do anything without us.' The pendulum just keeps swinging because we never built the guardrails to make self-service safe."

**DevEx PM:** What about observability once services are running?

**David Okafor:** Inconsistent. Some teams have great dashboards because they happened to have an SRE embedded. Others have the bare minimum — a CPU chart and a memory chart that tell you nothing about business logic health. There's no standard. "I can tell you the p99 latency of our checkout service down to the endpoint level. For our recommendations service, I can tell you it's... running. Probably. The dashboard hasn't been updated since the engineer who built it left six months ago."

**DevEx PM:** If you could change one thing, what would it be?

**David Okafor:** Self-service service creation with built-in guardrails. A golden path — you fill out a form or run a CLI command, and you get a fully configured service with monitoring, alerts, dashboards, CI, deployment pipeline, everything. It follows our standards by default. If you want to deviate, you can, but you have to explicitly opt out of the defaults. "Don't make teams ask permission to launch a service. Make the right thing the easy thing. Pave the road and they'll walk on it."

**DevEx PM:** How do you prioritize between firefighting and building that kind of platform capability?

**David Okafor:** We don't. Firefighting always wins. We've had "build a service creation wizard" on our roadmap for three quarters. Every quarter it gets bumped because there's an incident, or a team needs hand-holding for a launch, or someone's dashboard breaks. "We're stuck in a toil trap. We can't build the automation because we're too busy doing the manual work. And we can't stop the manual work because we haven't built the automation. Something has to give."
