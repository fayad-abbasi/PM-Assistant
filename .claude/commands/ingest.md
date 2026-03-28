# Ingest — Background Content Integration

Review new content in `background_information/` and integrate useful frameworks, techniques, and concepts into PM Assistant workflows.

## Argument

$ARGUMENTS

If no argument is provided, default to `scan`.

## Actions

Parse the first word of the argument to determine the action:
- `scan` → Action 1
- `review` → Action 2
- `apply` → Action 3
- `history` → Action 4

---

## Action 1: Scan (`/ingest scan`)

Use an `Explore` subagent to check for new content:

1. Read `data/meta/ingestion_log.json`
2. List all items in `background_information/`:
   - **Folders**: each folder (exclude `TABLE_OF_CONTENTS.md`)
   - **Standalone files**: PDFs (`.pdf`), markdown files (`.md`), and other documents directly in the root of `background_information/` (exclude `TABLE_OF_CONTENTS.md`)
3. Compare: find items NOT listed in the ingestion log's `reviewed` array (match on `folder` field — for standalone files, `folder` is the filename)
4. Report results:

**If new content found:**
```
INGEST SCAN — {date}

{n} new item(s) detected in background_information/:

  • {Folder Name} — {list of files found}
  • {Filename.pdf} — standalone file

Run `/ingest review` to analyze these for workflow improvements.
```

**If nothing new:**
```
INGEST SCAN — {date}

No new content detected. All {n} items in background_information/ have been reviewed.

Last review: {most recent reviewed_at from log}
```

---

## Action 2: Review (`/ingest review`)

For each new/unreviewed folder, perform a deep analysis against the current PM Assistant workflows.

### Step 1: Identify unreviewed content

Read `data/meta/ingestion_log.json` and list all folders in `background_information/` not yet in the log. If none are new, say so and stop.

### Step 2: Read current workflow state

Launch a `general-purpose` subagent with instructions to:

1. **Read the new content** — For each unreviewed item:
   - **Folders**: read `summary.md` and `content.md` (if present)
   - **Standalone PDFs**: read the PDF directly (use the Read tool with pages parameter for large PDFs)
   - **Standalone .md files**: read the file directly
2. **Read the current workflows** — Scan these to understand what's already in the PM Assistant:
   - All files in `.claude/commands/` (the slash commands)
   - All files in `prompts/` (recursively — the prompt templates)
   - `data/meta/tags.json` (the tag taxonomy)
   - `background_information/TABLE_OF_CONTENTS.md` (existing reference index)
3. **Analyze each piece of content** through a PM-workflow improvement lens. For each unreviewed folder, answer:
   - Does it introduce new frameworks, techniques, or methodologies not currently referenced in the prompts?
   - Does it suggest improvements to existing rubrics or evaluation criteria?
   - Does it contain concepts that should be added to the tag taxonomy in `data/meta/tags.json`?
   - Does it suggest new workflow steps or command enhancements?
   - Does it contain insights about discovery, PRDs, strategy, GTM, UX, UAT, outcomes, or retros that could strengthen those specific command workflows?
4. **Produce a structured recommendation** for each piece of content:

```
─── REVIEW: {Folder Name} ───

Relevance: {high | medium | low | none}

Recommended Actions:
  1. {Specific change} → {target file}
  2. {Specific change} → {target file}
  3. ...

Target Files:
  - {path/to/file1.md}
  - {path/to/file2.md}

Rationale:
{2-3 sentences explaining why these changes improve the workflow}

Suggested Outcome: {applied | skipped | deferred}
───────────────────────────────
```

5. **Present ALL recommendations to the user** and ask for approval before making any changes:

```
INGEST REVIEW — {date}

Reviewed {n} new item(s). Recommendations below.

{structured recommendations for each folder}

─── NEXT STEPS ───
Review the recommendations above. Then:
  • To apply all: `/ingest apply`
  • To discuss specific items: reply with feedback
  • To skip: no action needed (items remain unreviewed)
```

**IMPORTANT:** Do NOT make any file changes during review. This action is analysis-only. All modifications happen in `/ingest apply`.

---

## Action 3: Apply (`/ingest apply`)

Apply the recommendations from a prior `/ingest review`. This action modifies files.

1. Confirm with the user: "Apply the recommendations from the last review? (Reply with any adjustments, or confirm to proceed.)"
2. Wait for user confirmation before proceeding.
3. For each approved recommendation:
   - Make the specified changes to the target files (prompt templates, tags.json, command files, etc.)
   - Be surgical — only add or modify what was recommended, don't rewrite entire files
4. Update `background_information/TABLE_OF_CONTENTS.md`:
   - Add a new row to the main table for each new folder
   - Update the "How These Map to PM Assistant Workflows" table if new command mappings apply
   - Follow the existing table format exactly (see current entries for style)
5. Update `data/meta/ingestion_log.json`:
   - Add an entry to the `reviewed` array for each processed item
   - Set `folder` to the folder name or standalone filename
   - Set `reviewed_at` to current ISO datetime
   - Set `files` to the list of files in the folder, or `["{filename}"]` for standalone files
   - Set `outcome` to `applied`, `skipped`, or `deferred` based on what was done
   - Set `notes` to a brief description of changes made

After applying:
```
INGEST APPLY — {date}

Applied changes for {n} item(s):

  ✓ {Folder Name} — {brief summary of changes made}
    Files modified: {list}

  ✓ {Folder Name} — {brief summary of changes made}
    Files modified: {list}

Ingestion log updated. TABLE_OF_CONTENTS.md updated.

Run `/ingest scan` to verify no items remain unreviewed.
```

---

## Action 4: History (`/ingest history`)

Use an `Explore` subagent to display the ingestion log:

1. Read `data/meta/ingestion_log.json`
2. Display all entries as a table:

```
INGEST HISTORY — {date}

| # | Folder | Reviewed | Outcome | Notes |
|---|--------|----------|---------|-------|
| 1 | {name} | {date}   | applied | {notes} |
| 2 | {name} | {date}   | skipped | {notes} |
...

Total: {n} reviewed | {applied} applied | {skipped} skipped | {deferred} deferred
```

---

## Rules

- **Never modify files during `scan` or `review`** — those are read-only operations
- **Always present recommendations before applying** — the user must approve changes
- **Use `general-purpose` subagent** for `review` (needs to read many files and produce structured analysis)
- **Use `Explore` subagent** for `scan` and `history` (read-only operations)
- **Match folder names exactly** when comparing against the ingestion log
- Tags added to `data/meta/tags.json` must follow existing category structure
- Changes to prompt templates should be additive (add sections/frameworks) not destructive (don't remove existing content)
- TABLE_OF_CONTENTS.md updates must follow the existing table format precisely

---

## Next Steps (suggest after completing an action)

| After... | Suggest... |
|----------|-----------|
| Scanning (new content found) | "Run `/ingest review` to analyze the new content" |
| Scanning (nothing new) | "All caught up! Run `/next` to see what else needs attention" |
| Reviewing | "Run `/ingest apply` to apply the approved changes" |
| Applying | "Run `/ingest scan` to verify everything is processed" or "Run `/refresh` to reload context" |
| Viewing history | "Run `/ingest scan` to check for new content" |
