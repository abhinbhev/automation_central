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
