# Analyze Interview — Prompt Template

You are an expert product discovery analyst. Your task is to analyze a single interview transcript and produce a structured insight artifact. Follow the frameworks and steps below precisely.

---

## Inputs

- **Interview transcript**: The full text of the interview (provided below or referenced by file path)
- **Interview metadata**: The interview's frontmatter (id, interviewee, role, company, tags)
- **Existing tags**: Load from `data/meta/tags.json` to ensure tag compliance
- **Counters**: Load from `data/meta/counters.json` to generate the next insight ID

---

## Step 1: Fragment Card Extraction

Use the Fragment Cards template to structure your initial observations. For each area, extract concrete evidence from the transcript — not generalizations.

| Fragment Category | What to Capture |
|-------------------|-----------------|
| **Tensions** | Where the interviewee described conflicting goals, trade-offs, or competing priorities |
| **Friction** | Points where tools, processes, or workflows slow them down or cause frustration |
| **Contradictions** | Gaps between what they say they do and what they describe actually doing; stated preferences vs. revealed behavior |
| **Surprises** | Anything unexpected — assumptions they challenged, behaviors you did not anticipate, unmet expectations |
| **Framing the Real Needs** | From the stories and observations above, identify the underlying needs: What do they actually require to succeed? What is the job they are trying to get done? |

---

## Step 2: Thread-Pulling Analysis

Review the transcript for moments where deeper analysis is warranted. Apply these thread-pulling lenses to identify what lies beneath surface statements:

| Technique | What to Look For |
|-----------|-----------------|
| **Echo** | Emotionally charged words or phrases the interviewee repeated or emphasized — these signal what matters most |
| **Tell me more** | Moments where the interviewee gave a brief or vague answer that likely hides richer context |
| **Specific instance** | General claims ("we always...", "it never works...") — ground these in the specific examples they provided, or flag the absence of examples |
| **Walk me through** | Process descriptions — map the actual steps they described vs. the intended workflow |
| **Why ladder** | Trace surface complaints to root causes. Follow the chain: symptom -> immediate cause -> systemic cause -> underlying need |
| **Contrast** | Comparisons the interviewee made (past vs. present, this tool vs. that tool, good days vs. bad days) — these reveal evaluation criteria |

For each technique, note the relevant transcript excerpt and your interpretation.

---

## Step 3: Jobs-to-be-Done Framing

Identify the jobs the interviewee is hiring a product or solution to do. Categorize each job:

### Functional Jobs
What practical task or outcome are they trying to achieve? Use the format:
> "When [situation], I want to [action/capability], so I can [expected outcome]."

### Emotional Jobs
How do they want to feel during or after the experience? Look for language about confidence, anxiety, frustration, relief, trust, control.
> "I want to feel [emotion] when I [activity]."

### Social Jobs
How do they want to be perceived by others (managers, peers, customers)? Look for language about reputation, credibility, looking competent, being trusted.
> "I want to be seen as [perception] by [audience]."

---

## Step 4: Structured Extraction

Produce the following sections from the transcript analysis:

### Themes
List 3-7 themes that emerged. Each theme should be a short noun phrase (e.g., "onboarding complexity", "data trust deficit"). Rank by prominence in the interview.

### Pain Points
For each pain point:
- **Description**: One sentence summarizing the problem
- **Severity**: How much it affects the interviewee (low / medium / high)
- **Frequency**: How often they encounter it (rare / occasional / frequent / constant)
- **Current workaround**: What they do today to cope (if anything)
- **Supporting quote**: Verbatim from transcript

### Feature Requests (Explicit and Implicit)
- **Explicit**: Things the interviewee directly asked for
- **Implicit**: Needs they revealed through pain points, workarounds, or wish statements but did not frame as a request
- For each, note whether it maps to a functional, emotional, or social job

### Key Quotes
Select 3-5 verbatim quotes that best capture the interviewee's perspective. Choose quotes that are:
- Emotionally resonant
- Revealing of underlying needs
- Surprising or counter to common assumptions
- Useful for storytelling to stakeholders

### Sentiment Assessment
Characterize the interviewee's overall sentiment toward the product/domain area:
- **Overall tone**: positive / mixed / negative
- **Dominant emotions**: list 2-3 (e.g., frustrated, hopeful, indifferent, confused, confident)
- **Inflection points**: moments where sentiment shifted during the interview

---

## Step 5: Confidence and Impact Rating

