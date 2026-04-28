---
name: excel-report
description: Generate formatted Excel reports and trackers from data input (CSV, JSON, table, or description). Produces .xlsx files with formatted tables, charts, and summary tabs.
domain: office
requires_script: true
script: scripts/office/excel_builder.py
---

## Usage

Invoke with `/excel-report` then provide:
- Report type (see supported types)
- Data to populate: paste a table, CSV, JSON, or describe the structure
- Report title and any branding/formatting notes

## Supported Report Types

| Type | Description |
|---|---|
| `sprint-tracker` | Sprint backlog with status, assignee, story points |
| `status-report` | Project/initiative status with RAG indicators |
| `data-summary` | Aggregated metrics table with charts |
| `budget-tracker` | Cost vs actuals with variance |
| `test-results` | Test run summary with pass/fail counts |
| `custom` | Freeform — describe the columns and structure |

## Output

**Phase 1 — Sheet plan (always):**

```
Sheet 1: Summary
  - KPI tiles: Total Items, Completed, In Progress, Blocked
  - Chart: Burndown by week

Sheet 2: Backlog
  - Columns: ID | Title | Type | Assignee | Status | Points | Sprint
  - Conditional formatting: Status (green=Done, amber=In Progress, red=Blocked)

Sheet 3: By Assignee
  - Pivot-style breakdown of items per person
```

**Phase 2 — Excel file (if script available):**

Runs `scripts/office/excel_builder.py` to produce a `.xlsx` file.

## Formatting Standards

- Header rows: bold, light blue fill (`#D9E1F2`), auto-filter enabled
- Conditional formatting for status columns: green / amber / red
- Frozen top row on every data sheet
- Summary sheet always first
- Column widths auto-fitted
- No merged cells (they break pivot tables)

## Steps

1. Identify report type from input
2. Plan the sheet structure (list sheets, columns, any charts)
3. Show the sheet plan for review
4. Ask for the data if not already provided
5. On confirmation: call `scripts/office/excel_builder.py` with the report spec as JSON
6. Return the output file path

## Data Input Formats

Accept any of:
- Pasted Markdown table
- CSV block
- JSON array of objects
- Natural language description ("4 sprints, 8 engineers, track story points per sprint")
