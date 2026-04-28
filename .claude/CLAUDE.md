# automation_central — Project Instructions

You are assisting a cross-functional engineering team at ABI. This repo is the team's central hub for AI agents, skills, scripts, and templates.

## Team Context

- **Project management:** Azure DevOps (ADO) — all work items, sprints, pipelines
- **Communication:** Microsoft Teams, Outlook
- **Docs:** Confluence, SharePoint, OneDrive, Microsoft Loop
- **Code:** GitHub (primary), ADO Repos
- **Cloud:** Azure
- **Primary languages:** Python 3.11, SQL, Terraform/Bicep, YAML, PowerShell

## How This Repo is Structured

- `.claude/skills/` — skills you can invoke with `/skill-name`
- `.claude/agents/` — specialized agent modes
- `scripts/` — Python scripts called by skills when execution is needed
- `templates/` — PowerPoint, Word, Excel, ADO, IaC templates
- `configs/` — MCP server configs, conda environment
- `docs/` — ADRs, runbooks, and API docs (output from doc-writer agent)

## Standards for Any Output

- Code: snake_case (Python), kebab-case (folders/files), typed function signatures, no hardcoded secrets
- Documents: clear headings, bullet points, no corporate filler
- ADO work items: always include Title, Description, Acceptance Criteria, Type, and Priority
- Never commit secrets or credentials
- Ask before sending messages or emails on behalf of the user

## Available MCP Tools (when configured)

- `azure-devops` — create/update/query work items, sprints, boards
- `github` — read PRs, issues, diffs, repo contents
- `ms-graph` — Outlook, SharePoint, OneDrive, Teams

## Skills Available

Run `/update-catalog` to see the latest list, or check the README.md#automation-catalog section.

Quick reference for the most-used skills:
- `/meeting-minutes` — notes or transcript → structured minutes
- `/email-draft` — draft a stakeholder email
- `/pr-description` — git diff → PR body
- `/ppt-from-outline` — outline → PowerPoint plan + file
- `/create-work-items` — freetext → ADO work items
- `/code-review` — diff → SCM checklist review
- `/plan-task` — feature description → subtasks
- `/new-skill` — scaffold a new skill

