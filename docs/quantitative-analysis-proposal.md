# Quantitative Analysis Capability — Proposal (Placeholder)

## Problem

The PM Assistant is heavily qualitative — interviews, insights, narratives. But PM work regularly requires reasoning about quantitative data: platform metrics, survey results, cost models, capacity planning, adoption curves. Without structured support for this, the PM must do quantitative analysis entirely outside the workflow.

## Why This Is a Placeholder

The right approach depends on **what tooling is available in the actual role**:

- If there's an analytics platform with an **MCP server** (or one can be built), we can pull data directly into the workflow
- If data lives in **spreadsheets/CSVs**, we need a different ingestion pattern
- If there's a **BI tool** (Looker, Tableau, Grafana), we may just need to reference dashboards rather than analyze raw data

Until the tooling landscape is clear, this document captures **what we need** without committing to **how we build it**.

---

## What We Need

### 1. Metric Tracking & Interpretation

**The gap**: No structured way to ingest, store, or reason about platform metrics over time.

**Examples of metrics a DevEx PM tracks**:
- Platform NPS (e.g., 32 current → 50+ target)
- CI/CD pipeline times (e.g., 38 min median)
- New hire onboarding time (e.g., 2.8 days → target <1 day)
- PR review cycle time (e.g., 18 hours median)
- Tool adoption rates (e.g., design system at 40%)
- Security incident frequency and cost
- Infrastructure cost trends

**What the solution should do**:
- Store periodic metric snapshots (manually entered or pulled via MCP)
- Show trends (improving, flat, degrading)
- Flag metrics that crossed a threshold (good or bad)
- Connect metrics to OKRs — "this metric maps to KR-2 of our Q1 objective"

### 2. Survey / Feedback Data Analysis

**The gap**: Developer surveys produce structured quantitative data (ratings, rankings, categorized feedback). The PM Assistant can analyze interview transcripts but has no support for structured survey data.

**What the solution should do**:
- Ingest survey results (CSV, JSON, or manual entry)
- Categorize and theme open-text responses (similar to `/discover` batch analysis)
- Surface top pain points with frequency counts
- Compare across survey waves (Q1 vs Q2)
- Link findings to insights and PRDs

### 3. Capacity Planning

**The gap**: Roadmap prioritization requires matching work against available capacity (engineer-weeks, team constraints, hiring ramps). Currently this is done ad hoc.

**What the solution should do**:
- Model team capacity (headcount × availability × allocation)
- Map backlog items to effort estimates
- Flag over-commitment (more work than capacity)
- Account for known constraints (people leaving, ramp-up time for new hires)
- Support "what if" scenarios (what if we get 2 more engineers in Q2?)

### 4. Cost Modeling

**The gap**: Build-vs-buy decisions, infrastructure planning, and vendor negotiations all require cost analysis. No structured support exists.

**What the solution should do**:
- TCO modeling (Year 1, Year 3 — licensing + implementation + maintenance + hidden costs)
- ROI calculations (time saved × hourly rate × headcount)
- Cost comparison across options
- Sensitivity analysis (what if headcount grows 50%? What if vendor raises prices?)

---

## Possible Implementation Paths

### Path A: MCP Integration (Preferred if available)

If the organization has analytics/BI tooling with API access:

| Tool | MCP Approach |
|------|-------------|
| **Grafana** | MCP server to query dashboards and pull metric snapshots |
| **Looker / Tableau** | MCP server to pull report data |
| **Google Sheets** | MCP server to read/write spreadsheet data |
| **Datadog / New Relic** | MCP server to pull observability metrics |
| **Internal metrics API** | Custom MCP server wrapping the API |

This would add a new MCP server (e.g., `mcp-servers/analytics-server/`) and a `/metrics` or `/analyze` command.

### Path B: CSV/Manual Ingestion

If no API access is available:

- New `data/analytics/` directory stores metric snapshots as JSON files
- `/analyze import` accepts CSV or manual key-value entry
- Periodic snapshots captured via `/analyze snapshot` (manual entry with guided prompts)
- Trend analysis compares snapshots over time

### Path C: Hybrid

- Some metrics pulled via MCP, others entered manually
- All stored in a common format in `data/analytics/`
- Analysis commands work the same regardless of data source

---

## Integration with Existing Commands

| Command | Integration |
|---------|-------------|
| `/strategy` | Pull current metrics when suggesting OKRs; validate key results against baseline data |
| `/simulate` | Feed capacity and cost data into scenario analysis; `/simulate` Build vs Buy uses TCO data |
| `/outcomes` | Compare actual metrics against expected; auto-populate delta from metric snapshots |
| `/pm-dash` | Show metric trends and threshold alerts |
| `/prd` | Include baseline metrics as context when generating PRDs |
| `/next` | Flag metrics trending in the wrong direction as action items |

---

## Decision Points (To Resolve Once In-Role)

1. **What analytics tooling exists?** (Grafana, Looker, internal dashboards, spreadsheets?)
2. **Is there API access?** (determines MCP vs manual path)
3. **What's the primary data format?** (JSON, CSV, API responses?)
4. **Who owns the data?** (Can we pull it, or does someone need to export it for us?)
5. **What's the refresh cadence?** (Real-time, daily, weekly, quarterly?)
6. **Are there existing dashboards we should reference rather than replicate?**

---

## Minimum Viable Version

Even without tooling clarity, we could start with:

1. A `data/analytics/` directory with a simple JSON schema for metric snapshots
2. Manual entry via a `/metrics capture` command
3. Trend comparison across snapshots
4. Linkage to OKRs and PRDs

This gives us a place to store and reason about numbers without committing to a specific data pipeline. The MCP integration layer can be added later once the tooling landscape is clear.

---

## Files That Would Be Created (MVP)

| File | Purpose |
|------|---------|
| `.claude/commands/metrics.md` | Command for metric capture, trends, analysis |
| `prompts/strategy/analyze-metrics.md` | Prompt for metric interpretation |
| `data/analytics/snapshots/.gitkeep` | Periodic metric snapshots |
| `data/analytics/surveys/.gitkeep` | Survey result storage |

## Files That Would Be Modified

| File | Change |
|------|--------|
| `data/meta/counters.json` | Add `"metric-snapshot": 0`, `"survey": 0` |
| `data/meta/tags.json` | Add `"metrics"`, `"survey"`, `"capacity-planning"` |
| `CLAUDE.md` | Add command, schema |
| `PM_ASSISTANT_CLAUDE_NATIVE.md` | Add to command docs + inventory |
