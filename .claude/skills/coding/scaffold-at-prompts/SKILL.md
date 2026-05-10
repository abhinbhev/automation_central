---
name: scaffold-at-prompts
description: Interactively scaffold all 6 Langfuse prompt files for any Analysis Template (AT) pipeline use case across any domain — query enhancer, template selector, arguments selector, simple summarizer, complex summarizer, and response evaluator
domain: coding
requires_script: false
---

## Usage

Invoke with `/scaffold-at-prompts` then answer the interview below.
The skill generates `prompt.md` files for **any AT pipeline use case, any domain**. Nothing domain-specific is baked in — all content is derived entirely from what the user provides. The skill only brings structure and universal rules; the user brings the domain knowledge.

Read alongside `/scaffold-stored-procedure` and `/scaffold-sp-wrapper` — prompts are the third and final layer of the AT pipeline.

**Output location:** `prompts/langfuse/<usecase>/` — skill is repo-agnostic; ask the user for the root path.

**AT pipeline sequence:**
```
User query
  → [at_query_enhancer]      Normalizes abbreviations, synonyms, entity names
  → [at_template_selector]   Picks which top-level function to call
  → [at_arguments_selector]  Extracts structured parameters from the query
  → SP class + wrapper       Fetches data
  → [at_simple_summarizer]   Writes 3-4 bullet narrative (factual results)
       OR
  → [at_complex_summarizer]  Writes multi-section narrative (analytical results)
  → [at_response_evaluator]  Grades the final answer quality
```

**The 6 prompt types:**

| Prompt type | One per | Folder path |
|---|---|---|
| `at_query_enhancer` | use case | `<usecase>/at_query_enhancer/prompt.md` |
| `at_template_selector` | use case | `<usecase>/at_template_selector/prompt.md` |
| `at_arguments_selector` | registered function | `<usecase>/at_arguments_selector/<function_name>/prompt.md` |
| `at_simple_summarizer` | source_name label | `<usecase>/at_simple_summarizer/<source_name>/prompt.md` |
| `at_complex_summarizer` | complex function | `<usecase>/at_complex_summarizer/<function_name>/prompt.md` |
| `at_response_evaluator` | use case | `<usecase>/at_response_evaluator/prompt.md` |

**Key naming rule:** `at_simple_summarizer/` folder name = exact `source_name` string from `@register_function("name", "source_name")` — spaces and capitalisation preserved, NOT the function name. All other service folders use the registered function name (snake_case).

**How prompts are fetched at runtime:**
- Dynamic use-case prompts are fetched by `fetch_dynamic_usecase_prompt(usecase, service_name, function_name)` and injected as `guidelines` template variables.
- Prompts are **cached for 300 seconds** in memory; changes take effect after cache expires.
- The file path encodes the Langfuse key: `<usecase>/<service>/<function_name>`.

## Output

For each prompt type selected, one `prompt.md` file at the correct path. Content is built entirely from user-supplied inputs — the skill writes structure, universal rules, and formatting; the user supplies all domain values.

**Universal rules applied to every prompt file (non-negotiable):**
- Plain prose, minimal markup — no HTML; Markdown tables in example sections are fine
- Enumerated values (entity names, codes, identifiers) written in the canonical form the user specifies
- Always include `### fsl_examples` section even if empty (use `*Empty*`) — the service fetches this section independently
- Numbered rules for procedural instructions; prose for context-setting
- Include explicit anti-rules ("do not do X") for every common failure mode the user describes
- Define every abbreviation and domain term on first use — the LLM's context is stateless per call
- Define `"across"` wherever it appears as a parameter value: "all values in this dimension, show breakdown by this dimension"
- Examples trump prose for LLM accuracy — a 20-row examples table does more than 3 paragraphs of rules

## Steps

