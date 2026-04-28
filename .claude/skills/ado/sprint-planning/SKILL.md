---
name: sprint-planning
description: Plan and populate an ADO sprint from the backlog. Balances capacity against story points, assigns items, and creates the sprint in ADO.
domain: ado
requires_script: false
---

## Usage

Invoke with `/sprint-planning` then provide:
- Sprint name / number and dates (start → end)
- Team name (or confirm the current team)
- Team capacity (hours or story points per person, or total)
- Any items you know must be in this sprint ("committed" items)

If you don't have capacity numbers, say so — the skill will ask.

## Output

A sprint plan table for review:

```
Sprint: Sprint 42  (12 May – 23 May 2025)
Capacity: 60 story points

| # | ID | Type | Title | Points | Assignee | Priority |
|---|---|---|---|---|---|---|
| 1 | #1042 | Story | Migrate auth service to Azure AD | 8 | @user1 | High |
| 2 | #1048 | Story | Add rate limiting to API gateway | 5 | @user2 | High |
| 3 | #1055 | Task | Update terraform for new VNet | 3 | @user3 | Medium |
...

Total: 58 / 60 points
Uncommitted (backlog): #1031, #1067 (overflow)
```

Then asks for confirmation before moving items into the sprint in ADO.

## Steps

1. Query the backlog for unassigned, ready items (ask for the ADO project/team if unknown)
2. Sort by priority, then by dependency order
3. Ask for team capacity if not provided
4. Fill the sprint greedily: committed items first, then priority order
5. Flag items with no estimate — ask for quick point assignment or exclude
6. Show the draft sprint plan table
7. Identify overflow items and call them out
8. On confirmation: assign items to the sprint iteration path in ADO

## Sprint Health Checks

Before confirming, surface any issues:
- Stories without acceptance criteria → block and flag
- Items with no estimate → warn, ask to assign or exclude
- Any item depending on an unplanned item → flag the dependency
- Over-capacity by more than 10% → warn explicitly

## Capacity Inputs

Accept any of these:
- `"60 story points total"`
- `"4 devs × 3 days available = roughly 12 points each"`
- `"3 backend engineers and 1 data engineer, each at 80% capacity"`
- If completely unknown: use previous sprint's velocity as a default and state that assumption

## Boundaries

- Never move items into a sprint without user confirmation
- Do not change item estimates — only read them
- If ADO MCP is unavailable, produce the plan as a Markdown table the user can copy
