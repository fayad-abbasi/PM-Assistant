# PM Assistant — Gemini CLI Migration Feasibility

## Summary

The PM Assistant can be ported to Gemini CLI without an architectural rebuild. Gemini CLI has near feature-parity with Claude Code on every primitive the PM Assistant depends on: slash commands, subagents, hooks, MCP servers, project instructions, and file tools. The effort is a **format migration**, not a redesign.

The primary risk is not the tooling — it's whether the underlying model (Gemini) handles multi-step orchestration, long-context reasoning, and structured document generation at the same quality level as Claude. This should be validated early with a representative command (e.g., `/prd`) before committing to a full migration.

---

## Primitive-by-Primitive Migration Map

### 1. Slash Commands (22 commands)

| Claude Code | Gemini CLI |
|---|---|
| `.claude/commands/*.md` (Markdown) | `.gemini/commands/*.toml` (TOML) |

**What changes**: File format. Each command's prompt content stays the same but wraps in TOML syntax.

**Claude Code format**:
```markdown
---
name: grill-me
description: Interview the user relentlessly about a plan or design.
---

Interview me relentlessly about every aspect of this plan...
```

**Gemini CLI equivalent**:
```toml
description = "Interview the user relentlessly about a plan or design."

prompt = """
Interview me relentlessly about every aspect of this plan...
"""
```

**Notes**:
- Gemini supports `{{args}}` template variable for argument injection — equivalent to how Claude Code commands receive arguments
- Gemini supports `@{path}` for file content injection and `!{command}` for dynamic shell execution within prompts — may simplify some commands that currently ask subagents to read files
- Subdirectories become namespaced (e.g., `.gemini/commands/pm/prd.toml` → `/pm:prd`), which could be useful for organizing the 22 commands
- Reload with `/commands reload` — no restart needed

**Effort**: Low. Mechanical format conversion. The prompt content (the hard part) is already written.

**Commands to convert**:
`discover`, `eval`, `grill-me`, `gtm`, `ingest`, `jira`, `link-check`, `next`, `ost`, `outcomes`, `pm-dash`, `prd`, `quality-check`, `quick-insight`, `refresh`, `retro`, `search`, `simulate`, `status`, `strategy`, `uat`, `ux`, `weekly`

---

### 2. Subagents

| Claude Code | Gemini CLI |
|---|---|
| Runtime Agent tool (`general-purpose`, `Explore`) | `.gemini/agents/*.md` with YAML frontmatter |

**What changes**: Subagents move from implicit runtime types to explicitly defined agent files.

**Claude Code pattern** (in command prompts):
```
Launch a general-purpose subagent with instructions to read the linked insights and generate the full PRD...
```

**Gemini CLI equivalent** — define a subagent file:
```yaml
---
name: prd-generator
description: Generates PRDs from problem statements and linked insights
tools: [read_file, write_file, replace, grep_search, glob]
model: gemini-2.5-pro
---

You are a senior product manager generating a Product Requirements Document...
```

Then reference in command prompts via `@prd-generator` or let the model auto-delegate.

**Notes**:
- Gemini subagents have isolated context windows — similar to Claude Code's Agent tool
- Subagents can be tool-restricted (e.g., `Explore`-equivalent gets only read tools)
- Subagents cannot call other subagents (no recursion) — same constraint as Claude Code
- Requires `"experimental": { "enableAgents": true }` in settings
- Built-in `codebase_investigator` subagent may replace the `Explore` agent type for read-only analysis

**Effort**: Medium. Need to create explicit agent definition files and update command prompts to reference them. The delegation logic in commands like `/prd`, `/discover`, `/eval`, `/gtm`, `/uat` all use subagents and would need prompt adjustments.

---

### 3. Hooks

| Claude Code | Gemini CLI |
|---|---|
| `SessionStart`, `PostToolUse` (Write matcher) | 10 hook events across 4 categories |

**Current hooks**:
1. **SessionStart** → runs `session-context.sh` to inject context
2. **PostToolUse (Write)** → runs `validate-frontmatter.sh` on written files
3. **PostToolUse (Write)** → runs `validate-crosslinks.sh` on written files

**Gemini CLI mapping**:

| Claude Code Hook | Gemini CLI Hook | Notes |
|---|---|---|
| `SessionStart` | `SessionStart` | Direct equivalent |
| `PostToolUse` (Write matcher) | `AfterTool` (matcher: `write_file`) | Direct equivalent — matcher syntax may differ slightly |

**Gemini CLI provides additional hooks not currently used**:
- `BeforeTool` — could deny or rewrite tool args (useful for guardrails)
- `BeforeAgent` / `AfterAgent` — could inject context or reject responses
- `PreCompress` — could preserve critical context before compression

**Notes**:
- Hooks communicate via stdin/stdout JSON in Gemini CLI — need to verify the shell scripts work with this interface or wrap them
- Same `settings.json` configuration pattern

**Effort**: Low. The hook events map directly. Shell scripts may need minor adjustments to handle Gemini's JSON stdin/stdout protocol.

---

### 4. MCP Servers

| Claude Code | Gemini CLI |
|---|---|
| `mcpServers` in `.claude/settings.json` | `mcpServers` in `.gemini/settings.json` |

