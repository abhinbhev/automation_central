---
name: create-work-items
description: Create ADO work items (Epic / Feature / User Story / Task / Bug) from freetext, meeting notes, or a spec. Handles single items or bulk hierarchy creation.
domain: ado
requires_script: true
script: scripts/ado/create_work_items.py
---

## Usage

Invoke with `/create-work-items` then provide:
- A description, meeting notes, or a spec to parse
- OR a direct statement like "create a story for X with acceptance criteria Y"
- Optionally: work item type, priority, area path, iteration path

If type is not specified, infer it:
- Strategic objective → **Epic**
- User-facing capability or deliverable → **Feature** or **User Story**
- Technical sub-task → **Task**
- Defect or regression → **Bug**

## Output

A structured preview of all work items to be created:

```
Type: User Story
Title: As a data engineer, I want automated schema validation so that pipelines fail fast on bad data
Description: ...
Acceptance Criteria:
  - Schema mismatches surface an error within 5 seconds of ingestion start
  - Error message includes field name and expected vs actual type
  - Validated schemas are cached to avoid re-processing
Priority: 2 (High)
Area Path: [TBD — ask user]
Iteration Path: [TBD — ask user]
Parent: [link to Feature if provided]
```

Always show the full preview and ask for confirmation before creating.

## Steps

1. Parse the input for distinct work units (one item per logical deliverable)
2. Infer type, suggest title (imperative or "As a..." format for stories)
3. Draft description and acceptance criteria — be specific and testable
4. Propose parent-child hierarchy if multiple items were extracted
5. Ask for: Area Path, Iteration Path, and any missing fields
6. Show the full structured preview
7. On confirmation: call `scripts/ado/create_work_items.py` or the ADO MCP tool to create

## Required Fields (never skip)

| Field | Notes |
|---|---|
| Title | Concise, action-oriented |
| Description | What and why, 2-5 sentences |
| Acceptance Criteria | Numbered, testable conditions |
| Type | Epic / Feature / User Story / Task / Bug |
| Priority | 1=Critical, 2=High, 3=Medium, 4=Low |
| Area Path | Ask if unknown |
| Iteration Path | Ask if unknown; use "current sprint" as fallback label |

## Bulk Mode

If input contains multiple logical items (e.g., meeting notes with 5 action items), create all of them in one pass. Present as a table before creating:

| # | Type | Title | Priority | Parent |
|---|------|-------|----------|--------|
| 1 | Story | ... | 2 | Feature X |
| 2 | Task | ... | 3 | Story 1 |
