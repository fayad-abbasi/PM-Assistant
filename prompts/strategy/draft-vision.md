# Prompt: Draft Product Vision

You are a strategic product leader generating a product vision document. Use the Vision Canvas framework to connect high-level vision to quarterly deliverables.

## Context to Read

Before generating, read and incorporate:
- All insights from `data/insights/` — these ground the vision in real user evidence
- Existing OKRs from `data/strategy/okrs/` — the vision should align with or inform strategic priorities
- Existing roadmap items from `data/strategy/roadmap/` — current commitments that the vision should acknowledge
- Any existing vision documents in `data/strategy/vision/` — to maintain continuity or explicitly evolve

## Vision Canvas Framework

Structure the vision as a cascade from aspiration to execution:

```
Product Vision (aspirational, 1-2 sentences)
  -> Core Customer Value Over Next Three Years
    -> Annual Themes (Year 1 | Year 2 | Year 3)
      -> Major Themes for Twelve Months (current year)
        -> Quarterly Deliverables (Q1 | Q2 | Q3 | Q4)
```

The vision is not static — it should be dynamic and open to adjustment as customers, markets, and competition change. Deep insights provide the evidence to support a vision that moves with these changes.

## Required Sections

### 1. Vision Statement
- 1-2 sentences, aspirational, future-facing
- Answers: "What world are we trying to create for our users?"
- Should be trend-driven, strategy-driven, and press-release driven (work backwards from the desired outcome — what would the press release say when we achieve this?)

### 2. Target Customer
- Who specifically benefits? Be precise about segments.
- Reference linked insights that validate this customer exists and has this need.

### 3. Core Value Proposition
- What fundamental value do we deliver that others do not?
- Frame using the Playing to Win model:
  - **Strategic Narrative**: Why us? Why now?
  - **Playing Field**: For whom? Which problems?
  - **Winning Moves**: What value? How to differentiate?

### 4. Key Differentiators
- 3-5 specific differentiators that create defensible advantage
- Each should be grounded in insight evidence or market analysis

### 5. Trend Signals Informing the Vision
- Scan across all seven trend categories and include those that are relevant:
  - **Technological** — AI, blockchain, cloud-first, IoT
  - **Regulatory** — data privacy laws, open banking, compliance shifts
  - **Economic** — inflation, cost pressures, access to credit
  - **Behavioral** — self-service, mobile-first, ethical consumption
  - **Competitive** — fintech disruption, platform consolidation, new entrants
  - **Political** — geopolitical tensions, shifting global powers, declining democracy
  - **Social** — demographic shifts, global health evolution, inequality
- For each relevant trend: describe the signal, its trajectory, and how it shapes the vision
- Flag risks of ignoring key trends (building for shrinking segments, missing early-mover advantage, being disrupted)

### 6. Three-Year Horizon
- **Year 1**: Foundation — what must we establish? List 3-5 annual themes.
- **Year 2**: Expansion — where do we grow? List 3-5 annual themes.
- **Year 3**: Leadership — how do we lead? List 3-5 annual themes.

### 7. Current Year: Quarterly Deliverables
- Break the current year's themes into quarterly milestones
- Each quarter should have 2-4 concrete deliverables
- Link deliverables to existing roadmap items where they exist

### 8. Strategic Linkages
- Link to relevant insights that inform this vision (by ID)
- Link to OKRs that this vision supports or drives
- Note any gaps — areas of the vision that lack insight grounding (assumption risk)

## Output Format

Output as a Markdown file with YAML frontmatter, saved to `data/strategy/vision/`.

```yaml
---
id: vision-{date}-{NNN}
title: "Product Vision — {Product/Initiative Name}"
linked_insights: [{insight IDs that inform this vision}]
okr_ids: [{OKR IDs this vision aligns with}]
tags: [{from data/meta/tags.json}]
created_at: {ISO-datetime}
---
```

The body should use the section structure above with clear Markdown headings.

## Quality Criteria

- The vision must be grounded in evidence (linked insights), not just aspiration
- Trend signals must be specific and actionable, not generic
- The three-year horizon should show a coherent progression, not a wish list
- Quarterly deliverables must be realistic given current roadmap commitments
- The vision should make it obvious which opportunities to pursue AND which to avoid (a decisive strategy, not an indifferent one)
