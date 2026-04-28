---
name: release-notes
description: Generate formatted release notes from closed ADO work items for a sprint, milestone, or date range.
domain: ado
requires_script: true
script: scripts/ado/release_notes.py
---

## Usage

Invoke with `/release-notes` then provide:
- Sprint name/number OR a date range (e.g., "2025-05-01 to 2025-05-23")
- Target audience: `internal` (engineers) or `stakeholder` (business/management)
- Version/release tag if applicable (e.g., `v2.4.0`)

## Output

### Stakeholder Format

```markdown
# Release Notes — Sprint 42 / v2.4.0
**Released:** 23 May 2025

## What's New
- **Auth service migrated to Azure AD** — users now sign in with their corporate credentials
- **API rate limiting** — prevents runaway requests, improves reliability for all teams

## Bug Fixes
- Fixed intermittent timeout in the data ingestion pipeline

## Coming Up
- Real-time alerting dashboard (Sprint 43)
```

### Internal / Engineering Format

```markdown
# Release Notes — Sprint 42
**Items closed:** 14  |  **Story points delivered:** 58

## Features & Stories
| ID | Title | Type | Points |
|---|---|---|---|
| #1042 | Migrate auth service to Azure AD | Story | 8 |

## Bugs Fixed
| ID | Title | Severity |
|---|---|---|
| #1031 | Ingestion pipeline timeout | 2 |

## Technical Changes
- Upgraded `azure-identity` to 1.16.0
- Deprecated `legacy_auth` module (removal in Sprint 45)
```

## Steps

1. Query ADO for closed items in the given sprint/date range
2. Separate items by type: Feature, Story, Bug, Task
3. Filter out internal tasks (type=Task) from stakeholder format — include only Stories, Features, Bugs
4. For each feature/story: write a one-line plain-language description (no jargon for stakeholder format)
5. For internal format: include IDs, types, and story points
6. Add a "Coming Up" section if next sprint items are visible
7. Output the formatted notes
8. Offer to save as a `.md` file or post to SharePoint/Confluence

## Audience Tone

| Audience | Tone |
|---|---|
| `stakeholder` | Plain language, user impact focus, no IDs/points |
| `internal` | Technical, include IDs, points, upgrade notes |
