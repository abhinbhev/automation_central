---
name: write-owr-hlr
description: "Generate an OWR (One Way Report) + HLR (High-Level Requirements) product document — the standard ABI template covering feature objectives, scope, assumptions, open questions, and the full 8-phase discovery-to-delivery checklist"
mode: agent
---

Generate an OWR + HLR word (docx) document using the standard ABI template.

## Inputs to collect

Before writing, ask for any missing items:
- **Feature / product name**
- **ADO feature ID and link** (optional)
- **Target date** — go-live or milestone
- **Team members** — all contributors
- **Objective** — 2–4 bullet points describing what is being built and why
- **Success metrics** — adoption, engagement, outcome, and business impact KPIs
- **Assumptions** — features in scope, technical approach, data scope (brands, regions, channels, periods, granularity)
- **Out-of-scope items**
- **Open questions**
- **Reference docs or design artefacts** — if provided, study the tone and writing style (not content) and apply it throughout

## Document structure

Produce the document in this order:

### Section 1 — Metadata table
| Field | Value |
|---|---|
| ADO Feature | |
| Area Path | |
| Target Date | |
| Document Status | DRAFT |
| Team Members | |
| Design File | |
| ADO Backlog | |

### Section 2 — Feature sections

- `/Objective` — what the feature does and why (4–7 bullets covering what, who, and success criteria; no prose filler)
- `/Success Metrics` — Goal → Metric table grouped as Adoption / Engagement / Outcome / Business Impact
- `/Assumptions` — three H3 subsections:
  - *Features in scope* — bulleted list of included capabilities
  - *Technical approach* — bulleted implementation approach
  - *Data scope* — table: Dimension | Value (brands, regions, channels, periods, granularity)
- `/Milestones` — table: Milestone | Date
- `/Requirements` — grouped under descriptive H3 capability headers (not "Scenario 1", "Scenario 2"); each bullet is a concise noun phrase or `trigger → outcome` mapping; no long "The system must…" sentences
- `/Out of Scope` — flat bullet list, 4–6 items, no Short-term / Long-term subsections; each item is a noun phrase
- `/Design` — artefact links table, then a **User Flows** H3 subsection (see below)
- `/Open Questions` — table: Question | Answer | Date Answered; one-line conversational questions; blank Answer/Date for unresolved items
- `Change & Request Log` — table: Request/Update | Requestor/Personnel | Date (pre-populate initial draft entry)
- `/Reference Links` — ADO feature URL and related features

### Section 3 — Discovery → Delivery Checklist (8 phases)

For each phase:
1. Open with `Goal: [one-line italic description]`
2. List feature-specific checklist items (not generic placeholders)
3. Close with `Required output: [concrete artefact name]`

| Phase | Goal |
|---|---|
| 1 — Discovery Framing & Alignment | Ensure problem, scope, business intent, and ownership are clear before any solutioning |
| 2 — Business Rules & Data Contract | Lock meaning, logic, and constraints before design |
| 3 — Discovery Validation (Users) | Validate hypotheses and decision flow with real users |
| 4 — HLR (High-Level Requirements) | Define MVP scope, non-goals, and dependencies before engineering starts |
| 5 — Design Handoff & Prototype Validation | Confirm design decisions match business rules before any build begins |
| 6 — Delivery Prep (User Stories & Walkthrough) | Ensure engineering has everything needed to start — no ambiguity on scope, states, or criteria |
| 7 — Release & Communication | Communicate the release and limitations to all affected stakeholders |
| 8 — Post-Release Validation & Learning | Confirm the feature works as intended in production and inform next iteration |

## User Flows (always include in Design section)

- Add a **User Flows** H3 under Design
- Write 3–5 numbered flows as H3 headings: `Flow 1 — <descriptive name>`
- Each flow is a step-by-step bullet list; use `→` to indicate outcomes
- End with a summary table — columns vary by feature (e.g. Flow | Entry point | Key events | Notes)

Example structure:
```
### User Flows

#### Flow 1 — <name>
- User does X.
- System responds → Y fires / Z appears.
- User does A → outcome B.

#### Flow 2 — ...

| Flow | Entry point | Key events | Notes |
|---|---|---|---|
```

## Writing conventions

- **Bullets over prose** — every line adds information
- **Requirements**: noun-phrase bullets or `trigger → outcome`; group under capability H3s
- **Out of Scope**: flat list, no subsections, 4–6 items max
- **Open Questions**: one-line conversational phrasing per question
- **Checklist items**: feature-specific, not generic
- **Tone**: collaborative working doc, not a formal spec — direct and specific
- Leave table cells blank (not "TBD") where information is not yet provided

## Generating .docx output

Once the outline is confirmed, offer to generate `.docx` files by running:

```bash
# Build all registered features
python scripts/office/generate_owr_docs.py

# Build a specific feature only
python scripts/office/generate_owr_docs.py --feature 156058

# Build multiple specific features
python scripts/office/generate_owr_docs.py -f 156056 -f 156058

# Custom output folder
python scripts/office/generate_owr_docs.py --out-dir working_directory/hlr

# Custom output folder + specific feature
python scripts/office/generate_owr_docs.py --out-dir working_directory/hlr --feature 156058
```

The script produces one fully-styled `.docx` per feature with ABI brand colours, dark banner header, metadata table, all Section 2 subsections, and the full Section 3 Discovery → Delivery Checklist.

### Registering a new feature in the script

When a new ADO feature is added, register it in `generate_owr_docs.py`:

1. Write a `_build_<id>(doc: Document) -> None` function following the existing pattern.
2. Add a 3-tuple entry to the `DOCS` list:
   ```python
   DOCS: list[tuple[str, str, callable]] = [
       ("156056", "156056-feedback-nudge-owr.docx", _build_156056),
       ("<id>",   "<id>-<kebab-title>-owr.docx",   _build_<id>),
       ...
   ]
   ```
3. The `--feature` flag uses the first element of each tuple as the lookup key.
4. Unknown feature IDs passed via `--feature` print a clear error listing valid options and exit with code 1.
