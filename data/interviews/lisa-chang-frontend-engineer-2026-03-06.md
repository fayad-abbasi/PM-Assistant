---
id: interview-2026-03-06-001
title: "1:1 — Lisa Chang, Frontend Engineer, Growth Team"
date: 2026-03-06
interviewee: Lisa Chang
role: Senior Frontend Engineer
company: Internal — Growth Team
tags: [documentation, frontend-engineer, cognitive-load, discoverability]
status: analyzed
created_at: 2026-03-06T14:00:00Z
---

# 1:1 — Lisa Chang, Senior Frontend Engineer, Growth Team

**Date:** 2026-03-06
**Interviewer:** DevEx PM (onboarding conversations)
**Duration:** 35 minutes
**Format:** Video call

---

**DevEx PM:** Lisa, thanks for meeting. I'm ramping up on the DevEx team and want to understand what's working and what's not for frontend engineers. What's top of mind?

**Lisa Chang:** The shared component library. Or rather, the three shared component libraries. We have the original one from 2022, the "v2" that someone started migrating to but never finished, and a third one that the Design Systems team is building now. Nobody knows which components to use. "I asked in Slack which button component to use and got four different answers from four different engineers. That's not a component library, that's a choose-your-own-adventure book."

**DevEx PM:** How does that affect your day-to-day work?

**Lisa Chang:** Every new feature starts with 30 minutes of archaeology. Which components exist? Which ones are deprecated? Does this one support the new design tokens? I end up reading source code in three different repos just to figure out if I can use an existing dropdown or if I need to build one. And then code review turns into a debate about which library I should have used. "I spend more time figuring out what already exists than building the thing I need. That's backwards."

**DevEx PM:** What about documentation?

**Lisa Chang:** That's the core issue, honestly. Docs are scattered across Confluence, README files, Storybook (which is out of date), and tribal knowledge in Slack threads. The Confluence docs were last updated eight months ago. The Storybook instance builds but half the stories are broken because the props changed. "Our documentation is a museum of how things used to work. It's technically still there, but nothing in it reflects reality."

**DevEx PM:** How do new frontend engineers handle this?

**Lisa Chang:** They shadow someone for a week and build up a mental map. That's literally our onboarding strategy — "sit with Lisa and she'll show you." I've onboarded four engineers this year, and each time I lose a week of my own productivity. Not because I mind helping, but because the knowledge shouldn't be in my head — it should be in a system. "I'm a single point of failure for frontend institutional knowledge on my team. If I go on vacation, people wait until I get back to ask questions. That's not sustainable."

**DevEx PM:** What would make the biggest difference?

**Lisa Chang:** One source of truth for the component library. Kill the old ones, finish the migration, and have a living Storybook that's tested in CI so it can't go stale. And I want a search tool — I should be able to type "date picker" and find the canonical component, its props, usage examples, and which design token set it uses. "Don't give me more docs. Give me one doc that's actually correct and findable."

**DevEx PM:** Any thoughts on the broader developer experience?

**Lisa Chang:** The internal developer portal — if you can call it that — is a Confluence space with 200 pages and no navigation structure. There's a page called "Getting Started" that references tools we stopped using two years ago. New engineers don't trust any of the docs because they've been burned by following outdated instructions. "The worst documentation is documentation that's wrong but looks authoritative. At least if there's no doc, you know to ask someone."
