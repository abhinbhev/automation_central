---
name: write-owr-hlr
description: Generate an OWR (One Way Report) + HLR (High-Level Requirements) product document — the standard ABI template covering feature objectives, scope, assumptions, open questions, and the full 8-phase discovery-to-delivery checklist
domain: docs
requires_script: true
script: scripts/office/generate_owr_docs.py
---

## Usage

Invoke with `/write-owr-hlr` then provide:
- **Feature / product name** — e.g. `WatchTower Integration into OneWay`
- **ADO feature ID and link** (optional)
- **Target date** — desired go-live or milestone date
- **Team members** — names of all contributors
- **Objective** — 2–4 bullet points describing what is being built and why

Optionally provide:
- **Success metrics** — adoption, engagement, outcome, and business impact KPIs
- **Assumptions** — features in scope, technical approach, data scope (brands, regions, channels, periods, granularity)
- **Out-of-scope items** — what is explicitly excluded
- **Open questions** — any unresolved items
- **Reference docs or design artefacts** — if provided, study the tone and writing style and apply it throughout; do not copy content

## Output

A complete OWR + HLR word (docx) document with all sections populated, structured as follows:

**Section 1 — Product brief (metadata table)**
- ADO feature, area path, target date, document status, team members, quick links (design file, ADO backlog)

**Section 2 — Feature body**
- `/Objective` — what the feature does and why
- `/Success Metrics` — Goal → Metric table grouped as Adoption / Engagement / Outcome / Business Impact
- `/Assumptions` — three subsections: *Features in scope* (bulleted), *Technical approach* (bulleted), *Data scope* (table: brands, regions, channels, periods, granularity)
- `/Milestones` — table with key dates
- `/Requirements` — grouped under short capability-header H3s; each group uses concise noun-phrase bullets (not "Scenario N" labels, not long "must" sentences)
- `/Out of Scope` — flat bullet list, 4–6 items; no Short-term / Long-term subsections
- `/Design` — artefact links table, then a **User Flows** subsection (see below)
- `/Open Questions` — table: Question | Answer | Date Answered; questions phrased as one-line conversational questions
- `Change & Request Log` — table: Request/Update | Requestor/Personnel | Date
- `/Reference Links` — ADO feature URL and related features

**Section 3 — Discovery → Delivery Checklist (8 phases)**

Each phase opens with a one-line **Goal** (in italic), followed by feature-specific checklist items and a "Required output" line.

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

## Writing conventions

### Requirements
- Group under descriptive H3 capability headers — not "Scenario 1", "Scenario 2"
- Each bullet: short noun phrase or `trigger → outcome` mapping (e.g. `Brand page (identifier: 'brand') → label: 'Clara Brand Guidance'`)
- No long "The system must…" sentences

### Out of Scope
- Flat bullets only — no Short-term / Long-term split
- 4–6 items; each item is a noun phrase, not a sentence

### Open Questions
- One line per question, conversational phrasing (e.g. "Who owns the domain identifier contract — FE or platform?")
- Leave Answer and Date blank for unresolved items

### Design — User Flows
- Always include a **User Flows** H3 subsection within Design
- Write 3–5 numbered flows as H3 headings (`Flow 1 — <name>`) with step-by-step bullet points
- Each step uses `→` to indicate outcomes (e.g. `User clicks Share → system generates a shareable link`)
- End with a summary table: columns vary by feature (e.g. Flow | Entry point | Key events | Notes)

### Checklist phases
- Prepend each phase with: `Goal: [one-liner in italic]`
- Checklist items are feature-specific — do not use generic placeholders
- Close each phase with: `Required output: [concrete artefact name]`

### Tone
- Collaborative working doc, not a formal spec
- Bullets over prose everywhere
- Direct and specific — every line adds information

## Steps

1. Collect all required inputs — ask for any that are missing before drafting
2. If reference docs are provided, study the tone and style (not content) — apply it throughout
3. Set document status to `DRAFT` unless the user specifies otherwise
4. Populate the metadata table
5. Write Objective — bullet points, no fluff; 4–7 bullets covering what, who, and success criteria
6. Build Success Metrics table — Goal → Metric, grouped by Adoption / Engagement / Outcome / Business Impact
7. Write Assumptions — three H3 subsections: Features in scope, Technical approach, Data scope
8. Add Milestones table
9. Write Requirements — group under capability H3 headers; noun-phrase bullets or `trigger → outcome` per item
10. Write Out of Scope — flat bullet list, 4–6 items, no subsections
11. Write Design section — artefact links table, then User Flows (numbered H3 flows with bullet steps + summary table)
12. Build Open Questions table — one-line conversational questions; leave Answer/Date blank
13. Add empty Change & Request Log table (pre-populate the initial draft entry)
14. Add Reference Links
15. Append full Discovery → Delivery Checklist (Phases 1–8) — each with Goal line, feature-specific items, Required output
16. Show the complete draft for review
17. Ask if the user wants `.docx` files — if yes, run the generator. Options:

    ```bash
    # Build all registered features
    python scripts/office/generate_owr_docs.py --out-dir <path>

    # Build a specific feature only (preferred when only one doc changed)
    python scripts/office/generate_owr_docs.py --out-dir <path> --feature <id>

    # Build multiple specific features
    python scripts/office/generate_owr_docs.py --out-dir <path> -f <id1> -f <id2>
    ```

    The script produces one fully-styled `.docx` per feature with ABI brand colours, dark banner header, all Section 2 subsections, and the Phase 1–8 checklist.

18. **Registering a new feature** — when a new ADO feature needs a `.docx`, add it to `generate_owr_docs.py`:
    - Write `_build_<id>(doc: Document) -> None` following the existing pattern.
    - Add a 3-tuple to `DOCS`: `("<id>", "<id>-<kebab-title>-owr.docx", _build_<id>)`.
    - The `--feature` / `-f` flag uses the first element of each tuple as the lookup key.
    - Unknown IDs exit with code 1 and list valid options.
