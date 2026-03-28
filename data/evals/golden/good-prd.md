---
id: eval-golden-prd-good
title: "Golden Example — High Quality PRD"
status: draft
priority: high
linked_insights: [insight-2026-03-05-001]
okr_ids: []
roadmap_ids: []
tags: [automation, pm, workflow]
created_at: 2026-03-12T00:00:00Z
updated_at: 2026-03-12T00:00:00Z
---

# PRD: Automated PRD-to-Jira Ticket Generation

## Problem Statement

Product managers spend 3-4 hours per medium-sized feature manually recreating PRD content as Jira tickets, and up to two full days for large releases. This manual translation introduces sync drift: when requirements change, there is no link between the PRD paragraph and the implementing ticket, leading to stale tickets and incorrect implementations.

**Evidence from research:**

- **insight-2026-03-05-001** (interview with Sarah Chen, Senior PM, Acme Corp): *"It feels like I'm a human copy-paste machine. I went to business school for this?"* Sarah reported spending 3-4 hours per feature on ticket creation alone.
- Sarah's team of six PMs loses approximately 40 person-hours per month to ticket creation and synchronization — a full person-month per quarter of administrative overhead.
- Sync failures have caused teams to ship incorrect features: *"I've missed updating tickets before, and we shipped the wrong thing. That was a bad week."* In one case, three teams worked off stale tickets for nearly a full sprint after a compliance requirement changed.
- Existing integrations (Confluence-to-Jira, standalone AI tools) fail because they cannot parse PRD structure or require a separate application outside the PM's existing workflow.

## Hypothesis

**I BELIEVE THAT** providing automated, structure-aware PRD-to-Jira ticket generation with bidirectional sync detection **WILL** reduce ticket creation time by at least 75% and eliminate sync drift **FOR** product managers who write PRDs and manage Jira backlogs **BECAUSE** interview research shows PMs already have well-structured PRDs with acceptance criteria but lack tooling that understands that structure and maintains the PRD-to-ticket linkage over time.

## Personas

### Primary: The Overloaded PM (Early Adopter)

- **Name:** Sarah Chen
- **Role:** Senior Product Manager at a mid-to-large SaaS company (50-500 engineers)
- **Adoption curve segment:** Innovator / Early Adopter — actively seeking workflow automation, has already tried Confluence integrations and AI tools
- **Goals:** Spend more time on customer research and strategic decisions; less on administrative ticket management
- **Pain points:** 3-4 hours per feature on manual ticket creation; missed ticket updates causing incorrect implementations; maintains a fragile manual spreadsheet mapping PRD sections to Jira IDs
- **Behavioral context:** Writes detailed PRDs with Given/When/Then acceptance criteria; uses Jira daily; comfortable with CLI tools and automation
- **Quote:** *"I want to be a product manager, not a Jira administrator."*

### Secondary: The PM Team Lead (Early Majority)

- **Name:** David Reeves
- **Role:** Director of Product Management overseeing 6-10 PMs
- **Adoption curve segment:** Early Majority — needs proven ROI before adopting; influenced by team productivity metrics
- **Goals:** Increase team velocity; reduce administrative overhead across the PM org; improve traceability for compliance audits
- **Pain points:** Aggregate team loses 40+ hours/month to ticket admin; no visibility into PRD-to-ticket traceability; compliance risks from stale tickets
- **Behavioral context:** Reviews PRDs and Jira boards; needs reporting on sync status; makes tooling decisions for the team

## User Stories

1. **As a** product manager, **I want to** generate Jira epics and stories directly from an approved PRD **so that** I do not have to manually re-type requirements into Jira fields.
2. **As a** product manager, **I want** the generated Jira stories to include acceptance criteria in Given/When/Then format, proper epic hierarchy, and linked dependencies **so that** engineering teams have complete, actionable tickets from day one.
3. **As a** product manager, **I want to** receive a sync report when my PRD changes after tickets have been created **so that** I can identify and update affected tickets before teams work off stale requirements.
4. **As a** PM team lead, **I want to** view a traceability matrix linking PRD sections to Jira ticket IDs **so that** I can verify coverage and satisfy compliance audit requirements.
5. **As a** product manager, **I want** the tool to work within my existing workflow (CLI or editor) without requiring me to log into a separate application **so that** adoption friction is minimized.

## Functional Requirements

