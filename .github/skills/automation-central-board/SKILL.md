---
name: automation-central-board
description: "Connect the ADO CLI to the Automation Central board — sets org, project, and team defaults so all subsequent ADO commands target this repo's own board."
mode: agent
---

When invoked, connect to the Automation Central ADO board by running the following steps:

1. Set ADO CLI defaults:
   - Organization: `https://dev.azure.com/ab-inbev-analytics`
   - Project: `GHQ_Commercial_Strategy_And_Insights_Analytics`

   ```bash
   az devops configure --defaults organization=https://dev.azure.com/ab-inbev-analytics project=GHQ_Commercial_Strategy_And_Insights_Analytics
   ```

2. Verify the team exists:
   ```bash
   az devops team show --team "Automation Central" --project GHQ_Commercial_Strategy_And_Insights_Analytics
   ```

3. Run a confirmation query against the board:
   ```bash
   az boards query --wiql "SELECT [System.Id],[System.Title],[System.WorkItemType],[System.State] FROM WorkItems WHERE [System.AreaPath] UNDER 'GHQ_Commercial_Strategy_And_Insights_Analytics\Automation Central' ORDER BY [System.ChangedDate] DESC" --project GHQ_Commercial_Strategy_And_Insights_Analytics
   ```

4. Report the team ID, description, and a summary table of current work items.

No inputs are required. All connection details are fixed for this board. Use this skill at the start of any session before querying or creating Automation Central work items.