1. Run Step 1 (identity) — confirm use case name, domain context, output path, and which prompt types to generate; use the Prompt Structures section below for all file formats
2. For each selected type: run its interview step and generate the file before moving to the next type — do not batch all interviews first
3. Within every interview step: do not invent domain content — if a required field (valid values, examples, rules) has not been provided, ask before writing
4. Apply universal base rules automatically (simple summarizer 12 rules, complex summarizer structural constraints); ask only about per-use-case additions or confirmed deviations
5. Write files; create parent directories as needed
6. Print all paths written and the post-generation checklist (Step 8)

### Step 1 — Use case identity
Ask together:
- Root output path (full path to `prompts/langfuse/<usecase>/`)
- Use case name string (runtime key)
- Domain / subject matter — brief description so prompts can be written with correct context
- Which prompt types to generate? (checklist; default: all 6)

### Step 2 — `at_query_enhancer`
Ask the user to supply all domain content; do not assume any value:
- **Entity allowlists** — any dimension whose values must be canonicalized (e.g. location names, product codes, segment labels). For each: what are the canonical forms, and what approximate user phrasings should map to them?
- **Acronym expansion table** — domain abbreviations and their full expansions; ask user for each pair
- **Composite → expansion mappings** — shorthand expressions that should expand to a list of values (e.g. a regional grouping → list of specific locations, a metric family name → list of individual metric names)
- **Synonym mappings** — natural language terms that must be normalized to a canonical domain term
- **Anti-expansion words** — terms that look expandable but must NOT be touched (ask user)
- **Query-level defaults** — any implicit behaviors the enhancer should enforce (e.g. default time granularity, default aggregation level)

Generate `at_query_enhancer/prompt.md` using the **Query Enhancer structure** in Prompt Structures below.

### Step 3 — `at_template_selector`
Ask:
- Top-level registered functions to choose among (real `@register_function` functions only, not dummies)
- Per function: scope description (what query intent it handles) + 3–5 representative trigger phrases
- Priority ordering: which function wins when two could apply — ask user to rank from most to least specific
- 15–25 disambiguation examples: user query → correct function → one-line reasoning; ask for intentionally ambiguous edge cases
- Tie-breaking rules: hard cases the priority ordering alone cannot resolve

Generate `at_template_selector/prompt.md` using the **Template Selector structure** in Prompt Structures below.

### Step 4 — `at_arguments_selector` (loop per function)
For each top-level registered function:
- Function name (snake_case, becomes folder name) + one-sentence purpose
- Full parameter list matching the SP wrapper signature; for each parameter:
  - Enumerated (user-supplied allowlist) or open-ended?
  - Valid values or format (ask user — do not invent)
  - Default when absent from query (None, a literal, or omit entirely)
  - Normalization rule: colloquial phrasing → canonical value (ask user for examples)
  - Always output as a list, even single-valued (universal rule — state explicitly)
  - `"across"` eligible?
- 20–30 extraction examples (ask user to supply representative queries covering: time-only, entity+metric, trend/range, segmented, multi-metric, "across", absent params, domain edge cases)
- Special edge case rules (ask user)

Always include the **"only extract what is present" rule** verbatim: do not infer or default any parameter that is absent from the query; the downstream SP class handles defaults at query-build time.

**Standard time parameters (present in most functions):**
- `year` — 4-digit integers; ranges expand to list; no default (leave absent if not mentioned)
- `period` — Jan/Feb/.../Q1/Q2/Q3/Q4/H1/H2/FY; multi-valued lists
- `period_type` — QTR, YTD, MTH, half year, full year, R3M/R6M/R9M/R12M
- `country` — lowercase canonical name from use-case allowlist

Generate `at_arguments_selector/<function_name>/prompt.md` using the **Arguments Selector structure** in Prompt Structures below.