| ID | Requirement | Priority (MoSCoW) | Linked Insight |
|----|-------------|-------------------|----------------|
| FR-01 | Parse PRD Markdown files and extract: title, user stories, acceptance criteria, functional requirements, non-functional requirements, dependencies, and priority levels. | Must Have | insight-2026-03-05-001 |
| FR-02 | Generate Jira epics from PRD top-level sections with title, description, and priority mapped from PRD priority field. | Must Have | insight-2026-03-05-001 |
| FR-03 | Generate Jira stories under the correct epic, with summary, description, acceptance criteria (preserved in Given/When/Then), and story point estimate placeholder. | Must Have | insight-2026-03-05-001 |
| FR-04 | Create dependency links between Jira tickets when the PRD specifies inter-requirement dependencies. | Should Have | insight-2026-03-05-001 |
| FR-05 | Produce a traceability report (Markdown table) mapping each PRD section/requirement to the generated Jira ticket ID. | Must Have | insight-2026-03-05-001 |
| FR-06 | Detect changes between the current PRD version and the version used for the last ticket generation; output a diff report highlighting affected Jira tickets. | Should Have | insight-2026-03-05-001 |
| FR-07 | Support dry-run mode that previews ticket structure without creating tickets in Jira. | Must Have | insight-2026-03-05-001 |
| FR-08 | Allow user to select which PRD sections to include/exclude before generation. | Could Have | insight-2026-03-05-001 |

## Non-Functional Requirements

| ID | Requirement | Target | Rationale |
|----|-------------|--------|-----------|
| NFR-01 | Ticket generation for a PRD with up to 30 acceptance criteria must complete within 60 seconds. | < 60s end-to-end | PMs expect near-instant feedback; anything over 2 minutes breaks flow. |
| NFR-02 | The system must authenticate with Jira Cloud via OAuth 2.0 or API token, storing credentials in the local environment (`.env`), never in generated files. | Zero credential leakage | Security requirement. |
| NFR-03 | The system must handle Jira API rate limits (429 responses) with exponential backoff and retry up to 3 times before failing gracefully with a clear error message. | 3 retries, max 30s backoff | Jira rate limits are common at scale. |
| NFR-04 | All generated Jira tickets must be valid per the target project's issue type schema; the system must validate field compatibility before creation and report mismatches. | Zero invalid ticket creation attempts | Prevents partial failures and orphaned tickets. |
| NFR-05 | The traceability report must be deterministic: the same PRD input must always produce the same report structure (ticket order may vary due to Jira API). | Deterministic output | Enables diffing and version control. |

## Acceptance Criteria

### AC-01: Basic ticket generation from PRD

**Given** a PRD Markdown file with at least one user story and two acceptance criteria in Given/When/Then format, and valid Jira credentials configured in `.env`
**When** the user runs the `/jira create` command targeting that PRD
**Then** the system creates one Jira epic with the PRD title and one story per user story, each story containing the acceptance criteria text in its description field, and returns a traceability report listing each generated ticket ID alongside its source PRD section heading.

### AC-02: Acceptance criteria format preservation

**Given** a PRD containing acceptance criteria written in Given/When/Then format
**When** Jira stories are generated from that PRD
**Then** each story's description field contains the acceptance criteria with Given, When, and Then on separate lines, preserving the exact wording from the PRD without truncation or reformatting.

### AC-03: Dry-run mode

**Given** a valid PRD file and the `--dry-run` flag passed to the `/jira create` command
**When** the command executes
**Then** the system outputs a preview of the ticket hierarchy (epic title, story titles, acceptance criteria counts) to the console without making any Jira API calls, and no tickets are created in Jira.

### AC-04: Sync drift detection

**Given** a PRD that has been previously used to generate Jira tickets (traceability report exists) and the PRD has since been modified (acceptance criteria wording changed in section 3)
**When** the user runs the `/jira sync-check` command targeting that PRD
**Then** the system outputs a report listing each changed PRD section, the specific change detected (old text vs. new text), and the Jira ticket ID(s) affected, with a status of "out-of-sync" for each affected ticket.

### AC-05: Error handling for invalid Jira project

**Given** a valid PRD file and Jira credentials configured for a project key that does not exist in the target Jira instance
**When** the user runs the `/jira create` command
**Then** the system returns an error message within 5 seconds stating "Jira project [KEY] not found. Verify the project key in your configuration." and does not create any tickets or partial artifacts.

### AC-06: Rate limit resilience

**Given** a PRD with 20 user stories requiring 20+ Jira API calls, and the Jira API returns HTTP 429 (rate limited) on the 5th call
**When** the system encounters the rate limit response
**Then** the system waits with exponential backoff (initial delay 2 seconds, maximum 30 seconds), retries up to 3 times, and if successful, completes all ticket creation and reports the total elapsed time; if all retries fail, the system reports which tickets were created and which remain, enabling the user to resume.

### AC-07: Dependency linking

**Given** a PRD where User Story 3 specifies a dependency on User Story 1 (e.g., "Depends on: US-01")
**When** Jira tickets are generated
**Then** the Jira story for US-03 has a "is blocked by" link to the Jira story for US-01, and the traceability report reflects this dependency relationship.

## Success Metrics (HEART Framework)

