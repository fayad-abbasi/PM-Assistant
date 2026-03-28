# Tag Taxonomy

Definitions for all tags in `tags.json`. Every tag used in artifact frontmatter must be defined here.

---

## Domain Tags

Tags describing the platform area or engineering domain.

| Tag | Definition |
|-----|-----------|
| `ci-cd` | Continuous integration and delivery pipelines, build/deploy automation |
| `local-dev-environment` | Local setup, dev containers, environment parity, hot reload |
| `build-systems` | Build tooling, compilation, bundling, dependency resolution |
| `testing-infrastructure` | Test frameworks, test environments, flaky test management, test data |
| `sdk` | Internal SDKs, client libraries, shared packages |
| `internal-tooling` | Developer-facing tools built in-house (CLIs, dashboards, utilities) |
| `documentation` | Internal docs, API references, runbooks, onboarding guides |
| `developer-onboarding` | New engineer ramp-up, first-day experience, starter tasks |
| `observability` | Logging, metrics, tracing, alerting, dashboards |
| `service-templates` | Scaffolding, boilerplate, cookiecutters, golden paths |
| `self-service` | Capabilities engineers can use without filing tickets or asking for help |
| `api` | Internal API design, contracts, versioning, developer experience |
| `security` | Auth, secrets management, vulnerability scanning, dependency audits |
| `data-pipeline` | ETL, data flows, data transformation, ingestion |
| `integrations` | Connections between internal systems, webhooks, event buses |
| `automation` | Automated workflows, bots, scheduled tasks, rule-based actions |
| `notifications` | Alerts, build notifications, deployment notifications, Slack bots |
| `compliance` | Regulatory requirements, audit trails, data governance |

## Persona Tags

Tags identifying the internal engineer type or stakeholder role.

| Tag | Definition |
|-----|-----------|
| `backend-engineer` | Server-side engineers, API developers, service owners |
| `frontend-engineer` | UI engineers, web developers, design system consumers |
| `fullstack-engineer` | Engineers working across the stack |
| `sre` | Site reliability engineers, infrastructure, on-call |
| `tech-lead` | Technical leads, architects, senior ICs driving technical direction |
| `engineering-manager` | EMs, people managers, team leads |
| `vp-engineering` | VP/Director of Engineering, engineering leadership |
| `pm` | Product managers, product owners |
| `designer` | UX/UI designers, design system maintainers |
| `data-engineer` | Data engineers, ML engineers, analytics engineers |
| `devops-engineer` | DevOps, platform engineers, release engineers |
| `new-hire` | Recently onboarded engineers, first 90 days |

## Priority Tags

Tags indicating urgency or importance level.

| Tag | Definition |
|-----|-----------|
| `critical` | Must address immediately — blocking or high-risk |
| `high` | Important — significant impact, address this quarter |
| `medium` | Moderate impact — plan for upcoming cycles |
| `low` | Nice to have — address when capacity allows |

## Theme Tags

Tags describing the nature of the insight, request, or problem.

| Tag | Definition |
|-----|-----------|
| `pain-point` | An identified developer frustration or problem |
| `feature-request` | A specific capability engineers have asked for |
| `developer-friction` | Unnecessary steps, slowdowns, or confusion in developer workflows |
| `toil-reduction` | Eliminating repetitive manual work that could be automated |
| `cognitive-load` | Mental overhead from complexity, poor abstractions, or unclear patterns |
| `inner-loop-speed` | Code → build → test → debug cycle speed on a developer's machine |
| `outer-loop-speed` | PR → CI → review → merge → deploy cycle speed |
| `adoption` | Getting engineers to start using a platform capability |
| `developer-satisfaction` | Overall developer happiness, survey scores, sentiment |
| `workflow` | Related to engineering processes, task flows, or sequences |
| `performance` | Speed, latency, throughput, responsiveness |
| `scalability` | Ability to handle growth in engineers, services, or load |
| `reliability` | Uptime, error rates, consistency, fault tolerance |
| `self-service` | Enabling engineers to accomplish tasks without dependencies on other teams |
| `discoverability` | How easily engineers find tools, docs, APIs, and capabilities |
| `migration` | Moving teams from old systems/patterns to new ones |
| `backward-compatibility` | Ensuring changes don't break existing consumers |
| `cost-reduction` | Reducing infrastructure or operational costs |
| `time-saving` | Reducing time spent on engineering tasks |
| `collaboration` | Cross-team coordination, shared ownership, contribution models |

## Stage Tags

Tags indicating where in the product lifecycle an artifact sits.

| Tag | Definition |
|-----|-----------|
| `discovery` | Exploring problems, gathering insights, validating needs |
| `validation` | Testing hypotheses, prototyping, experiments |
| `build` | Active development, implementation |
| `launch` | Internal rollout, release, communication |
| `adoption` | Driving usage, measuring uptake, removing barriers |
| `maturity` | Stable capability, maintenance, incremental improvement |
