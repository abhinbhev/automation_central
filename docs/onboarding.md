# Onboarding

Get from zero to productive in under 30 minutes.

## Prerequisites

- VS Code with either Claude Code or GitHub Copilot extension
- Git
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda

## Step 1 — Clone the repo

```bash
git clone <repo-url>
cd automation_central
```

Open the folder in VS Code. When prompted, click **Open Workspace** — this activates the `.vscode/settings.json` configuration.

## Step 2 — Install recommended extensions

VS Code will show a toast notification. Click **Install All**, or:

1. Open the Command Palette (`Ctrl+Shift+P`)
2. Run **Extensions: Show Recommended Extensions**
3. Install everything in the Workspace Recommendations list

## Step 3 — Set up the Python environment

```bash
conda env create -f configs/envs/conda-env.yml
conda activate automation-central
```

Verify:
```bash
python -c "import azure.devops, pptx, docx, openpyxl; print('OK')"
```

## Step 4 — Configure MCP servers

MCP servers give Claude Code (and other tools) live access to ADO, GitHub, Teams, and Outlook.

Follow the guide: [configs/mcp/local/README.md](../configs/mcp/local/README.md)

## Step 5 — Test a skill (Claude Code)

1. Open any file or a blank editor tab
2. Invoke the Claude Code chat
3. Type `/meeting-minutes` and paste in some bullet-point notes
4. Claude should return a formatted meeting minutes doc

## Step 6 — Test a prompt (GitHub Copilot)

1. Open Copilot Chat (`Ctrl+Alt+I`)
2. Type `@workspace /create-work-item` followed by a task description
3. Copilot should return a structured work item JSON

## You're set up

Browse the [automation catalog](automation-catalog.md) to see everything available.

Want to add your own automation? Read [contributing.md](contributing.md).
