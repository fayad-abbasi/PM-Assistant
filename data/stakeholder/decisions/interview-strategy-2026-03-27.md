---
id: decision-2026-03-27-001
title: "First 3 Weeks Interview & Discovery Strategy"
decision: "Structured interview approach with visual workflow mapping before global tech summit in week 3"
participants:
  - "DevEx PM"
linked_prds: []
tags:
  - developer-onboarding
  - discovery
  - workflow
created_at: 2026-03-27T16:00:00Z
---

# First 3 Weeks Interview & Discovery Strategy

## Context

Starting as DevEx PM with ~8 dev teams (likely split across frontend/backend, Java/Python, dev/QA — exact structure TBD). Global tech summit with 300+ developers happens in week 3. Need to build enough context before the summit to have informed conversations, then use the summit as a high-volume data collection event.

## Decision

### Interview Structure — Three Layers

1. **Senior IC** — gives the real workflow (what actually happens day-to-day)
2. **New IC** — reveals onboarding and documentation gaps (hasn't normalized the workarounds yet)
3. **Tech Lead / EM** — validates findings and provides cross-team patterns

Not all three layers for every team — prioritize depth based on what's learned and what's urgent.

### Wave Approach

**Pre-summit (Weeks 1-2):** 4-5 senior IC interviews across the most central teams. Goal is building a draft workflow map with enough context to ask smart questions at the summit.

**Summit (Week 3):** High-volume, informal data collection — coffee chats, hallway conversations, sessions. Target: 30-40 touchpoints across three days.

**Post-summit (Week 4+):** Go deep on 2-3 teams where the most interesting friction, complexity, or divergence appeared. Add new IC and tech lead/EM interviews for these teams.

### Visual Artifact — Workflow Maps

- One Miro or Lucid board per team (tool depends on firm's supported stack)
- Journey-style flow: code submit from IDE → production deployment
- Reusable template built before the first interview:
  - **Stages**: code → commit → build → test → review → merge → deploy → monitor
  - **Swim lanes**: tooling, time, pain points, workarounds
- Same format for every team — enables side-by-side comparison to spot convergence and divergence

### Interview Format

- **First 10-15 minutes**: Open and relational — background, what they're working on, what they care about. Build trust.
- **Second half**: Transition to live board-building together — "can I map this out with you?" Collaborative, not extractive. Interviewee sees and corrects the output in real time.

## Still Open

- Which 4-5 teams to prioritize for pre-summit (depends on day-1 context about org structure and urgency)
- Miro vs. Lucid (depends on firm's tool stack)
- Summit strategy details (format unknown until after joining)
- Specific interview questions for the open first half and the mapping session
- How the workflow maps feed into DevEx strategy and OKR planning

## Rationale

- Building visual maps enables pattern recognition across teams that notes alone don't provide
- The summit is a force multiplier — arriving with context makes every conversation more valuable
- Three-layer interview structure captures reality (senior IC), fresh perspective (new IC), and systemic view (tech lead/EM)
- Live mapping during interviews builds trust AND produces tangible output — the collaboration is the relationship-building