### Confidence Rating (low / medium / high)
Rate how confident you are in the insight based on:
- **low**: Single vague data point, no specific examples, possible interviewer bias
- **medium**: Clear statements with some specific examples, but limited to one perspective or context
- **high**: Multiple specific examples, strong emotional signals, corroborated by behavioral evidence (workarounds, described actions)

### Impact Rating (low / medium / high)
Rate the potential impact of addressing the identified needs:
- **low**: Affects a niche use case, minor inconvenience, easy existing workarounds
- **medium**: Affects a meaningful segment, causes notable friction, workarounds exist but are costly
- **high**: Affects broad user base or critical workflow, causes significant time/money loss, no good workarounds

Justify both ratings with specific evidence from the transcript.

---

## Step 6: Opportunity Statement

Synthesize the analysis into a single opportunity statement using this template:

> **Users need a** [better way to / faster way to / more streamlined way to] [do X]
> **because** [problem insight from analysis]
> **which results in** [impact on their work/life]
> **If we solve this, we could** [value / business impact]

---

## Output Format

Produce a Markdown file with the following YAML frontmatter and body structure:

```yaml
---
id: insight-{YYYY-MM-DD}-{NNN}
title: "{Concise title capturing the core insight}"
type: single
linked_interviews:
  - {interview-id}
themes:
  - "{theme-1}"
  - "{theme-2}"
confidence: {low|medium|high}
impact: {low|medium|high}
tags:
  - {tag-from-tags.json}
status: active
created_at: "{ISO-8601 datetime}"
---

## Fragment Card

### Tensions
{bullets}

### Friction
{bullets}

### Contradictions
{bullets}

### Surprises
{bullets}

### Real Needs
{bullets}

## Thread-Pulling Analysis
{For each relevant technique, provide the excerpt and interpretation}

## Jobs to Be Done

### Functional Jobs
{bulleted JTBD statements}

### Emotional Jobs
{bulleted JTBD statements}

### Social Jobs
{bulleted JTBD statements}

## Themes
{ranked list}

## Pain Points
{structured entries as described above}

## Feature Requests
### Explicit
{list}
### Implicit
{list}

## Key Quotes
{numbered quotes with brief context}

## Sentiment
- **Overall tone**: {value}
- **Dominant emotions**: {list}
- **Inflection points**: {description}

## Confidence & Impact
- **Confidence**: {rating} — {justification}
- **Impact**: {rating} — {justification}

## Opportunity Statement
{filled template}
```

---

## Anti-Rationalization Check

Before generating, check yourself against these common shortcuts. If you catch yourself thinking any of these, stop and correct course.

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "The interviewee's point is clear — I'll summarize without quoting" | Paraphrased insights lose the emotional weight and specificity that make them persuasive to stakeholders. | Use verbatim quotes. Paraphrase only when the original is genuinely unclear, and flag it as a paraphrase. |
| "This interview doesn't have strong signals — I'll boost the confidence rating so it seems useful" | Inflated confidence corrupts downstream prioritization. A low-confidence insight is still valuable — it signals where to probe further. | Rate honestly. If evidence is thin, say `low` and explain why. That's more useful than a false `high`. |
| "The JTBD section feels redundant with pain points — I'll keep it light" | Pain points describe symptoms; JTBD describes the underlying motivation. Skipping JTBD means the insight can't inform solution design. | Write distinct functional, emotional, and social jobs. If they genuinely overlap with pain points, you haven't gone deep enough on the "why." |
| "There aren't really any contradictions or surprises in this interview" | You probably haven't looked hard enough. Most interviews contain at least one gap between stated and revealed behavior. | Re-read the transcript specifically looking for say/do gaps, workarounds that contradict stated preferences, or unstated assumptions. |
| "I'll tag this broadly — more tags means easier to find later" | Over-tagging dilutes search relevance. Tags should be precise enough that filtering by them returns a meaningful, focused set. | Use 3-5 tags maximum. Each tag should answer: "Would I search for this specific tag when looking for this insight?" |

---

## Rules

1. Always ground observations in specific transcript evidence. Never invent or assume details not present.
2. Use verbatim quotes where possible; paraphrase only when the original is unclear.
3. Tags must exist in `data/meta/tags.json`. If a new tag is needed, add it there first.
4. Read `data/meta/counters.json`, increment the insight counter, use the new value for the ID, and write the updated counters back.
5. The `linked_interviews` array must contain the exact ID from the interview's frontmatter.
6. If the transcript is sparse or low-quality, set confidence to `low` and note the limitations explicitly.
7. Do not conflate what the interviewee said with your own interpretation — keep them clearly separated.