### Step 5 — `at_simple_summarizer` (loop per source_name)
For each source_name:
- Exact `source_name` string (this is the folder name — spaces and capitalisation preserved)
- Result shape: wide (one column per metric) or long (a `value` column with a metric-identifier column)?
- Rolling-period data present? (e.g. R12M, R6M) — if yes, add rule: always report period + period_type together
- Requested period can be absent? — if yes, add rule: surface nearest available period explicitly
- Any opaque column names needing inline definition for the LLM?
- Domain-specific reporting conventions (metric unit, index vs. percentage, rounding, pairs that always appear together)?
- Additional zero-value suppression rules beyond the universal default?
- Delta unit label for this use case (e.g. "p.p." for percentage points, "pts" for index points, "%" for raw percent)
- Company/entity name conventions (e.g. what any abbreviation stands for)

Apply all **12 universal base rules** automatically (do not ask — these are non-negotiable):
1. Analyze data for trends across cuts; identify key or notable shifts
2. Identify top 3 increasing/decreasing or highest/lowest data points
3. If >2 time periods: identify trend; else comment on delta between the two periods
4. Do not use "significant" — use "notable" instead
5. Summarize in maximum 3–4 bullet points
6. Avoid jargon, fancy language, extrapolation; only use the provided data
7. Delta: use +/- and the confirmed unit label; format: "metric X has moved from x.x to y.y (+z.z [unit]) gain / (-z.z [unit]) loss"; if no delta column is available, do not calculate on your own
8. Insert entity/company name aliases the user confirmed
9. Do not hallucinate; only use provided data; do not reason about external causes
10. Do not use "overall" or create an overall summary; focus on specific data points
11. Use bold markdown to highlight key entity names, values, and numbers — only 1–2 words/numbers per sentence
12. Do not summarize any metric where at least one time-period value is zero; ignore such metrics

Always open every simple summarizer with this lead sentence verbatim:
> Do not include any pointers about missing data. Only focus on the data that is passed. Avoid writing data for X Y Z is unavailable because it does not look good.

Generate `at_simple_summarizer/<source_name>/prompt.md` using the **Simple Summarizer structure** in Prompt Structures below.

### Step 6 — `at_complex_summarizer` (loop per complex function)
For each function:
- Function name (snake_case, folder name)
- Primary metric this function reports on (ask — do not assume)
- Supporting metrics that accompany it (ask user for full list)
- Segmentation/dimension columns in the result; for each: does it require dedicated mention in the narrative?
- Does any metric require a special structural breakdown? (e.g. two sub-categories that each need their own sub-section). If yes: ask for the structure description and a worked example of the desired output format
- Delta unit label (same as confirmed in Step 5, or confirm separately)
- Any hard editorial constraints specific to this function's subject matter?

Always apply these structural rules regardless of domain:
- **Same-direction grouping**: only discuss supporting metrics that move in the same direction as the primary metric — prevents contradictory narratives; this is the most important editorial constraint
- **Segmentation coverage**: always include at least 1–2 points on cross-segment trends; ask the user which segment cross-cuts matter most
- **No headers on bullet points**: UI renders plain bullet text; headers break the visual style
- **Delta format**: +/- symbols + confirmed unit label

Generate `at_complex_summarizer/<function_name>/prompt.md` using the **Complex Summarizer structure** in Prompt Structures below.

### Step 7 — `at_response_evaluator`
Ask:
- Domain equivalences — synonym groups the evaluator must treat as identical (ask user; do not invent)
- System auto-behaviors that must never be penalized — ask user to enumerate ALL pipeline defaults (e.g. auto-including prior-period comparison, auto-calculating delta, defaulting time period when absent, returning all rows when top-k requested). **Also include**: metrics returning `NULL` for segments where the weight is zero (e.g. ROI returning NULL when there is no media spend in a segment for that period) — this is correct SP behavior, not a data gap.
- Hard failure conditions — response patterns that must always be flagged (ask: missing required entity, unsupported format, metric mismatch, etc.)
- FSL grading examples (optional; default `*Empty*`)

Generate `at_response_evaluator/prompt.md` using the **Response Evaluator structure** in Prompt Structures below.

