# automation_central — Build Progress

## What This Repo Is

Central hub for the ABI engineering team's AI-assisted agents, skills, scripts, and templates.
Supports both **Claude Code** and **GitHub Copilot** as AI frameworks, with shared Python scripts and templates underneath.

**Team scope:** Software/Backend, Platform/Infra, ML/AI, Data/Analytics, non-tech outputs (decks, docs, Excel)
**MCP:** Local per-dev now; centralized path documented for the future

---

## Status: Skills + Scripts + Agents Complete — Audit Passed

### Done — Foundation (Phase 0)

| Area | Files | Notes |
|---|---|---|
| Repo structure | All folders created | See tree below |
| `.claude/CLAUDE.md` | ✅ | Project instructions for Claude Code |
| `.github/copilot-instructions.md` | ✅ | Team base context for Copilot |
| **Agents (Claude Code)** | 7 × `.agent.md` | planner, coder, code-reviewer, tester, ado-manager, office-writer, devops-engineer |
| **Agents (Copilot)** | 7 × `.agent.md` | ✅ ado-manager, office-writer, devops-engineer, planner, coder, tester, code-reviewer |
| **Copilot prompts** | 6 × `.prompt.md` | create-work-items, ppt-from-outline, pr-description, release-notes, code-review, write-tests |
| **Copilot instructions** | 3 × `.instructions.md` | python, ado, terraform |
| PR template | ✅ | `.github/pull_request_template.md` |
| `configs/mcp/` | ✅ | Local + remote setup documented |
| `configs/envs/conda-env.yml` | ✅ | All Python dependencies |
| `docs/` | 6 docs | README, onboarding, contributing, naming-conventions, mcp-setup, automation-catalog |
| `.vscode/` | ✅ | settings.json + extensions.json |
| `.gitignore` | ✅ | |

### Done — Skills (26 total SKILL.md files)

| Domain | Skills | Status |
|---|---|---|
| `coding` | plan-task, code-review, write-tests | ✅ Phase 0 |
| `comms` | meeting-minutes, email-draft, teams-announcement | ✅ All done |
| `devops` | pr-description, ado-pipeline-yaml, gh-actions-workflow | ✅ All done |
| `meta` | new-skill, new-agent, validate-skill, update-catalog | ✅ Phase 0 |
| `office` | ppt-from-outline, word-doc, excel-report | ✅ All done |
| `ado` | create-work-items, sprint-planning, release-notes, pr-linker | ✅ All done |
| `data-ml` | schema-docs, pipeline-docs, model-card | ✅ All done |
| `infra` | terraform-module, arch-diagram, incident-runbook | ✅ All done |

### Done — Python Scripts (14 total)

| Script | Purpose | Status |
|---|---|---|
| `scripts/repo/validate_skill.py` | Validate SKILL.md structure | ✅ Phase 0 |
| `scripts/repo/validate_agent.py` | Validate agent.md structure | ✅ Phase 0 |
| `scripts/repo/generate_catalog.py` | Auto-generate automation catalog | ✅ Phase 0 |
| `scripts/shared/auth.py` | ADO/GitHub/MSGraph auth helpers | ✅ Phase 0 |
| `scripts/shared/utils.py` | Common utilities | ✅ Phase 0 |
| `scripts/git/pr_description.py` | Generate PR description from diff | ✅ Phase 0 |
| `scripts/ado/create_work_items.py` | ADO REST: create Epic/Feature/Story/Task from JSON | ✅ |
| `scripts/ado/sprint_report.py` | Fetch sprint data → Markdown/JSON report | ✅ |
| `scripts/ado/release_notes.py` | Build release notes from closed work items | ✅ |
| `scripts/office/ppt_builder.py` | jinja2 + HTML: build presentation from JSON slide plan | ✅ |
| `scripts/office/word_builder.py` | python-docx: generate Word docs from JSON spec | ✅ |
| `scripts/office/excel_builder.py` | openpyxl: formatted Excel reports from JSON spec | ✅ |
| `scripts/data/schema_documenter.py` | DDL/live DB → schema Markdown + Mermaid ER | ✅ |
| `scripts/data/pipeline_documenter.py` | Airflow/ADF/dbt/generic → pipeline docs | ✅ |

