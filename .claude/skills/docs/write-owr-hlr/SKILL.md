---
name: write-owr-hlr
description: Generate an OWR (One Way Report) + HLR (High-Level Requirements) product document — the standard ABI template for capturing feature objectives, scope, assumptions, open questions, and the full discovery-to-delivery checklist
domain: docs
requires_script: true
script: scripts/office/generate_owr_docs.py
---

## Usage

Invoke with `/write-owr-hlr` then provide:
- **Feature / product name** — e.g. `WatchTower Integration into OneWay`
- **Country / scope** — which market(s) this covers
- **Target date** — desired go-live or milestone date
- **Team members** — names of all contributors
- **Objective** — 2–4 bullet points describing what is being built and why
- **ADO link** (optional) — backlog or feature URL

Optionally provide:
- **Success metrics** — adoption, engagement, outcome, and business impact KPIs
- **Assumptions** — brands, regions, channels, periods, granularity, and known data constraints
- **Out-of-scope items** — what is explicitly excluded
- **Open questions** — any unresolved items

## Output

A complete OWR + HLR document with all sections populated, structured as follows:

**Section 1 — Product brief (metadata table)**
- Target date, document status, team members, quick links (design file, ADO backlog)

**Section 2 — Feature body**
- `/Objective` — what the feature does and why
- `/Success Metrics` — adoption, engagement, outcome, and business impact KPIs with a Goal → Metric table
- `/Assumptions` — features in scope, technical approach, data scope (brands, regions, channels, periods, granularity)
- `/Milestones` — ADO link and key timeline dates
- `/Requirements` — feature pre-reqs, business rules, and constraints
- `/Out of Scope` — explicitly excluded items (short-term and long-term)
- `/Design` — design artefact links and tentative timeline
- `/Open Questions` — table with Question / Answer / Date Answered columns
- `Change & Request Log` — table with Request/Update, Requestor/Personnel, Date columns
- `/Reference Links` — related docs, tickets, Confluence pages

**Section 3 — Discovery → Delivery Checklist (8 phases)**

| Phase | Goal |
|---|---|
| 1 — Discovery Framing & Alignment | Problem, scope, business intent, ownership clear before solutioning |
| 2 — Business Rules & Data Contract | Metrics, delta logic, time logic, audience rules, edge cases locked before design |
| 3 — Discovery Validation (Users) | Hypotheses validated with real users; frictions and mental model confirmed |
| 4 — HLR (High-Level Requirements) | MVP scope, key user questions, required actions, dependencies, non-goals |
| 5 — Design Handoff & Prototype Validation | Design solves the right problem; prototype reviewed against business rules |
| 6 — Delivery Prep (User Stories & Walkthrough) | Engineering-ready stories with AC, business rules, empty/error states, event mapping |
| 7 — Release & Communication | Release note, known limitations, stakeholder comms, enablement material |
| 8 — Post-Release Validation & Learning | Success metrics tracked, adoption signals monitored, v2 decision made |

Each phase lists its checklist items and required output artefacts.

## Steps

1. Collect all required inputs — ask for any that are missing before drafting
2. Set document status to `DRAFT` unless the user specifies otherwise
3. Populate the metadata table (target date, status, team, quick links)
4. Write the Objective section — bullet points, no fluff
5. Build the Success Metrics section: group KPIs into Adoption / Engagement / Outcome / Business Impact; include a two-column Goal → Metric table
6. Write the Assumptions section: features in scope (bulleted list), technical approach, and data scope table (brands, regions, channels, periods, granularity)
7. Add Milestones section with the ADO backlog link and any timeline dates provided
8. Write Requirements section — list feature pre-reqs, business rules, and data constraints
9. Write Out of Scope — separate short-term and long-term exclusions
10. Write Design section — paste any provided links; note WIP artefacts and tentative design review dates
11. Build the Open Questions table (Question / Answer / Date Answered) — populate with any known open items; leave Answer and Date blank for unresolved items
12. Add an empty Change & Request Log table
13. Add Reference Links section
14. Append the full Discovery → Delivery Checklist (Phases 1–8), each with its checklist items and required output artefacts
15. Show the complete draft for review
16. Ask if the user wants `.docx` files — if yes, run `scripts/office/generate_owr_docs.py` (optionally with `--out-dir <path>`). The script produces one fully-styled `.docx` per OWR doc with ABI brand colours, banner header, all Section 2 subsections, and the Phase 1–8 checklist. Output defaults to `docs/`.
