---
mode: ask
description: Break a feature, epic, or vague requirement into an estimable, implementable backlog
---

Decompose the following feature or requirement into a structured backlog.

Ask for clarification only when inputs/outputs, scope boundaries, or personas are genuinely unclear.

**Output format for each item:**

```
## Feature: [Name]
**Estimate:** S / M / L / XL
**Priority:** Critical / High / Medium / Low
**Dependencies:** [none | list items]

### User Stories
1. **As a [persona], I want [thing] so that [outcome]**
   - AC 1: [testable condition]
   - AC 2: [testable condition]
   - Estimate: S

### Technical Tasks
1. [Task title]
   - What: ...
   - Definition of Done: ...
   - Estimate: S
```

**Decomposition rules:**
- Stories must be independently shippable (INVEST principle)
- Tasks completable in 1–3 days; split anything larger
- Acceptance criteria must be testable — no "works correctly" or "performs well"
- Every story needs at least 2 acceptance criteria
- Infrastructure, config, and refactor work → Tasks (not Stories)

**After decomposing:**
- Summarise total estimated scope
- List open risks or blocking questions
- Ask if the user wants to create these as ADO work items (offer to invoke `ado-manager`)
- Ask if the user wants a test plan generated (offer to invoke `tester`)
