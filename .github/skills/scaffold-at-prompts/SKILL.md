---
name: scaffold-at-prompts
description: Interactively scaffold all 6 Langfuse prompt files for any Analysis Template (AT) pipeline use case across any domain — query enhancer, template selector, arguments selector, simple summarizer, complex summarizer, and response evaluator
mode: agent
---

## Overview

Scaffolds the `prompts/langfuse/<usecase>/` directory for any AT pipeline use case.
Produces `prompt.md` files for all 6 prompt types. All domain content is gathered from the user — nothing is assumed or hardcoded.

Companion to `scaffold-stored-procedure` and `scaffold-sp-wrapper`. Prompts are the third and final AT pipeline layer.

**Reference:** `templates/scripts/at_prompts_brief.md`  
**Example structure (not content):** `templates/prompts/`

**6 prompt types:**

| Type | Multiplicity | Path |
|---|---|---|
| `at_query_enhancer` | one per use case | `<usecase>/at_query_enhancer/prompt.md` |
| `at_template_selector` | one per use case | `<usecase>/at_template_selector/prompt.md` |
| `at_arguments_selector` | one per registered function | `<usecase>/at_arguments_selector/<function_name>/prompt.md` |
| `at_simple_summarizer` | one per source_name | `<usecase>/at_simple_summarizer/<source_name>/prompt.md` |
| `at_complex_summarizer` | one per complex function | `<usecase>/at_complex_summarizer/<function_name>/prompt.md` |
| `at_response_evaluator` | one per use case | `<usecase>/at_response_evaluator/prompt.md` |

`at_simple_summarizer` folder name = exact `source_name` from `@register_function` (spaces + capitalisation preserved). All others = snake_case function name.

## When to invoke

User says: "scaffold the AT prompts for X", "create the Langfuse prompt files for X", "build the prompt layer for the X use case", or similar.

## What to do

1. Read `templates/scripts/at_prompts_brief.md` for structure rules; review `templates/prompts/` for structure examples (ignore domain-specific values in those files)
2. Run the interview below type by type; generate each file before moving to the next
3. Never invent domain content — if a required value is unknown, ask before writing
4. Apply the universal rules (simple summarizer 12 rules, complex summarizer structural constraints) automatically

### Step 1 — Identity

Ask together:
- Root output path (full path ending in `prompts/langfuse/<usecase>/`)
- Use case name and domain / subject matter (brief description)
- Which of the 6 prompt types to generate (default: all)

### Step 2 — at_query_enhancer

Ask user to supply all domain values:
- Dimension allowlists to canonicalize (location names, product codes, segment labels…) — for each: canonical form + approximate user phrasings that map to it
- Acronym expansions — ask per pair
- Composite → expansion mappings (shorthand grouping → list of canonical values)
- Synonym normalizations (natural language term → canonical term)
- Anti-expansion words (terms that look expandable but must NOT be changed)
- Query-level defaults the enhancer should enforce

Output format:
```
### fsl_examples

*Empty*

### guidelines

<rules built entirely from user input>
```

### Step 3 — at_template_selector

Ask:
- Registered functions to select among (real `@register_function` names only)
- Per function: intent scope + 3–5 representative trigger phrases
- Priority ordering (user ranks from most to least specific)
- 15–25 disambiguation examples (query → function → one-line reason); ask for intentionally ambiguous edge cases
- Tie-breaking rules for hard cases priority alone cannot resolve

Output:
- Role paragraph
- `### Function Options` — `####` block per function
- `### Function Selection Priority` — numbered list in user's order
- `### Examples` — Markdown table
- `### Notes` — tie-breaking rules

### Step 4 — at_arguments_selector (loop per function)

For each registered function:
- Function name + one-sentence purpose
- Full parameter list matching SP wrapper signature; for each param:
  - Enumerated (allowlist) or open-ended?
  - Valid values / format (ask — do not invent)
  - Default when absent (None / literal / omit)
  - Normalization examples (colloquial → canonical — ask user)
  - Always-output-as-list rule (universal — state explicitly)
  - `"across"` eligible?
