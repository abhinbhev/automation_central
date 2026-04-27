# automation_central — Build Progress

## What This Repo Is

Central hub for the ABI engineering team's AI-assisted agents, skills, scripts, and templates.
Supports both **Claude Code** and **GitHub Copilot** as AI frameworks, with shared Python scripts and templates underneath.

**Team scope:** Software/Backend, Platform/Infra, ML/AI, Data/Analytics, non-tech outputs (decks, docs, Excel)
**MCP:** Local per-dev now; centralized path documented for the future

---

## Status: Foundation Complete

### Done

| Area | Files | Notes |
|---|---|---|
| Repo structure | All folders created | See tree below |
| `.claude/CLAUDE.md` | ✅ | Project instructions for Claude Code |
| `.github/copilot-instructions.md` | ✅ | Team base context for Copilot |
| **Agents (Claude Code)** | 6 × `.agent.md` | planner, coder, code-reviewer, tester, ado-manager, office-writer |
| **Agents (Copilot)** | Folder ready | Stubs to be written — use existing `.claude/agents/` as reference |
| **First-wave skills** | 4 × `SKILL.md` | meeting-minutes, email-draft, pr-description, ppt-from-outline |
| **Coding skills** | 3 × `SKILL.md` | plan-task, code-review, write-tests |
| **Meta skills** | 4 × `SKILL.md` | new-skill, new-agent, validate-skill, update-catalog |
| **Copilot prompts** | 6 × `.prompt.md` | create-work-item, ppt-from-outline, pr-description, release-notes, code-review, write-tests |
| **Copilot instructions** | 3 × `.instructions.md` | python, ado, terraform |
| PR template | ✅ | `.github/pull_request_template.md` |
| `scripts/repo/` | 3 scripts | validate_skill.py, validate_agent.py, generate_catalog.py |
| `scripts/shared/` | 2 scripts | auth.py (ADO/GitHub/MSGraph), utils.py |
| `scripts/git/` | 1 script | pr_description.py |
| `configs/mcp/local/` | ✅ | Full setup guide + mcp-settings.template.json |
| `configs/mcp/remote/` | ✅ | Future centralized setup documented |
| `configs/envs/conda-env.yml` | ✅ | All Python dependencies |
| `docs/` | 6 docs | README, onboarding, contributing, naming-conventions, mcp-setup, automation-catalog |
| `.vscode/` | ✅ | settings.json + extensions.json |
| `.gitignore` | ✅ | |

---

### Placeholder Skill Folders (SKILL.md not yet written)

These folders exist — SKILL.md needs to be added. Use `/new-skill` in Claude Code to scaffold each one.

| Domain | Skills Remaining |
|---|---|
| `ado` | create-work-items, sprint-planning, release-notes, pr-linker |
| `office` | word-doc, excel-report |
| `comms` | teams-announcement |
| `devops` | gh-actions-workflow, ado-pipeline-yaml |
| `data-ml` | pipeline-docs, schema-docs, model-card |
| `infra` | terraform-module, arch-diagram, incident-runbook |

### Python Scripts Not Yet Written

| Script | Purpose |
|---|---|
| `scripts/ado/create_work_items.py` | ADO REST API: create Epic/Feature/Story/Task |
| `scripts/ado/sprint_report.py` | Fetch sprint data → report |
| `scripts/ado/release_notes.py` | Build release notes from work items |
| `scripts/office/ppt_builder.py` | python-pptx: populate slide deck from JSON plan |
| `scripts/office/word_builder.py` | python-docx: fill Word templates |
| `scripts/office/excel_builder.py` | openpyxl: generate/update spreadsheets |
| `scripts/data/schema_documenter.py` | Introspect DB/CSV schema → markdown |
| `scripts/data/pipeline_documenter.py` | Parse DAG/pipeline config → docs |

### Copilot Agent Files Not Yet Written

Folder: `.github/agents/`
Agents to mirror from `.claude/agents/`: ado-manager, office-writer, devops-engineer, planner, coder, tester, code-reviewer

### Templates Not Yet Added

Folder: `templates/`
- `ppt/team-update.pptx`, `ppt/project-kickoff.pptx`
- `word/sop.docx`, `word/adr.docx`, `word/rca.docx`
- `excel/sprint-tracker.xlsx`
- `iac/terraform-module/` starter files
- `iac/gh-actions/` reusable workflow YAMLs

---

## Getting Started (for new team members)

```bash
# 1. Clone and open workspace
git clone <repo-url>
code automation_central

# 2. Set up Python env
conda env create -f configs/envs/conda-env.yml
conda activate automation-central

# 3. Set up MCP servers
# → Follow configs/mcp/local/README.md

# 4. Test a skill in Claude Code
# Type /meeting-minutes and paste some bullet-point notes
```

---

## Key Commands

```bash
# Validate a skill before PRing
python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>

# Validate an agent file
python scripts/repo/validate_agent.py .claude/agents/<name>.agent.md

# Rebuild the automation catalog
python scripts/repo/generate_catalog.py

# Generate a PR description from current branch
python scripts/git/pr_description.py --base main
```

---

## Contribution Workflow

```
1. Branch:   git checkout -b skill/<name>
2. Scaffold: /new-skill  (Claude Code)
3. Write:    fill in SKILL.md
4. Validate: python scripts/repo/validate_skill.py <path>
5. Catalog:  python scripts/repo/generate_catalog.py
6. PR:       fill in .github/pull_request_template.md
7. Review:   1 reviewer minimum
```

---

## Architecture Decisions

| Decision | Choice | Reason |
|---|---|---|
| AI frameworks | Both Claude Code + GitHub Copilot | Whole team uses VS Code; some use Claude Code, some Copilot |
| Skills location | `.claude/skills/<domain>/<name>/SKILL.md` | Claude Code standard; domain grouping keeps catalog navigable |
| Copilot equivalent | `.github/prompts/*.prompt.md` | Copilot has no native "skills" — prompts are the closest equivalent |
| Scripts | Python in `scripts/` | Framework-agnostic; called by skills when execution > text output |
| MCP strategy | Local first, remote path documented | No shared server yet; designed for easy migration |
| Catalog | Auto-generated via `generate_catalog.py` | Prevents catalog drift as skills accumulate |
| Contribution | Open PR, light review, validator gate | Low friction; `validate_skill.py` catches structural issues automatically |
