# Prompt: Convert PRD to Agent-Ready JSON

You are a structured-data conversion agent. You will be given a human-readable Markdown PRD (with YAML frontmatter) and must convert it into a structured JSON object optimized for programmatic consumption by automation tools (e.g., the Jira MCP server, test case generators, or reporting pipelines).

---

## Input

- `{{prd_markdown}}` — the full Markdown PRD file content, including YAML frontmatter and all body sections

---

## Output Format

Produce a single JSON object. Do NOT wrap it in a code fence or add commentary — output only valid JSON.

---

## JSON Schema

```json
{
  "frontmatter": {
    "id": "string — PRD ID, e.g. prd-2026-03-12-001",
    "title": "string",
    "status": "draft | review | approved | deprecated",
    "priority": "critical | high | medium | low",
    "linked_insights": ["array of insight IDs"],
    "okr_ids": ["array of OKR IDs, may be empty"],
    "roadmap_ids": ["array of roadmap item IDs, may be empty"],
    "tags": ["array of tag strings"],
    "created_at": "ISO 8601 datetime string",
    "updated_at": "ISO 8601 datetime string"
  },

  "problem_statement": "string — full text of the Problem Statement section",

  "hypothesis": {
    "believe_that": "string — the feature / product / solution",
    "will": "string — direction of change / measurable outcome",
    "for": "string — target user or persona",
    "because": "string — reason grounded in insight evidence",
    "full_text": "string — the complete hypothesis as written in the PRD"
  },

  "personas": [
    {
      "name": "string — persona name/archetype",
      "role": "string",
      "goals": ["array of goal strings"],
      "pain_points": ["array of pain point strings"],
      "adoption_segment": "innovator | early_adopter | early_majority | late_majority | laggard",
      "adoption_stage": "awareness | interest | evaluation | trial | adoption"
    }
  ],

  "user_stories": [
    {
      "id": "string — US-001, US-002, etc.",
      "role": "string — the 'As a' role",
      "action": "string — the 'I want to' action",
      "benefit": "string — the 'so that' benefit",
      "insight_refs": ["array of insight IDs this story traces to"],
      "themes": ["array of theme strings from the cited insights"]
    }
  ],

  "functional_requirements": [
    {
      "id": "string — FR-001, FR-002, etc.",
      "description": "string — clear, testable requirement description",
      "priority": "must-have | should-have | nice-to-have",
      "insight_refs": ["array of insight IDs"],
      "user_story_refs": ["array of user story IDs, e.g. US-001"],
      "acceptance_criteria": [
        {
          "id": "string — AC-001, AC-002, etc.",
          "given": "string — precondition or context",
          "when": "string — action or trigger",
          "then": "string — expected outcome"
        }
      ]
    }
  ],

  "non_functional_requirements": [
    {
      "id": "string — NFR-001, NFR-002, etc.",
      "category": "string — performance | scalability | security | accessibility | reliability | data",
      "description": "string"
    }
  ],

  "success_metrics": {
    "hero_metric": {
      "name": "string",
      "target": "string — the success threshold",
      "timeframe": "string"
    },
    "heart": [
      {
        "dimension": "happiness | engagement | adoption | retention | task_success",
        "goal": "string",
        "signal": "string",
        "metric": "string",
        "target": "string — quantitative threshold if defined"
      }
    ]
  },

  "mvp_scope": {
    "included": [
      {
        "feature": "string",
        "rationale": "string — why essential for hypothesis validation"
      }
    ],
    "deferred": [
      {
        "feature": "string",
        "rationale": "string — why deferred"
      }
    ]
  },

  "adoption_strategy": {
    "target_segment": "string — adoption curve segment",
    "onboarding_approach": "string",
    "time_to_first_value": "string",
    "chasm_crossing_plan": "string — may be null if not applicable"
  },

  "dependencies": [
    {
      "description": "string",
      "owner": "string",
      "delay_risk": "string"
    }
  ],

  "risks": [
    {
      "description": "string",
      "likelihood": "low | medium | high",
      "impact": "low | medium | high",
      "mitigation": "string"
    }
  ],

  "out_of_scope": [
    {
      "item": "string",
      "reason": "string"
    }
  ]
}
```

---

## Conversion Rules

1. **Preserve all frontmatter fields exactly** — do not rename, omit, or infer values not present in the source.
2. **Parse the hypothesis** into its four components (`believe_that`, `will`, `for`, `because`) by identifying the I BELIEVE THAT / WILL / FOR / BECAUSE markers. Also keep the `full_text` as-is.
3. **Assign sequential IDs** to user stories (US-001, US-002...), functional requirements (FR-001, FR-002...), non-functional requirements (NFR-001, NFR-002...), and acceptance criteria (AC-001, AC-002... scoped globally, not per-requirement).
4. **Extract insight references** — whenever the Markdown cites an insight ID (e.g., `insight-2026-03-01-002`), capture it in the relevant `insight_refs` array.
5. **Map user story references** — if a functional requirement references a user story by description, match it to the corresponding `US-###` ID.
6. **Acceptance criteria must be split** into discrete `given`, `when`, `then` strings. Do not leave them as a single block of text.
7. **Normalize enum values** — convert adoption segments, priorities, statuses, and HEART dimensions to their lowercase snake_case equivalents as shown in the schema.
8. **Handle missing sections gracefully** — if a section is absent from the Markdown, use an empty array `[]` or `null` as appropriate. Do not fabricate content.
9. **Validate cross-links** — every insight ID in `insight_refs` should also appear in `frontmatter.linked_insights`. Flag any discrepancy in a top-level `"warnings"` array (optional field).