### Step 8 — Post-generation checklist (print after all files written)
- Naming reminder: `at_simple_summarizer/` folder = exact `source_name` (spaces + capitalisation preserved); all other folders = snake_case function name
- Langfuse cache: allow 300 seconds after upload before testing
- Verification:
  - Selector accuracy: run 10–15 queries (including ambiguous ones) through template selector; verify function mapping
  - Arguments extraction: test 5–6 complex examples per arguments-selector prompt; compare output against expected
  - Summarizer quality: 3–4 end-to-end pipeline runs; check bold formatting, delta unit labels, bullet count (≤4)
  - Enhancer round-trip: raw query → enhancer → verify all expansions fire correctly
  - Evaluator sanity: one correct + one incorrect answer → verify grading against "do not penalize" list

---

## Prompt Structures

Canonical file formats for all 6 prompt types. All content inside `<...>` is user-supplied.

### Query Enhancer structure

```markdown
### fsl_examples

*Empty*

### guidelines

Your job is to enhance the query according to the instructions. Do not go beyond them.

<Entity allowlist name>: [<canonical values...>]
If a <entity type> name approximately matches one of these, enhance it to the canonical form.
Example: <user phrasing> → <canonical value>, <user phrasing> → <canonical value>.

Acronym expansions:
- <ACRONYM> → <expansion>
- <ACRONYM> → <expansion>

Do not expand: <anti-expansion word list>.

Composite mappings:
- <shorthand> → <expanded list>

Synonym mappings:
- <term1>, <term2> → <canonical term>

<Any query-level defaults>
```

### Template Selector structure

```markdown
## Template Selection Prompt

<Role definition — 2–3 sentences describing the task.>

---

### Function Options

#### 1. <function_name>
Use when:
- <condition>
- <condition>
- Examples of triggers: *"<phrase>", "<phrase>", "<phrase>"*

---

#### 2. <function_name>
Use when:
- <condition>
- Examples of triggers: *"<phrase>", "<phrase>"*

---

(repeat for each function)

### Function Selection Priority
1. <most specific scope> → `<function>`
2. <next> → `<function>`
...

---

### Examples (Expanded & Cross-Learned)

| User Query | Chosen Function | Reasoning |
|---|---|---|
| "<query>" | <function> | <reason> |
...

---

### Notes
- <Tie-breaking rule>
- <Edge case to avoid>
```

### Arguments Selector structure

```markdown
## <function_name> — Input Selection Prompt

<Role definition — 1–2 sentences.>
<Function purpose — when this function is used.>

---

### Parameters to Extract
[<param1>, <param2>, ...]

---

## Explicit variable value reference

Always output parameters as lists, even if a single value is present.
Do not infer or default any parameter absent from the query; the downstream SP handles defaults at query-build time.

---

### <param_name>
<Valid values or format. Normalization rules. Default when absent. "across" eligibility.>

---

(repeat for each param)

### Summary
<Brief restatement of the normalization mandate.>

---

### General Extraction Logic

#### 1. <rule category>
<rule>

---

### Examples (Expanded & Cross-Learned)

| User Query | Extracted Parameters |
|---|---|
| "<query>" | param1: [...], param2: [...] |
...

---

### Special Edge Case Logic

| Scenario | Behavior |
|---|---|
| <scenario> | <behavior> |

---

### Notes
```

### Simple Summarizer structure

```markdown
Do not include any pointers about missing data. Only focus on the data that is passed. Avoid writing data for X Y Z is unavailable because it does not look good.

1. Analyze data for trends across cuts. Identify key or notable shifts.
2. Identify top 3 increasing/decreasing or highest/lowest data points.
3. Identify trend if >2 time periods, else comment on delta between 2 periods.
4. Refrain from using "significant". Use "notable" instead.
5. Summarize in a maximum of 3–4 bullet points.
6. Avoid jargon, fancy language, or extrapolation. Only use data in sql_result.
7. If delta column is available: report delta with +/- symbols and <unit label>.
   Format: "metric X has moved from x.x to y.y (+z.z <unit>) gain / (-z.z <unit>) loss."
   If delta column is not available, do not calculate delta; only report values.
8. <Entity/company name alias confirmed by user — e.g. "ACME means ACME Corporation">
9. Avoid hallucinating. Only use data in sql_result. Do not make assumptions about the market.
10. Don't use "overall" or create an overall summary. Focus on specific data points.
11. Use bold markdown to highlight key entity names, values, and numbers.
    Only bold 1–2 words/numbers per sentence for readability.
12. Do not summarize any metric where at least one time-period value is zero; ignore such metrics.

<Per-source-name additions, if any>
```

