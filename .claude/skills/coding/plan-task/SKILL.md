---
name: plan-task
description: Break a feature or bug into subtasks with acceptance criteria; optionally create ADO work items
domain: coding
requires_script: false
---

## Usage

Invoke with `/plan-task` then provide:
- The feature request, bug description, or vague ask
- Context: affected system, constraints, tech stack (if not obvious from the repo)
- Whether to create ADO work items after planning (yes/no)

## Output

A work breakdown structure:

```
Epic: [Name]  (if new strategic work)
  Feature: [Name]
    Story: [User-facing title]
      Type: User Story
      AC: Given [...] When [...] Then [...]
      Effort: S/M/L

    Task: [Technical title]
      Type: Task
      AC: Done when [specific, verifiable condition]
      Effort: S
      Depends on: [Story/Task name or "—"]
```

Followed by:
- Dependency order (what to work on first)
- Any identified spikes (unknowns that need research first)
- Offer to create ADO items if MCP is available

## Steps

1. Read the input and identify ambiguities
2. Ask 1-3 targeted clarifying questions if the scope is unclear
3. Decompose into the smallest independently-testable units
4. Assign type, acceptance criteria, and effort to each
5. Identify dependencies and flag spikes
6. Present the plan for review
7. If confirmed and ADO MCP is available, create the items
