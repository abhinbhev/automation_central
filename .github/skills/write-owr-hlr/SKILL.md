---
name: write-owr-hlr
description: "Generate an OWR (One Way Report) + HLR (High-Level Requirements) product document — the standard ABI template covering feature objectives, scope, assumptions, open questions, and the full 8-phase discovery-to-delivery checklist"
mode: agent
---

Generate an OWR + HLR product document using the standard ABI template.

## Inputs to collect

Before writing, ask for any missing items:
- **Feature / product name**
- **Country / scope** — which market(s) this covers
- **Target date** — go-live or milestone
- **Team members** — all contributors
- **Objective** — 2–4 bullet points describing what is being built and why
- **ADO link** (optional) — backlog or feature board URL
- **Success metrics** — adoption, engagement, outcome, and business impact KPIs
- **Assumptions** — brands, regions, channels, periods, granularity, known data constraints
- **Out-of-scope items**
- **Open questions**

## Document structure

Produce the document in this order:

### Metadata table
| Field | Value |
|---|---|
| Target date | |
| Document status | DRAFT |
| Team members | |
| Design link | |
| ADO link | |

### Feature sections (use `/` prefix headings as in the template)

- `/Objective` — what the feature does and why (bullets, no prose filler)
- `/Success Metrics` — grouped as Adoption / Engagement / Outcome / Business Impact; include a Goal → Metric table
- `/Assumptions` — features in scope, technical approach, data scope (brands, regions, channels, periods, granularity)
- `/Milestones` — ADO link and timeline dates
- `/Requirements` — pre-reqs, business rules, constraints
- `/Out of Scope` — short-term and long-term exclusions
- `/Design` — artefact links and tentative timeline
- `/Open Questions` — table: Question | Answer | Date Answered
- `Change & Request Log` — table: Request/Update Description | Requestor / Involved Personnel | Date
- `/Reference Links`

### Discovery → Delivery Checklist (append after the feature body)

Generate all 8 phases with their checklist items and required outputs:

**Phase 1 — Discovery Framing & Alignment**
Checklist: capability identified, user role/moment defined, problem statement written, business objective aligned, decision owner defined, feature usage context agreed
Output: Problem Statement, Business Objective, Decision & Owner Definition

**Phase 2 — Business Rules & Data Contract**
Checklist: all metrics defined, delta/index logic documented, time logic defined, audience rules documented, business interpretation rules written, edge cases defined, data dependencies validated, known gaps agreed
Output: Metric Definitions Document, Business Rules Section, Data Assumptions & Risks
🚫 If this phase is not closed → do not move to design

**Phase 3 — Discovery Validation (Users)**
Checklist: hypotheses documented, user interviews conducted, frictions identified, mental model validated, evidence collected
Output: Discovery Summary, Validated/Invalidated Hypotheses, UX Risks to Address

**Phase 4 — HLR (High-Level Requirements)**
Checklist: MVP scope defined, key user questions listed, key actions enabled, dependencies listed, non-goals documented
Output: HLR Document (user goals, business rules, required capabilities, out-of-scope items)

**Phase 5 — Design Handoff & Prototype Validation**
Checklist: design brief shared, prototype reviewed against business rules, metric hierarchy validated, drill-down paths validated, navigation paths validated, labels aligned with definitions
Output: Approved Prototype, Design Decisions Logged, Open Questions

**Phase 6 — Delivery Prep (User Stories & Walkthrough)**
Checklist: user stories written per user intent, acceptance criteria defined, business rules referenced, empty/error states specified, tooltips defined, event mapping done, engineering walkthrough completed, technical risks acknowledged
Output: Engineering-ready User Stories, Walkthrough Notes, Scope Lock (MVP)

**Phase 7 — Release & Communication**
Checklist: release note written, known limitations documented, stakeholders informed, enablement material shared
Output: Release Notes, Feature Announcement

**Phase 8 — Post-Release Validation & Learning**
Checklist: success metrics tracked, adoption signals monitored, user feedback collected, business outcome reviewed, gaps identified, v2 decision made
Output: Post-Release Review, Success Criteria Validation

## Output standards

- Use H1 for top-level document title, H2 for main sections, H3 for subsections
- Bullets over prose — every line adds information
- Leave table cells blank (not "TBD") where information is not yet provided
- Set document status to `DRAFT` unless specified otherwise

Once the outline is confirmed by the user, offer to generate `.docx` files by running the dedicated OWR script:

```bash
python scripts/office/generate_owr_docs.py
# or specify a custom output folder:
python scripts/office/generate_owr_docs.py --out-dir docs/word
```

The script reads the source markdown docs from `docs/` and produces one styled `.docx` per feature, with ABI brand colours, dark banner header, metadata table, all Section 2 subsections, and the full Section 3 Discovery → Delivery Checklist. Output defaults to `docs/`.
