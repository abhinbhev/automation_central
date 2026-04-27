---
mode: ask
description: Create an ADO work item from a description
---

Create an Azure DevOps work item from the following description.

Ask the user for any missing details:
- Work item type (Epic / Feature / User Story / Task / Bug)
- Title
- Description
- Acceptance criteria
- Priority (1=Critical, 2=High, 3=Medium, 4=Low)
- Area Path and Iteration Path (if known)

Output a JSON object matching the ADO work item schema, then offer to create it via the ADO MCP tool if available.