### Complex Summarizer structure

```markdown
# General Instructions:
<Company/entity name alias. No-missing-data rule. Always include time periods. Bold formatting rule.>

How to write Summary:
1. Start with overview of main KPI in specified context/time period.
2. Discuss top highlights: notable increases or decreases in main or related KPIs.
3. Choose KPI highlights that move in the SAME direction as the main KPI.
4. If main KPI is decreasing, discuss related KPIs also decreasing.
5. Include cohort/segmentation analysis as specified.
6. Always include 1–2 bullet points on cross-segment trends.
7. Structure highlights to EXPLAIN the main KPI through supporting KPIs.
8. Keep concise; no jargon; don't reason about market influences.
9. Use +/- and <unit label> for deltas.
10. Don't add headers to bullet points.
11. <Any additional user-supplied summary rules>

How to write Conclusion:
1. Action-point highlights.
2. Mention top 3–5 most notable metrics to focus on.
3. Short and pointed.
4. No jargon.
5. <Any additional user-supplied conclusion rules>

# Additional special instructions for <KPI type> analysis:
<Include only if a metric requires a special structural breakdown. User must supply this block
with a worked example showing the desired output format.>

Summary:
<specific section rules>

Conclusion:
<specific conclusion rules>
```

### Response Evaluator structure

```markdown
### fsl_examples

*Empty*

### guidelines

Domain equivalences (treat as identical):
- <term A> = <term B> = <term C>
- <synonym group>

Do NOT penalize the following system-level behaviors:
- <auto-behavior 1>
- <auto-behavior 2>
...

Flag the following as issues:
- <hard failure condition 1>
- <hard failure condition 2>
...
```

---

## Notes & Gotchas

- **Folder name = source_name for simple summarizer.** The folder name under `at_simple_summarizer/` must exactly match the `source_name` string from `@register_function(name, source_name)`. Spaces, capitalisation, and special characters are preserved — e.g. `"Affinity and Meet Needs Analysis"` → folder is `Affinity and Meet Needs Analysis`.
- **The arguments selector controls what the SP class receives.** If a param is extracted incorrectly, the SP class builds a wrong SQL query silently. This makes the arguments selector the highest-risk prompt — invest most effort in the examples table.
- **`fsl_examples` is a separate fetchable section.** The service fetches `guidelines` and `fsl_examples` independently. Always include both even if `fsl_examples` is empty.
- **"Across" has two distinct uses.** In the template selector, "across" in a query is a cue to select a broad function. In the arguments selector, "across" is a parameter value meaning "all values, show breakdown." Define these independently in each prompt.
- **The complex summarizer's "same-direction" rule prevents contradictory narratives.** Without it, the LLM will mention KPIs moving in opposite directions in the same bullet. This is the most impactful editorial constraint.
- **Response evaluator "do not penalize" list must be exhaustive.** Any system default not listed risks being incorrectly flagged as a bug. When a new SP introduces new default behaviors, add those behaviors to the evaluator.
- **Pipeline consistency rule:** column names in the DataFrame produced by the SP wrapper must match what the summarizer prompt instructs the LLM to reference. If the SP returns a column called `custom_metric`, the summarizer must understand it — either via an explicit definition or common domain knowledge.
- **Langfuse path encodes the key.** A miscased folder name causes a cache miss and silent fallback to the default static prompt. Double-check naming.