**Current MCP servers**: Jira, Miro, Lucid, Figma, Slack — all Python FastMCP via `uv`.

**Gemini CLI equivalent**:
```json
{
  "mcpServers": {
    "jira": {
      "command": "uv",
      "args": ["run", "--directory", "mcp-servers/jira-server", "python", "server.py"],
      "env": {
        "JIRA_BASE_URL": "$JIRA_BASE_URL",
        "JIRA_EMAIL": "$JIRA_EMAIL",
        "JIRA_API_TOKEN": "$JIRA_API_TOKEN"
      }
    }
  }
}
```

**Notes**:
- Nearly identical config shape — env var syntax may differ slightly (`${VAR}` vs `$VAR`)
- Gemini supports additional transports (SSE, HTTP streaming) beyond stdio — not needed but available
- Tool names get namespaced as `mcp_serverName_toolName` — command prompts referencing MCP tools may need updating
- Gemini supports `includeTools`/`excludeTools` for filtering exposed MCP tools

**Effort**: Very low. Config copy with minor syntax adjustments.

---

### 5. Project Instructions

| Claude Code | Gemini CLI |
|---|---|
| `CLAUDE.md` (single file) | `GEMINI.md` (hierarchical — global, project, subdirectory) |

**What changes**: Rename and potentially split.

**Notes**:
- Gemini supports `~/.gemini/GEMINI.md` (global) + project root `GEMINI.md` + subdirectory `GEMINI.md` files that merge automatically
- Could split the current monolithic `CLAUDE.md` into per-directory files (e.g., `data/GEMINI.md` with data conventions, `prompts/GEMINI.md` with prompt guidelines) — optional but useful
- `/init` command can auto-generate a `GEMINI.md` for the project

**Effort**: Very low. Content copy + rename. Hierarchical splitting is optional.

---

### 6. File Tools

| Claude Code | Gemini CLI | Notes |
|---|---|---|
| `Read` | `read_file` | Supports `offset`/`limit` line slicing |
| `Write` | `write_file` | Requires confirmation |
| `Edit` | `replace` | `old_string`/`new_string` + `allow_multiple` flag |
| `Grep` | `grep_search` | Regex with `include` glob filter |
| `Glob` | `glob` | `case_sensitive` and `respect_git_ignore` options |
| `Bash` | Shell execution | Equivalent |
| — | `read_many_files` | Bonus: batch file reading |
| — | `list_directory` | Bonus: directory listing as a tool |

**Effort**: None for the tools themselves. Command prompts that reference tool names by their Claude Code names (e.g., "use the Read tool") would need updating.

---

### 7. Data and Prompts

| Component | Migration Needed? |
|---|---|
| `data/` (all artifacts) | No — plain Markdown/JSON files |
| `prompts/` (templates) | No — plain Markdown files |
| `data/meta/` (counters, tags) | No — plain JSON files |
| `background_information/` | No — plain files |
| `scripts/` | No — shell scripts |

**Effort**: Zero. Fully portable as-is.

---

## Effort Summary

| Component | Files | Effort | Risk |
|---|---|---|---|
| Slash commands (MD → TOML) | 22 | Low | Low — mechanical conversion |
| Subagent definitions | ~3-5 new files | Medium | Medium — delegation prompt adjustments |
| Hooks | 3 hooks | Low | Low — direct event mapping |
| MCP servers | 5 servers | Very low | Low — config copy |
| Project instructions | 1 file | Very low | None |
| Command prompt adjustments | 22 | Medium | Medium — tool name references, subagent invocation syntax |
| Data and prompts | 0 | Zero | None |

**Total estimated effort**: A few focused sessions. The bulk of the work is the 22 command prompt adjustments (updating subagent references and tool name references), not architectural changes.

---

## Key Risks

1. **Model quality** — The PM Assistant's output quality depends heavily on the model's ability to follow complex multi-step instructions, maintain long-context coherence, and generate structured documents (PRDs, insights, OKRs). Gemini models should be validated against representative commands before committing to migration.

2. **Subagent behavior differences** — Claude Code's `general-purpose` and `Explore` agent types have built-in behavioral patterns. Gemini's subagents are defined from scratch, so the system prompts need to fully specify the behavior that Claude Code's agent types provide implicitly.

3. **Hook protocol** — Gemini hooks communicate via JSON on stdin/stdout. The existing shell scripts (`session-context.sh`, `validate-frontmatter.sh`, `validate-crosslinks.sh`) may need wrappers to handle this protocol.

4. **Tool name references in prompts** — Several command prompts reference Claude Code tool names (e.g., "launch a `general-purpose` subagent", "use the `Read` tool"). These references are scattered across 22 commands and prompt templates, requiring a careful find-and-replace pass.

---

## Recommended Validation Approach

Before migrating all 22 commands, port a single representative command end-to-end:

1. **Pick `/prd`** — it exercises subagents, file tools, prompt templates, counters, cross-links, and the self-eval loop
2. Port the command, its prompt template (`prompts/prd/generate-prd.md`), its eval rubric, and the required subagent definition
3. Run it against a real problem statement and compare output quality to the Claude Code version
4. If quality holds, proceed with the remaining 21 commands. If not, identify whether the gap is in the model, the prompt tuning, or the tooling
