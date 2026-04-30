---
name: plan-sprint
description: "Plan a sprint by pulling ready backlog items and matching them to team capacity"
mode: ask
---

Plan the next sprint from the available backlog.

If team capacity (person-days) or sprint duration is not provided, ask before proceeding.

**Sprint planning process:**
1. Query the backlog for items that are: unassigned to a sprint, `Ready` state, have estimates and acceptance criteria
2. Sort by: Priority (Critical first) → Dependencies → Estimate (smallest first to fill gaps)
3. Fill the sprint to ~80% of stated capacity — leave buffer for unplanned work
4. Flag any backlog items that are **not sprint-ready** (missing AC, no estimate, blocked dependency) — do not add these; list them separately

**Output format:**

```
## Sprint [N] — [Start Date] to [End Date]
**Total capacity:** X person-days | **Committed:** Y points/days | **Buffer:** Z

### Committed Items
| # | Title | Type | Priority | Estimate | Assignee |
|---|-------|------|----------|----------|----------|
| AB#123 | ... | Story | High | M | @name |

### Not Ready (excluded)
| AB# | Title | Blocker |
|-----|-------|---------|
| AB#456 | ... | Missing acceptance criteria |

### Risks & Notes
- ...
```

Confirm the plan with the user before assigning items to the sprint in ADO.
