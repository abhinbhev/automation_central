---
name: automation-central-board
description: Connect the ADO CLI to the Automation Central board — sets org, project, and team defaults so all subsequent ADO commands target this repo's own board.
domain: ado
requires_script: false
---

## Usage

Invoke with `/automation-central-board` when you need to target the Automation Central ADO board. No inputs required — all connection details are hardcoded for this board.

Use this at the start of any session where you are about to query, create, or update work items on the Automation Central backlog, especially after working on a different project.

## Output

ADO CLI defaults set to:

| Setting | Value |
|---------|-------|
| Organization | `https://dev.azure.com/ab-inbev-analytics` |
| Project | `GHQ_Commercial_Strategy_And_Insights_Analytics` |
| Team | `Automation Central` |

Followed by a confirmation query showing the team details and current backlog item count.

## Steps

1. Run:
   ```bash
   az devops configure --defaults \
     organization=https://dev.azure.com/ab-inbev-analytics \
     project=GHQ_Commercial_Strategy_And_Insights_Analytics
   ```
2. Verify the team exists:
   ```bash
   az devops team show --team "Automation Central" \
     --project GHQ_Commercial_Strategy_And_Insights_Analytics
   ```
3. Run a quick sanity query to confirm connectivity:
   ```bash
   az boards query \
     --wiql "SELECT [System.Id],[System.Title],[System.WorkItemType],[System.State] FROM WorkItems WHERE [System.AreaPath] UNDER 'GHQ_Commercial_Strategy_And_Insights_Analytics\Automation Central' ORDER BY [System.ChangedDate] DESC" \
     --project GHQ_Commercial_Strategy_And_Insights_Analytics
   ```
4. Report: team ID, description, and a summary table of current work items on the board.
