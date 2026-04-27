# Naming Conventions

Consistent names make the catalog searchable and keep the repo predictable.

## Pattern

```
<domain>-<action>
```

| Part | Values | Examples |
|---|---|---|
| `domain` | `ado`, `office`, `devops`, `data-ml`, `infra`, `comms`, `coding`, `meta` | `ado`, `comms` |
| `action` | Verb-noun or noun phrase in kebab-case | `create-work-items`, `sprint-report`, `ppt-from-outline` |

## Files & Folders

| Type | Convention | Example |
|---|---|---|
| Skill folder | `<action>/` inside domain folder | `.claude/skills/ado/create-work-items/` |
| Skill file | always `SKILL.md` | `.claude/skills/ado/create-work-items/SKILL.md` |
| Agent file | `<domain>-<role>.agent.md` | `.claude/agents/ado-manager.agent.md` |
| Copilot prompt | `<domain>-<action>.prompt.md` | `.github/prompts/ado-create-work-item.prompt.md` |
| Copilot instructions | `<topic>.instructions.md` | `.github/instructions/python.instructions.md` |
| Python script | `<action>_<noun>.py` (snake_case) | `scripts/ado/create_work_items.py` |
| Template file | descriptive kebab-case | `templates/ppt/team-update.pptx` |

## Domains

| Domain | Covers |
|---|---|
| `ado` | Azure DevOps — work items, sprints, pipelines, PRs |
| `office` | PowerPoint, Word, Excel, non-tech doc outputs |
| `devops` | CI/CD, GitHub Actions, ADO Pipelines, git workflows |
| `data-ml` | Schemas, pipelines, model cards, experiment tracking |
| `infra` | Terraform, Bicep, cloud infra, architecture diagrams |
| `comms` | Teams, Outlook, meeting minutes, stakeholder updates |
| `coding` | Code review, test generation, task planning, SCM |
| `meta` | Repo self-maintenance — scaffold, validate, catalog |

## Do's and Don'ts

| Do | Don't |
|---|---|
| `create-work-items` | `CreateWorkItems`, `createworkitems`, `create_work_items` (folder) |
| `ado-manager.agent.md` | `ADOmanager.agent.md`, `manager.agent.md` |
| `sprint_report.py` | `SprintReport.py`, `sprintreport.py` |
| Use action verbs: `create`, `generate`, `draft`, `scaffold`, `validate` | Use vague names: `helper`, `tool`, `util` |
