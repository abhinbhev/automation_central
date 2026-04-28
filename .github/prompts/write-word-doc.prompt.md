---
mode: agent
description: Generate a Word document (SOP, ADR, RCA, spec, runbook) from a description or outline
---

Generate a Word document from the following description or outline.

First, identify the document type:
- **SOP** — Standard Operating Procedure
- **ADR** — Architecture Decision Record
- **RCA** — Root Cause Analysis
- **Spec** — Feature or technical design specification
- **Runbook** — Operational runbook for a service or incident type
- **Charter** — Project charter

Then produce a full Markdown outline of the document with all sections populated. Show it for review and ask for any missing sections or corrections before building.

**Document standards:**
- Clear headings (H1 title, H2 sections, H3 subsections)
- Bullet points over prose where possible
- No corporate filler — every sentence adds information
- Dates, owners, and version numbers on every document

**Section templates by type:**

*ADR:* Status | Context | Decision | Consequences | Alternatives Considered
*RCA:* Incident Summary | Timeline | Root Cause | Contributing Factors | Action Items | Prevention
*SOP:* Purpose | Scope | Roles | Prerequisites | Procedure (numbered steps) | Rollback | References
*Spec:* Overview | Goals & Non-Goals | Design | API / Interface | Data Model | Dependencies | Open Questions
*Runbook:* Service Overview | Alert/Trigger | Diagnosis Steps | Remediation | Escalation | Post-Incident

Once the outline is confirmed, run `scripts/office/word_builder.py` with the appropriate template to produce the `.docx` file.
