---
mode: agent
description: Build a formatted Excel report, tracker, or dashboard from a description or data
---

Build an Excel report or tracker from the following description or data.

First, identify the report type and define the sheet structure. Common types:
- **Sprint tracker** — stories, status, owner, estimate, actuals
- **Status dashboard** — RAG status per workstream, updated weekly
- **Data summary** — tabular data with aggregations and charts
- **Capacity planner** — team members, availability, allocation per sprint
- **Incident log** — date, severity, service, duration, resolution, action items

Show a sheet plan before building:
```
Sheet: [Name]
Columns: [col1 (type)], [col2 (type)], ...
Conditional formatting: [column] — green/amber/red based on [rule]
Freeze: header row
Filter: all columns
```

**Excel standards (always apply):**
- Freeze the header row on every sheet
- Auto-filter enabled on all data sheets
- Status columns use RAG colour coding (green = on track, amber = at risk, red = blocked/overdue)
- No merged cells — use centre-across-selection if visual grouping is needed
- Number and date formats explicit (not General)
- Separate raw data sheets from summary/dashboard sheets

Wait for user confirmation of the sheet plan, then run `scripts/office/excel_builder.py` to generate the `.xlsx` file.