- 20–30 extraction examples (ask user; cover: time-only, entity+metric, trend/range, segmented, multi-metric, "across", absent params, edge cases)
- Special edge case rules

Always include verbatim: "Do not infer or default any parameter absent from the query; the downstream SP handles defaults at query-build time."

### Step 5 — at_simple_summarizer (loop per source_name)

For each source_name:
- Exact `source_name` string (folder name — preserve spaces + capitalisation)
- Result shape (wide vs. long)
- Rolling-period data present? If yes → always report period + period_type together
- Requested period can be absent? If yes → surface nearest available period explicitly
- Opaque column names needing inline definition?
- Reporting conventions (unit, index vs. percentage, rounding, paired metrics)
- Delta unit label ("p.p.", "pts", "%" — ask user)
- Entity/company name abbreviation expansions (ask user for any aliases)

Apply all **12 universal base rules** automatically (do not ask; apply verbatim):
1. Analyze data for trends across cuts; identify key or notable shifts
2. Identify top 3 increasing/decreasing or highest/lowest data points
3. If >2 time periods: identify trend; else comment on delta between the two periods
4. Do not use "significant" — use "notable"
5. Summarize in maximum 3–4 bullet points
6. Avoid jargon, fancy language, extrapolation; only use provided data
7. Delta: use +/- and the confirmed unit label; format: "metric X has moved from x.x to y.y (+z.z [unit]) gain / (-z.z [unit]) loss"; if no delta column is available, do not calculate on your own
8. Insert entity/company name aliases the user confirmed
9. Do not hallucinate; only use provided data; do not reason about external causes
10. Do not use "overall" or create an overall summary; focus on specific data points
11. Use bold markdown to highlight key entity names, values, and numbers — only 1–2 words/numbers per sentence
12. Do not summarize any metric where at least one time-period value is zero; ignore such metrics

Always open every simple summarizer with this lead sentence verbatim:
> Do not include any pointers about missing data. Only focus on the data that is passed. Avoid writing data for X Y Z is unavailable because it does not look good.

### Step 6 — at_complex_summarizer (loop per complex function)

For each function:
- Function name (folder name)
- Primary metric; supporting metrics
- Segmentation/dimension columns — which need dedicated mention?
- Any metric needing a special structural sub-breakdown? If yes: ask for structure description + worked example
- Delta unit label
- Hard editorial constraints specific to this function's subject matter

Always apply these structural rules:
- **Same-direction grouping**: only discuss supporting metrics that move in the same direction as the primary metric
- **Segmentation coverage**: always include 1–2 points on cross-segment trends; ask user which segments matter most
- **No headers on bullet points**: plain bullet text only
- **Delta format**: +/- + confirmed unit label

Output: General Instructions → numbered Summary rules → numbered Conclusion rules → user-supplied special-structure block (with worked example if provided)

### Step 7 — at_response_evaluator

Ask:
- Domain equivalences — synonym groups to treat as identical
- System auto-behaviors that must never be penalized (enumerate ALL pipeline defaults: auto prior-period, auto delta, auto time default, all-rows default when top-k not specified, etc.). **Also include**: metrics returning `NULL` for segments where the denominator/weight is zero (e.g. ROI returning NULL when a segment has no media spend in that period) — this is correct SP behavior, not missing data, and must not be penalized.
- Hard failure conditions — patterns that must always be flagged
- FSL grading examples (default: `*Empty*`)

Output: `### guidelines` + `### fsl_examples`

### Step 8 — Post-generation checklist (print after all files written)

Print file paths created, then:
- Naming check: `at_simple_summarizer/` folder = exact `source_name`; all others = snake_case function name
- Langfuse cache: allow ~300 seconds after upload before live testing
- Verification:
  - Template selector: 10–15 queries (including ambiguous) → verify function mapping
  - Arguments selector: 5–6 complex queries per prompt → compare against expected output
  - Simple summarizer: 3–4 end-to-end runs → check bold formatting, delta label, bullet count (≤4)
  - Query enhancer: raw query → enhanced query → verify all expansions fire correctly
  - Response evaluator: 1 correct + 1 incorrect answer → verify "do not penalize" list respected
