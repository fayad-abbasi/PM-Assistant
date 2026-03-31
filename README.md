# PM Assistant

> A complete AI-native PM workflow system built inside Claude Code — no web app, no API server, no database. Every artifact lives as a file. Every workflow runs as a slash command.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Native-CC785C?style=flat)](https://claude.ai/code)
[![Python](https://img.shields.io/badge/MCP%20Servers-Python%20%2B%20FastMCP-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](LICENSE)

---

## What It Is

Most "AI for PMs" tools bolt an LLM onto a web form. This is different.

PM Assistant runs **entirely inside Claude Code** using its native primitives — slash commands, hooks, subagents, and MCP server integrations. There's no app to open, no UI to navigate. You work in natural language inside your terminal, and the system manages the full PM artifact lifecycle: discovery → strategy → execution → retrospective.

Everything is a file. Everything is git-versioned. Everything is linked.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code Session                      │
│                                                                 │
│  /slash-command ──► Prompt Template ──► Subagent (generation)   │
│                            │                    │               │
│                     background_information/   data/             │
│                     (PM frameworks, books,    (artifacts:       │
│                      course summaries)         PRDs, insights,  │
│                                                interviews, OKRs │
│  Hooks:                                        roadmap, GTM...  │
│  • Session-start → inject context             all as .md/.json) │
│  • On-write → auto quality-gate               git-versioned     │
│                                                                 │
│  MCP Servers: Jira · Slack · Figma · Miro · Lucid               │
└─────────────────────────────────────────────────────────────────┘
```

### Core Design Principles

**File-native** — Every artifact is a Markdown or JSON file in `data/`. No database, no hidden state. You can read, edit, grep, or diff anything.

**Evidence-traced** — Every PRD links to insights. Every insight links to interviews. Every OKR links to evidence. The chain is fully auditable.

**Quality-gated** — Generated artifacts are auto-scored against rubrics before being presented. Below-threshold outputs are fixed automatically.

**Git-versioned** — All work lives in version control. Diffs show exactly what changed and when.

**Continuously improvable** — Drop new PM frameworks or books into `background_information/`, run `/ingest`, and the system evaluates and integrates them into the workflow.

---

## Slash Commands

The full PM lifecycle, one command at a time:

### Discovery
| Command | What it does |
|---|---|
| `/discover` | Manage interviews, run analysis, import analytics |
| `/quick-insight` | Paste a quote or observation → tagged insight in one step |

### Strategy
| Command | What it does |
|---|---|
| `/strategy` | Vision, OKRs, roadmap, competitive analysis |
| `/ost` | Opportunity Solution Trees — outcome → opportunities → solutions → assumption tests → decision |

### Execution
| Command | What it does |
|---|---|
| `/prd` | Create, generate, edit, and convert PRDs |
| `/gtm` | Audience-specific messaging from PRDs (developer, EM, exec, compliance, finance) |
| `/ux` | Journey maps and design references |
| `/uat` | Test case generation, execution tracking, reports |
| `/jira` | Create Jira tickets from PRDs via MCP |

### Measurement
| Command | What it does |
|---|---|
| `/outcomes` | Post-launch metrics and impact reports |
| `/retro` | Retrospectives with strategy feedback loops |

### Stakeholder Management
| Command | What it does |
|---|---|
| `/status` | Stakeholder reports, decision logs, meeting notes |
| `/weekly` | End-of-week status report + dashboard in one shot |

### System
| Command | What it does |
|---|---|
| `/pm-dash` | Overview dashboard with data quality flags |
| `/search` | Cross-artifact search by tags, links, or content |
| `/eval` | Score any artifact against its quality rubric |
| `/quality-check` | Structural + content validation across `data/` |
| `/link-check` | Verify all cross-links and tag validity |
| `/next` | Prioritized recommendations for what to work on next |
| `/ingest` | Evaluate and integrate new PM frameworks into the workflow |
| `/grill-me` | Stress-test a plan — confrontational, one question at a time |
| `/refresh` | Re-inject session context mid-session |

---

## Full Lifecycle Example

```bash
# Discovery
/discover              # Add + analyze interviews with engineers
/discover batch        # Surface cross-cutting patterns

# Strategy
/ost                   # Map outcome → opportunities → solutions → tests
/discover test-assumption  # Run assumption tests
/ost resume            # Review results, pick winning solution

# Execution
/prd                   # Generate PRD from OST (pre-populated with evidence)
/strategy okrs         # Define outcome-focused OKRs linked to PRD
/strategy roadmap      # Add roadmap items linked to OKRs
/gtm internal          # Draft internal messaging for 4 engineering audiences
/uat                   # Generate test cases from acceptance criteria

# Measurement
/outcomes              # Track post-launch metrics against OKR targets
/retro                 # Retrospective → learnings → strategy feedback loop
```

---

## Data Model

All artifacts use YAML frontmatter with consistent ID patterns (`{type}-{YYYY-MM-DD}-{NNN}`), status enums, and cross-reference fields. The full chain:

```
Interview → Insight → OST → PRD → GTM Draft
                       │     │
                      OKR  Roadmap Item
                             │
                          Test Cases → Outcomes → Retrospective
```

Every link is validated by `/link-check`. Every artifact is scoreable by `/eval`.

---

## MCP Integrations

External tools connect via Python + FastMCP servers, run with `uv`:

| Server | Purpose |
|---|---|
| Jira | Epic, story, and task CRUD + transitions |
| Slack | Search messages, post updates, read threads |
| Figma | Design file access, asset export, comments |
| Miro | Affinity maps, visual journey maps |
| Lucid | Flowcharts and architecture diagrams |

---

## Setup

### Prerequisites
- [Claude Code](https://claude.ai/code) (this system is built for it natively)
- Python 3.11+ and `uv` (for MCP servers)

### Install

```bash
git clone https://github.com/fayad-abbasi/PM-Assistant.git
cd PM-Assistant
cp .env.example .env
# Add API keys for any MCP integrations you want active
```

### Configure MCP Servers

Edit `.claude/settings.json` to enable the integrations relevant to your stack. Each MCP server in `mcp-servers/` has its own setup instructions.

### Add Your Background Material

Drop PM books, course summaries, and framework references into `background_information/` (local-only, not tracked in git), then run:

```bash
/ingest scan    # Detect new material
/ingest review  # Evaluate what's worth integrating
/ingest apply   # Apply recommendations to prompts and rubrics
```

---

## Why I Built This

As a DevEx PM, I think a lot about cognitive load — the friction between having a thought and acting on it. Most PM tools add friction: open a tab, navigate a UI, remember a schema, copy-paste between tools.

This system removes that friction entirely. The interface is natural language. The storage is files you already understand. The workflow is your workflow, not the tool's workflow.

It's also a direct application of the Claude Code primitives I work with professionally — commands, hooks, subagents, MCP servers. Building your own tooling is the best way to understand it deeply enough to make product decisions about it.

---

## Roadmap

- [ ] End-to-end `/verify` command — validates the full artifact chain from interview to outcome
- [ ] Workflow analytics in `/pm-dash` — eval score trends, PRD cycle time, assumption test velocity
- [ ] DevEx-specific template library — platform migration PRDs, golden path proposals, deprecation plans
- [ ] Multi-product scoping — filter all commands and dashboards by product area

---

## Related Projects

- [codeguard-ai](https://github.com/fayad-abbasi/codeguard-ai) — AI-powered PR review bot using Claude + GitHub webhooks
- [ai-podcast-generator](https://github.com/fayad-abbasi/ai-podcast-generator) — Automated AI news podcast pipeline, $0.08/episode

---

## License

MIT

---

<div align="center">
  <sub>Built by <a href="https://linkedin.com/in/fayad-abbasi">Fayad Abbasi</a> · DevEx PM · Claude Code native architecture</sub>
</div>
