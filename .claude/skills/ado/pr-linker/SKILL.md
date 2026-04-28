---
name: pr-linker
description: Link GitHub PRs to ADO work items. Adds AB#ID tags to PR descriptions and sets the work item state to Active or In Review.
domain: ado
requires_script: false
---

## Usage

Invoke with `/pr-linker` then provide:
- PR URL or PR number + repo name
- ADO work item ID(s) to link (e.g., `#1042, #1048`)
- OR: describe what the PR does and the skill will suggest matching work items from the current sprint

## Output

An updated PR description with the `AB#<ID>` tag appended, and a confirmation that the ADO work item state was updated.

**Example PR description update:**
```
## Summary
Migrates authentication service to Azure AD using MSAL.

## Changes
- Replaced legacy auth module with `azure-identity`
- Updated environment variable names in all deployment configs

Closes AB#1042
```

**ADO state change:** `#1042 → In Review`

## Steps

1. Read the current PR description (via GitHub MCP or user paste)
2. Identify work item IDs from the input or suggest matches from the sprint backlog
3. Append `Closes AB#<ID>` (or `Related to AB#<ID>` if not a direct close) to the PR description
4. Update the PR description via GitHub MCP
5. Update the ADO work item state: `Active → In Review` (do not change if already `Closed`)
6. Confirm both operations succeeded

## Work Item State Mapping

| Scenario | ADO State |
|---|---|
| PR opened | In Review |
| PR merged | Closed |
| PR closed without merge | Active (revert if was In Review) |

## Matching Logic (when no ID provided)

If the user doesn't give an ID, look for:
1. Branch name containing an ID (e.g., `feature/1042-auth-migration`)
2. PR title keywords matching open sprint items
3. If ambiguous: show a shortlist and ask

## Boundaries

- Never close a work item unless the PR is actually merged
- Always confirm before modifying work item state
- If the PR already has `AB#` tags, show them and ask before adding more
