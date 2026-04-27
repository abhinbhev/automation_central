---
name: meeting-minutes
description: Convert transcript or bullet notes into structured meeting minutes
domain: comms
requires_script: false
---

## Usage

Invoke with `/meeting-minutes` then paste:
- Raw transcript text, OR
- Bullet-point notes, OR
- A list of discussion points

Optionally specify:
- Meeting title and date
- Attendees
- Meeting type (standup / planning / retrospective / stakeholder / ad-hoc)

## Output

A formatted meeting minutes document with:

```
# Meeting Minutes — [Title]
**Date:** [date]
**Attendees:** [names]

## Summary
[2-3 sentence overview]

## Discussion Points
[Each topic with key points raised]

## Decisions Made
[Numbered list of decisions]

## Action Items
| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | ...    | ...   | ... |

## Next Meeting
[Date / agenda if mentioned]
```

## Steps

1. Read the provided notes or transcript
2. Identify distinct discussion topics
3. Extract decisions (look for phrases like "we decided", "agreed to", "will proceed with")
4. Extract action items (look for names + verbs: "X will", "X to", "assigned to X")
5. Produce the formatted output above
6. If attendees or date are not in the input, ask or mark as `[TBD]`