| HEART Dimension | Goal | Signal | Metric | Target (3 months post-launch) |
|-----------------|------|--------|--------|-------------------------------|
| **Happiness** | PMs feel the tool saves meaningful time | Post-generation satisfaction survey (1-5 scale) | Average satisfaction score | >= 4.2 / 5.0 |
| **Engagement** | PMs use the tool for every new PRD | Generation commands executed per PM per month | Monthly active usage rate | >= 80% of PRDs processed through tool |
| **Adoption** | All PMs on a team adopt within 4 weeks of one PM starting | Number of unique PMs using the tool / total PMs on team | Team adoption rate | >= 70% team adoption within 4 weeks |
| **Retention** | PMs continue using the tool after the first month | PMs who used the tool in month 1 and month 2 | Month-over-month retention rate | >= 90% retention |
| **Task Success** | Tickets are generated correctly without manual edits | Percentage of generated tickets that require no manual field edits before sprint planning | First-pass accuracy rate | >= 85% of tickets need zero edits |

**Time-to-first-value:** A new user should generate their first set of Jira tickets from an existing PRD within 10 minutes of installation, including credential setup.

## MVP Scope (Goldilocks Principle)

### Too Small (insufficient to validate hypothesis)
- Only generates epic titles from PRD headings, no story details or acceptance criteria.
- Reason for exclusion: Does not reduce meaningful work; PMs still re-type the hard parts.

### Just Right (MVP)
- Parse PRD structure (FR-01)
- Generate epics and stories with acceptance criteria (FR-02, FR-03)
- Traceability report (FR-05)
- Dry-run mode (FR-07)
- Reason: Validates the core hypothesis (75% time reduction) with the minimum feature set that delivers end-to-end value. PMs can generate complete tickets and verify correctness before committing.

### Too Large (defer to v2)
- Bidirectional sync with automatic ticket updates (FR-06 partial)
- Selective section inclusion (FR-08)
- Dependency linking (FR-04)
- Reason for deferral: Sync and dependency features add complexity that could delay launch without being required to validate the core time-saving hypothesis.

## Adoption Strategy

### Phase 1: Innovators (Weeks 1-2)
- Recruit 3 PMs who have expressed frustration with Jira ticket creation (e.g., Sarah Chen archetype)
- Provide 1:1 onboarding walkthrough (15 minutes)
- Collect feedback after first 5 uses via structured interview

### Phase 2: Early Adopters (Weeks 3-6)
- Publish internal case study with time-saved metrics from Phase 1
- Create a 3-minute video tutorial demonstrating end-to-end flow
- Enable team leads to view traceability reports (addresses compliance motivation)

### Phase 3: Early Majority (Weeks 7-12)
- Integrate into PM team onboarding checklist
- Add sync-check command (v2) to address drift concerns surfaced in Phase 1-2 feedback
- Target: 70% team adoption

### Churn risks and mitigation
- **Risk:** Generated tickets require too many manual edits, making the tool feel like extra work. **Mitigation:** Target 85% first-pass accuracy; iterate on parsing logic weekly during Phase 1 based on edit patterns.
- **Risk:** PMs with non-standard PRD formats cannot use the tool. **Mitigation:** Provide a PRD template and a format validation command that reports parsing issues before generation.

## Risks and Dependencies

| Risk | Likelihood | Impact | Mitigation | Contingency |
|------|-----------|--------|------------|-------------|
| Jira API schema changes break ticket creation | Medium | High | Pin to Jira REST API v3; run integration tests weekly against a sandbox project | Maintain a compatibility layer that maps field names; alert on test failures |
| PRD format variability causes parsing failures | High | Medium | Define a canonical PRD template; validate format before generation; report specific parsing errors with line numbers | Allow manual section tagging as fallback |
| Rate limiting causes partial ticket creation | Medium | Medium | Implement exponential backoff (NFR-03); track creation progress for resume capability | Provide a `--resume` flag that reads the partial traceability report and creates only missing tickets |
| Credential leakage via generated artifacts | Low | Critical | Never write credentials to output files (NFR-02); scan generated Markdown for API token patterns in CI | Immediate token rotation playbook documented in runbook |

### Dependencies
- Jira Cloud instance with REST API v3 enabled and a service account with project-level create permissions
- Python 3.11+ with FastMCP, httpx, and PyYAML
- `.env` file with `JIRA_BASE_URL`, `JIRA_API_TOKEN`, `JIRA_USER_EMAIL`, `JIRA_PROJECT_KEY`

## Out of Scope

- **Confluence integration** — PRDs are Markdown files in the local repository, not Confluence pages. Confluence support is a separate initiative.
- **Automatic ticket updates on PRD change** — MVP detects drift but does not auto-update tickets. Auto-update is planned for v2 after validating that drift detection alone is valuable.
- **Sprint planning or story point estimation** — The tool generates tickets but does not assign them to sprints or estimate effort. These are team-specific decisions.
- **Support for project management tools other than Jira** — Linear, Asana, and Shortcut support may be explored post-v2 based on demand.
- **PRD authoring or editing** — This tool consumes PRDs; it does not help write them. PRD generation is handled by the `/prd` command.
