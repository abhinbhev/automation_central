---
applyTo: "scripts/ado/**"
---

# ADO Script Standards

- Use the `azure-devops` Python SDK (`from azure.devops.connection import Connection`)
- Authenticate via PAT stored in `ADO_PAT` environment variable
- Organization URL from `ADO_ORG_URL` environment variable
- Always handle `AzureDevOpsServiceError` exceptions
- Work item fields use camelCase keys as per ADO REST API (e.g., `System.Title`, `System.Description`)
- When creating work items, always set: Title, Description, Acceptance Criteria (`Microsoft.VSTS.Common.AcceptanceCriteria`), Area Path, Iteration Path
- Use `JsonPatchOperation` from `azure.devops.v7_1.work_item_tracking.models` for patch operations
