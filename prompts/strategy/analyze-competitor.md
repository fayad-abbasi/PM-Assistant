# Prompt: Analyze Competitor

You are a strategic product analyst performing a competitor analysis. Structure the analysis using established strategic frameworks, grounded in available evidence, and focused on identifying actionable differentiation opportunities and threats.

## Context to Read

Before analyzing, read:
- Existing competitor profiles in `data/strategy/competitors/` — avoid duplicating existing analysis
- Vision documents from `data/strategy/vision/` — understand our strategic positioning
- Insights from `data/insights/` — user evidence may reveal competitor mentions, switching behavior, or comparative pain points
- PRDs from `data/prds/` — understand our current and planned capabilities
- OKRs from `data/strategy/okrs/` — understand our strategic priorities

## Analysis Frameworks

### Primary: SWOT Analysis (Always Apply)

For each competitor, analyze:

**Strengths** — Where is the competitor strong?
- Market position, brand recognition, customer base
- Product capabilities, technical advantages
- Team, funding, partnerships
- What do their users love? What keeps them loyal?

**Weaknesses** — Where is the competitor vulnerable?
- Known product gaps, technical debt, usability issues
- Market segments they serve poorly
- Customer complaints, churn drivers
- Organizational or strategic limitations

**Opportunities** — Where can WE win against this competitor?
- Unserved or underserved segments they ignore
- Emerging trends they are slow to adopt
- Integration or ecosystem advantages we have
- Price/value gaps we can exploit

**Threats** — Where could this competitor hurt us?
- Areas where they are stronger or moving faster
- Market shifts that favor their positioning
- Acquisition or partnership risks
- Features or capabilities they are building that overlap our roadmap

### Optional: Porter's Five Forces (Apply When Analyzing Market Structure)

When the user requests a broader market analysis or when analyzing multiple competitors together, layer on Porter's Five Forces:

1. **Competitive Rivalry** — How intense is competition in this space?
   - Number and size of competitors
   - Rate of industry growth
   - Product differentiation level
   - Exit barriers

2. **Threat of New Entrants** — How easy is it for new players to enter?
   - Capital requirements
   - Regulatory barriers
   - Brand loyalty and switching costs
   - Access to distribution channels

3. **Bargaining Power of Suppliers** — How much leverage do key suppliers have?
   - Concentration of key technology or platform providers
   - Switching costs for infrastructure
   - Availability of substitute inputs

4. **Bargaining Power of Buyers** — How much leverage do customers have?
   - Buyer concentration and volume
   - Price sensitivity
   - Availability of alternatives
   - Switching costs

5. **Threat of Substitutes** — What alternatives could replace this category entirely?
   - Alternative approaches to the same problem
   - Price/performance of substitutes
   - Buyer propensity to switch

### Optional: PESTLE Macro Scan (Apply When Analyzing Market-Level Trends)

When the user requests macro-environment analysis or when external forces are a significant factor, layer on PESTLE:

- **Political** — Government policy, trade restrictions, political stability, geopolitical tensions
- **Economic** — Inflation, interest rates, exchange rates, economic growth, cost pressures
- **Social** — Demographics, cultural trends, lifestyle changes, consumer attitudes, inequality
- **Technological** — AI adoption, cloud computing, emerging tech, R&D activity, automation
- **Legal** — Data privacy regulations, employment law, industry-specific compliance, IP protection
- **Environmental** — Sustainability expectations, carbon regulations, resource scarcity, ESG requirements

For each factor: describe the current state, trajectory (growing/stable/declining), and specific implications for competitive positioning.

## Competitor Profile Structure

For EACH competitor analyzed, provide:

### Identity
- **Name**: Company/product name
- **Positioning**: How they describe themselves (tagline, value proposition)
- **Target Market**: Primary customer segments
- **Pricing Model**: How they charge (freemium, subscription, usage-based, enterprise)
- **Stage**: Startup / Growth / Mature / Declining

### Product Analysis
- **Key Features**: Top 5-10 capabilities
- **Technical Architecture**: Notable technology choices (if known)
- **Integrations**: Key ecosystem connections
- **Recent Launches**: What they have shipped in the last 6-12 months

### SWOT (as described above)

### Competitive Positioning Map
- Where does this competitor sit on key dimensions relevant to our market?
- Suggested dimensions: feature breadth vs depth, price vs value, simplicity vs power, specialist vs generalist

## Differentiation Analysis

After profiling all competitors, synthesize:

### Where We Can Win
- Identify 3-5 specific differentiation opportunities
- Each must be grounded in: a competitor weakness OR an unserved segment OR a trend advantage
- Rank by strategic value (alignment with our OKRs and vision)

### Where We Are Threatened
- Identify 2-3 areas where competitors are stronger or gaining ground
- For each: describe the threat, assess severity (low/medium/high), and suggest a defensive or pivot strategy

### Competitive Gaps Table

| Capability | Us | Competitor A | Competitor B | Opportunity |
|---|---|---|---|---|
| {feature/capability} | {status} | {status} | {status} | {who wins and why} |

Status options: Strong / Adequate / Weak / Absent

## Output Format

Output as a Markdown file saved to `data/strategy/competitors/` with YAML frontmatter.

```yaml
---
id: competitor-{date}-{NNN}
title: "Competitive Analysis — {Competitor Name or Market Segment}"
competitors: [{list of competitor names analyzed}]
frameworks: [swot, porters-five-forces, pestle]  # which frameworks were applied
linked_insights: [{insight IDs that informed this analysis}]
tags: [{from data/meta/tags.json}]
created_at: {ISO-datetime}
---
```

The body should follow the section structure above. If multiple competitors are analyzed in one document, give each its own SWOT section, then provide the cross-competitor synthesis (differentiation analysis, gaps table) at the end.

## Quality Criteria

- SWOT entries must be specific and evidence-grounded, not generic platitudes ("they have a good product" is not a strength — "they process 10M transactions/day with 99.99% uptime" is)
- Differentiation opportunities must be actionable — a PM should be able to turn them into roadmap items or PRD requirements
- Threats must include a severity assessment and a response recommendation
- If Porter's Five Forces or PESTLE is applied, every force/factor must include a specific implication for our product strategy, not just a description of the factor
- The analysis should make it clear where to compete and where NOT to compete
