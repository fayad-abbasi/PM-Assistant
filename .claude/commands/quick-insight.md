# Quick Insight

A fast inner-loop command for capturing insights on the fly. Paste a quote, observation, or data point and get a tagged, linked insight file in one step — no menu, no back-and-forth.

## How It Works

The user provides raw input in **any format** — no structure required. Examples:
- A quote from a 1:1 or meeting (with optional source info)
- An observation or pattern they noticed
- A data point or metric
- A snippet pasted from a Slack thread, email, or meeting notes
- Rough bullet points jotted during a meeting
- A rambling voice-to-text transcription
- Mixed content with multiple observations in one paste

If the input contains multiple distinct observations, capture the strongest one as the primary insight and suggest running `/quick-insight` again for the others.

## Process

1. Parse the input — regardless of format or messiness — to identify:
   - **Source**: If the user mentions a person, team, meeting, or Slack channel, check `data/interviews/` and `data/stakeholder/people/` for a matching file to link. Fuzzy-match names (e.g., "Raj" → "Raj Mehta")
   - **Themes**: Extract 1-3 themes from the content, even if the input is unstructured
   - **Tags**: Auto-select from `data/meta/tags.json` based on content
   - **Confidence**: Estimate based on source quality (direct quote = high, secondhand = medium, speculation = low, rough notes = medium)
   - **Impact**: Estimate based on scope (affects many engineers = high, single team = medium, niche = low)

2. Read `data/meta/counters.json`, increment the `insight` counter, write back

3. Write the insight directly to `data/insights/` with frontmatter:
```yaml
---
id: insight-{date}-{NNN}
title: "{auto-generated from content}"
type: single
linked_interviews: [{matched interview IDs, or empty}]
themes: [{extracted themes}]
confidence: {low|medium|high}
impact: {low|medium|high}
tags: [{auto-selected from tags.json}]
status: active
created_at: {ISO-datetime}
---
```

4. Body: the original input formatted as a structured insight with:
   - **Key Quote / Observation** (the raw input)
   - **Interpretation** (1-2 sentences on what this means)
   - **Implication** (1 sentence on what to do about it)

5. Run the quality-checker:
   - Read `prompts/evals/rubric-interview.md` and `prompts/evals/judge-prompt.md`
   - Score it. If below threshold (avg >= 3.5), fix and re-write
   - Save eval result to `data/evals/`

6. Present a brief confirmation:
   ```
   Saved: data/insights/{filename}.md
   ID: insight-{date}-{NNN} | Confidence: HIGH | Impact: MEDIUM
   Tags: [automation, workflow] | Linked: interview-2026-03-05-001
   Score: 4.2/5
   ```

## Rules

- No menus, no questions — go straight to generating the insight
- If the source is ambiguous, make your best guess on links and flag it: "Linked to interview-X — correct?"
- If the user provides the interviewee name or company, fuzzy-match against existing interviews
- Tags must come from `data/meta/tags.json`
- Always read and update `data/meta/counters.json`
- Keep the output to 3-4 lines max — this is a fast capture tool