---

### Done — Quality Audit

Full audit of all 26 skills, 14 agents (7 Claude + 7 Copilot), and 14 scripts. **12 inconsistencies found and fixed:**

| # | Issue | Fix |
|---|-------|-----|
| 1 | Missing Claude `devops-engineer` agent (Copilot had it, Claude didn't) | Created `.claude/agents/devops-engineer.agent.md` — now 7/7 parity |
| 2 | Terraform tag casing (`PascalCase` vs `snake_case`) in skills and agents | Standardized to `snake_case` everywhere per `terraform.instructions.md` |
| 3 | Broken `/rca` skill reference in `incident-runbook/SKILL.md` | Changed to `/word-doc` with `type: rca` |
| 4 | ADO scripts missing error handling for API calls | Added `AzureDevOpsServiceError` try/except to `sprint_report.py`, `release_notes.py` |
| 5 | Unused imports in 4 scripts | Removed `os`, `ast`, `RGBColor`, `sys` from respective scripts |
| 6 | Missing type annotations on API client params | Added string annotations to all 3 ADO scripts + `excel_builder.py` |
| 7 | Prompt naming mismatch (`create-work-item` → `create-work-items`) | Renamed file and updated to support bulk creation |
| 8 | Code-reviewer agent parity (severity labels, function length threshold) | Standardized to BLOCK/WARN/NIT/GOOD, 40-line threshold in both frameworks |
| 9 | Validator incompatibility (same frontmatter rules for Claude vs Copilot) | Split into `CLAUDE_REQUIRED_FRONTMATTER` / `COPILOT_REQUIRED_FRONTMATTER` |
| 10 | Python instructions ambiguity (`main()` only, not `app()`) | Updated to say `main()` or `app()` when using typer |

### Done — HTML Presentation Migration

Replaced `.pptx` generation (`python-pptx`) with self-contained HTML presentations (`jinja2`).

| Change | Details |
|--------|--------|
| `scripts/office/ppt_builder.py` | Rewrote: Jinja2 HTML generation with CSS template extraction, keyboard nav, print CSS |
| `ppt-from-outline` skill | Updated: template system now uses `.html` files, two-phase confirm-then-build |
| Both `office-writer` agents | Updated: PPT → HTML presentations, new template system documented |
| `ppt-from-outline` Copilot prompt | Updated: HTML output, confirm-before-build |
| `templates/ppt/team-update.html` | Created: ABI-branded HTML template with extractable `<style>` block |
| `configs/envs/conda-env.yml` | Removed `python-pptx` (already had `jinja2`) |
| `python.instructions.md` | Updated: `jinja2` for presentations instead of `python-pptx` |
| `CONTRIBUTING.md` | Created: extracted from README, full contribution guide at repo root |
| `README.md` | Updated: HTML presentations, new "What Can You Do?" section, contributing link |

### Done — Root README.md

Comprehensive `README.md` created at repo root covering: overview, prerequisites, full setup (conda, MCP, env vars, verification), repo structure, how to use (skills, prompts, agents, scripts), full automation catalog by domain, MCP server reference, env vars reference, contributing workflow, naming conventions, and architecture decisions.

`docs/README.md` updated to match (brief quickstart version with links to full docs).

---

### Remaining: Templates

Folder: `templates/`
Word and Excel templates require actual binary files (branded `.docx`, `.xlsx` bases). The scripts fall back to blank documents when templates are missing, so this is non-blocking.
Presentation templates are `.html` files — `team-update.html` is already provided.

- `ppt/team-update.html` ✅ (provided)
- `ppt/project-kickoff.html` (create when needed)
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
