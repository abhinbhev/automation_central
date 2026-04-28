---
name: word-doc
description: Generate Word documents from an outline or content — SOPs, ADRs, specs, project charters, RCAs, and reports. Uses team Word templates.
domain: office
requires_script: true
script: scripts/office/word_builder.py
---

## Usage

Invoke with `/word-doc` then provide:
- Document type (see supported types below)
- Title and content, or an outline to expand
- Audience: `team`, `management`, or `external`

## Supported Document Types

| Type | Use for |
|---|---|
| `sop` | Standard Operating Procedure — step-by-step process docs |
| `adr` | Architecture Decision Record — capturing a technical decision |
| `spec` | Technical spec or design doc |
| `rca` | Root Cause Analysis — incident post-mortem |
| `report` | Status report, project summary, or analysis report |
| `charter` | Project kickoff charter |
| `runbook` | Operational runbook for a service or process |

## Output

**Phase 1 — Document outline (always):**

A structured Markdown outline with all sections filled in, ready for review.

**Phase 2 — Word file (if script available):**

Runs `scripts/office/word_builder.py` to produce a `.docx` file using the template in `templates/word/`.

## Document Templates

### SOP Structure
```
1. Purpose
2. Scope
3. Roles and Responsibilities
4. Prerequisites
5. Procedure (numbered steps)
6. Verification
7. Troubleshooting
8. References
```

### ADR Structure
```
# ADR-NNN: [Title]
Status: Proposed | Accepted | Deprecated | Superseded
Date: YYYY-MM-DD

## Context
## Decision
## Consequences
## Alternatives Considered
```

### RCA Structure
```
## Incident Summary
## Timeline
## Root Cause
## Contributing Factors
## Impact
## Resolution
## Action Items (with owner + due date)
## Lessons Learned
```

### Spec Structure
```
## Overview
## Goals and Non-Goals
## Design
## Implementation Plan
## Testing Strategy
## Open Questions
```

## Steps

1. Identify document type from the input
2. Select the appropriate template structure
3. Populate each section from the provided content (expand thin sections with sensible defaults)
4. Produce the full Markdown outline for review
5. Ask if the user wants the `.docx` file generated
6. If yes: call `scripts/office/word_builder.py` with the document data as JSON
