# automation_central — Project Instructions

You are assisting a cross-functional engineering team at ABI. This repo is the team's central hub for AI agents, skills, scripts, and templates.

> **Before doing anything beyond a trivial answer, read [`INSTRUCTIONS.md`](../INSTRUCTIONS.md) at the repo root.** It is the canonical operating guide for this repo: wirings between skills/agents/prompts/scripts, file contracts, validators, standard workflows, and the pre-PR checklist. If anything below conflicts with `INSTRUCTIONS.md`, that file wins.

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
- `.github/agents/` — Copilot-side agent modes (paired with `.claude/agents/`)
- `.github/skills/` — Copilot skill definitions (SKILL.md format, `/skill-name` slash commands)
- `.github/instructions/` — scoped coding standards (Python, ADO, Terraform) auto-injected by Copilot
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

Run `/update-catalog` to see the latest list, or check `docs/automation-catalog.md`.

Quick reference for frequently used skills:
- `/meeting-minutes` — notes or transcript → structured minutes
- `/email-draft` — draft a stakeholder email
- `/pr-description` — git diff → PR body
- `/commit-message` — staged diff → conventional commit message
- `/ppt-from-outline` — outline → HTML presentation
- `/excel-report` — description → formatted `.xlsx`
- `/create-work-items` — freetext → ADO work items
- `/code-review` — diff → SCM checklist review
- `/plan-task` — feature description → subtasks
- `/write-readme` — codebase path → complete README
- `/write-adr` — decision description → ADR
- `/write-runbook` — service description → operational runbook
- `/write-api-docs` — source code / OpenAPI spec → API reference
- `/add-skill` — create + validate + register a new skill
- `/add-agent` — scaffold both `.agent.md` files, validate, update catalog
- `/new-skill` — scaffold a SKILL.md stub

