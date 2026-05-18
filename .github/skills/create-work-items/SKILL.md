---
name: create-work-items
description: "Create ADO work items from a description, meeting notes, or spec"
mode: ask
---

Create Azure DevOps work items from the following description.

Parse the input for distinct work units. For each item, determine:
- Work item type (Epic / Feature / User Story / Task / Bug)
- Title
- Description
- Acceptance criteria (numbered, testable)
- Priority (1=Critical, 2=High, 3=Medium, 4=Low)
- Area Path and Iteration Path (if known)
- Parent-child relationships if multiple items

Show a structured preview table of all items before creating. Ask the user for any missing required fields.
Offer to create them via the ADO MCP tool if available.
For features, create description with a clear problem statemen and gherkin style acceptance criteria. For user stories, follow the "As a [user], I want [feature] so that [benefit]" format in the title and description. For tasks, focus on the specific action to be taken. For bugs, include steps to reproduce and expected vs actual results.
For tasks, the estimates should be in hours and should be added in both current estimate and remaining work fields.
For user story, 1 story point should be equivalent to 6 hours of work, and the story points should be added in the "Story Points" field, with a round up.  
