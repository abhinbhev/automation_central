# automation_central

Central hub for the ABI engineering team's AI-assisted agents, skills, scripts, and templates.

Supports **Claude Code** and **GitHub Copilot** — any team member opens this repo in VS Code and gets access to 33 skills, 10 agent modes, 21 prompts, and 14 Python scripts that automate ADO board management, Office document generation, CI/CD scaffolding, data documentation, and more.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [1. Clone and open](#1-clone-and-open)
  - [2. Python environment](#2-python-environment)
  - [3. MCP servers](#3-mcp-servers)
  - [4. Verify setup](#4-verify-setup)
- [Repo Structure](#repo-structure)
- [How to Use](#how-to-use)
  - [Skills (Claude Code)](#skills-claude-code)
  - [Prompts (GitHub Copilot)](#prompts-github-copilot)
  - [Agent Modes](#agent-modes)
  - [Python Scripts](#python-scripts)
- [Agent Prerequisites](#agent-prerequisites)
  - [Summary](#summary)
  - [ado-manager](#ado-manager-1)
  - [github-manager](#github-manager-1)
  - [office-writer](#office-writer-1)
  - [devops-engineer](#devops-engineer-1)
  - [coder](#coder-1)
  - [tester](#tester-1)
  - [code-reviewer](#code-reviewer-1)
  - [planner](#planner-1)
  - [doc-writer](#doc-writer-1)
  - [agent-skill-manager](#agent-skill-manager-1)
- [Automation Catalog](#automation-catalog)
  - [ADO Board Management](#ado-board-management)
  - [Office Documents](#office-documents)
  - [Communication](#communication)
  - [DevOps / CI-CD](#devops--ci-cd)
  - [Infrastructure](#infrastructure)
  - [Data / ML](#data--ml)
  - [Coding](#coding)
  - [Documentation](#documentation)
  - [Meta (Repo Management)](#meta-repo-management)
- [Naming Conventions](#naming-conventions)
- [MCP Server Reference](#mcp-server-reference)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [What Can You Do?](#what-can-you-do)
- [Architecture Decisions](#architecture-decisions)

---

## Quick Start

```bash
# 1. Clone and open
git clone <repo-url>
cd automation_central
code .

# 2. Python env
conda env create -f configs/envs/conda-env.yml
conda activate automation-central

# 3. MCP servers local (optional, follow configs/mcp/local/README.md for auth)
npm install -g @modelcontextprotocol/server-azure-devops
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-msgraph

# 4. Test — in Claude Code type:
#    /meeting-minutes      then paste some notes
#    /ppt-from-outline     then paste a bullet outline (builds HTML presentation)
```

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| VS Code | Latest | Editor — loads agents, skills, prompts automatically |
| Claude Code extension | Latest | Runs `.claude/` agents and skills |
| GitHub Copilot extension | Latest | Runs `.github/` agents and prompts |
| Git | 2.x+ | Version control |
| Conda (Miniconda or Anaconda) | Latest | Python environment management |
| Node.js | 18+ | MCP server installation (`npm`) |

---

## Setup

### 1. Clone and open

```bash
git clone <repo-url>
cd automation_central
code .
```

When VS Code opens, it will prompt to install recommended extensions. Click **Install All**.

Alternatively, install manually:
1. Open the Command Palette (`Ctrl+Shift+P`)
2. Run **Extensions: Show Recommended Extensions**
3. Install everything in the Workspace Recommendations list

> **Multi-root workspace**: You can also add this repo as a folder to an existing workspace (`File → Add Folder to Workspace`). The `.vscode/settings.json` and all agents/skills will still load.

### 2. Python environment

```bash
conda env create -f configs/envs/conda-env.yml
conda activate automation-central
```

Verify:
```bash
python -c "import azure.devops, docx, openpyxl, jinja2; print('OK')"
```

**Key packages** (all installed by the conda env):

| Package | Used by |
|---------|--------|
| `azure-devops` | ADO scripts |
| `azure-identity` | Azure auth |
| `jinja2` | HTML presentation generation |
| `python-docx` | Word document generation |
| `openpyxl` | Excel report generation |
| `httpx` | HTTP calls |
| `typer` | CLI interfaces for all scripts |
| `rich` | Formatted console output |
| `pyyaml` | YAML parsing (pipeline docs) |
| `python-dotenv` | `.env` file loading |

### 3. MCP servers

MCP (Model Context Protocol) servers give Claude Code and Copilot live access to external systems.

> **Phase 1 — Local (current):** Each team member runs MCP servers on their own machine using the setup below.
> **Phase 2 — Centralised (future):** A shared server will be provisioned; skills require no changes to switch — they reference MCP tools by name only.

#### Install

```bash
npm install -g @modelcontextprotocol/server-azure-devops
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-msgraph
```

#### Authenticate

You need three sets of credentials. **Never commit these to the repo.**

**Azure DevOps PAT:**
1. Go to `https://dev.azure.com/<your-org>/_usersSettings/tokens`
2. Create a token with scopes: `Work Items (Read & Write)`, `Code (Read)`, `Build (Read)`

**GitHub PAT:**
1. GitHub → Settings → Developer Settings → Personal access tokens → Fine-grained tokens
2. Scopes: `repo`, `read:org`

**MS Graph (Azure AD App):**
1. Azure Portal → Azure Active Directory → App registrations → New registration
2. Name: `automation-central-mcp-local`
3. Delegated permissions: `Mail.ReadWrite`, `Calendars.Read`, `Files.ReadWrite`, `Sites.ReadWrite.All`, `ChannelMessage.Send`
4. Grant admin consent → create client secret

#### Set environment variables

Add to your shell profile (PowerShell `$PROFILE`, bash `~/.bashrc`, or Windows System Environment Variables):

```bash
# ADO
export ADO_ORG_URL="https://dev.azure.com/<your-org>"
export ADO_PAT="<your-ado-pat>"
export ADO_PROJECT="<your-project-name>"

# GitHub
export GITHUB_TOKEN="<your-github-pat>"

# MS Graph (Teams, Outlook, SharePoint)
export AZURE_TENANT_ID="<your-tenant-id>"
export AZURE_CLIENT_ID="<your-app-client-id>"
export AZURE_CLIENT_SECRET="<your-app-client-secret>"
```

PowerShell equivalent:
```powershell
$env:ADO_ORG_URL = "https://dev.azure.com/<your-org>"
$env:ADO_PAT = "<your-ado-pat>"
$env:ADO_PROJECT = "<your-project-name>"
# ... etc
```

#### Configure Claude Code

Merge the MCP server config into your Claude settings:

```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-azure-devops"],
      "env": { "ADO_ORG_URL": "${ADO_ORG_URL}", "ADO_PAT": "${ADO_PAT}" }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "ms-graph": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-msgraph"],
      "env": {
        "AZURE_TENANT_ID": "${AZURE_TENANT_ID}",
        "AZURE_CLIENT_ID": "${AZURE_CLIENT_ID}",
        "AZURE_CLIENT_SECRET": "${AZURE_CLIENT_SECRET}"
      }
    }
  }
}
```

See `configs/mcp/local/README.md` for the full guide and a template JSON you can copy.

### 4. Verify setup

| Check | Command |
|-------|---------|
| Python env works | `python -c "import azure.devops, docx, openpyxl, jinja2; print('OK')"` |
| ADO auth works | `python -c "from scripts.shared.auth import get_ado_connection; get_ado_connection(); print('OK')"` |
| Skills appear | In Claude Code, type `/` — skills should autocomplete |
| Prompts appear | In Copilot Chat, type `/` — prompts should autocomplete |
| Agents appear | In agent picker, `ado-manager`, `coder`, etc. should be listed |

**Test a skill (Claude Code):**
1. Open any file or a blank editor tab and invoke Claude Code chat
2. Type `/meeting-minutes` and paste some bullet-point notes
3. Claude should return formatted minutes with attendees, decisions, and action items

**Test a prompt (GitHub Copilot):**
1. Open Copilot Chat (`Ctrl+Alt+I`)
2. Type `/create-work-items` followed by a short task description
3. Copilot should return a structured ADO work item preview

---

## Repo Structure

```
automation_central/
├── .claude/
│   ├── CLAUDE.md                          ← project-level instructions for Claude Code
│   ├── agents/                            ← 10 Claude Code agent modes
│   │   ├── ado-manager.agent.md
│   │   ├── agent-skill-manager.agent.md
│   │   ├── code-reviewer.agent.md
│   │   ├── coder.agent.md
│   │   ├── devops-engineer.agent.md
│   │   ├── doc-writer.agent.md
│   │   ├── github-manager.agent.md
│   │   ├── office-writer.agent.md
│   │   ├── planner.agent.md
│   │   └── tester.agent.md
│   └── skills/                            ← 33 skills, grouped by domain
│       ├── ado/                           ← ADO board management
│       ├── coding/                        ← code review, planning, testing
│       ├── comms/                         ← email, meetings, Teams
│       ├── data-ml/                       ← schema docs, pipeline docs, model cards
│       ├── devops/                        ← CI/CD, PR descriptions, commit messages
│       ├── docs/                          ← READMEs, ADRs, runbooks, API docs
│       ├── infra/                         ← Terraform, arch diagrams, runbooks
│       ├── meta/                          ← repo management (add-skill, add-agent, validate, catalog)
│       └── office/                        ← HTML presentations, Word, Excel
├── .github/
│   ├── copilot-instructions.md            ← team context for GitHub Copilot
│   ├── agents/                            ← 10 Copilot agent modes
│   ├── prompts/                           ← 21 Copilot slash-command prompts
│   ├── instructions/                      ← scoped coding instructions (Python, ADO, Terraform)
│   └── pull_request_template.md
├── scripts/
│   ├── ado/                               ← ADO API scripts (create, report, release notes)
│   ├── office/                            ← ppt_builder (HTML), word_builder, excel_builder
│   ├── data/                              ← schema_documenter, pipeline_documenter
│   ├── git/                               ← pr_description
│   ├── repo/                              ← validate_skill, validate_agent, generate_catalog
│   └── shared/                            ← auth helpers, common utilities
├── templates/
│   ├── ppt/                               ← HTML aesthetic templates for presentations
│   ├── word/                              ← .docx templates (SOP, ADR, RCA)
│   ├── excel/                             ← .xlsx templates
│   ├── ado/                               ← work item JSON templates
│   └── iac/                               ← Terraform / GH Actions starters
├── configs/
│   ├── envs/conda-env.yml                 ← Python dependencies
│   └── mcp/                               ← MCP server setup (local + remote)
├── docs/                                  ← ADRs, runbooks, and API docs (generated by doc-writer agent)
├── .vscode/                               ← recommended extensions + settings
├── .gitignore
├── PROGRESS.md                            ← build progress tracker
└── README.md                              ← this file
```

---

## How to Use

### Skills (Claude Code)

Skills are invoked with `/skill-name` in the Claude Code chat. Type `/` and autocomplete will show all available skills.

**Example:**
```
/meeting-minutes

Here are my notes from today's standup:
- Alice: finished the auth migration PR, starting rate limiting today
- Bob: blocked on Terraform VNet config, needs @Charlie to review
- Charlie: completed sprint tracker Excel, will review Bob's PR after lunch
```

Claude will produce structured meeting minutes with attendees, decisions, and action items.

**Skills that produce files** (presentations, Word, Excel) work in two phases:
1. Phase 1: produces a structured plan/outline — you review and confirm
2. Phase 2: on your approval, runs a Python script to generate the actual file

### Prompts (GitHub Copilot)

Prompts appear in Copilot Chat when you type `/`. They work similarly to skills but are designed for the Copilot interface.

**Available prompts:**

**ADO & Planning**
| Command | What it does |
|---------|-------------|
| `/create-work-items` | Description → structured ADO work items |
| `/plan-sprint` | Pull backlog items → draft sprint plan |
| `/decompose-feature` | Feature description → estimable backlog |
| `/release-notes` | Sprint items → stakeholder release notes |

**Code & DevOps**
| Command | What it does |
|---------|-------------|
| `/code-review` | Diff → review findings by severity |
| `/write-tests` | Code → pytest test suite |
| `/implement-feature` | Task → coded implementation |
| `/commit-message` | Staged diff → conventional commit message |
| `/pr-description` | Git diff → PR body |
| `/scaffold-pipeline` | Requirements → GitHub Actions or Azure Pipelines YAML |
| `/scaffold-terraform` | Requirements → Terraform module (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`) |

**Documentation**
| Command | What it does |
|---------|-------------|
| `/write-readme` | Codebase path → complete README |
| `/write-adr` | Decision description → ADR |
| `/write-runbook` | Service description → operational runbook |
| `/write-api-docs` | Source code / OpenAPI spec → API reference |
| `/write-word-doc` | Outline → Word document (SOP, ADR, RCA, spec) |

**GitHub**
| Command | What it does |
|---------|-------------|
| `/triage-issues` | Freetext → structured GitHub issues |

**Office**
| Command | What it does |
|---------|-------------|
| `/ppt-from-outline` | Bullet outline → HTML presentation |
| `/build-excel-report` | Description → formatted `.xlsx` |

**Repo Management**
| Command | What it does |
|---------|-------------|
| `/add-skill` | Create + validate + register a new Claude Code skill |
| `/add-agent` | Create + validate + register agent files for both frameworks |

### Agent Modes

Both Claude Code and Copilot support specialized agent modes. Select them from the agent picker or invoke as subagents.

| Agent | Use when |
|-------|---------|
| `ado-manager` | Creating/querying ADO work items, sprint planning, release notes |
| `agent-skill-manager` | Creating, validating, and registering new skills and agents |
| `github-manager` | PRs, issues, repo management, branch policies, GitHub Actions |
| `office-writer` | Generating HTML presentations, Word, or Excel documents |
| `planner` | Breaking features/epics into subtasks with acceptance criteria |
| `coder` | Writing code following team standards |
| `tester` | Generating pytest test suites |
| `code-reviewer` | Reviewing diffs against the team checklist |
| `devops-engineer` | CI/CD pipelines, Terraform modules, architecture diagrams |
| `doc-writer` | READMEs, ADRs, runbooks, API docs, changelogs |

### Python Scripts

Scripts are called by skills when actual file generation or API calls are needed. You can also run them directly:

```bash
# Create ADO work items from a JSON spec
python scripts/ado/create_work_items.py --spec items.json --project MyProject

# Generate a sprint status report
python scripts/ado/sprint_report.py --iteration "MyProject\Sprint 42" --project MyProject

# Build an HTML presentation from a slide plan
python scripts/office/ppt_builder.py --plan slides.json --output presentation.html

# Generate schema docs from SQL DDL
python scripts/data/schema_documenter.py --ddl schema.sql --output docs.md

# Validate a skill before PR
python scripts/repo/validate_skill.py .claude/skills/ado/create-work-items

# Regenerate the automation catalog
python scripts/repo/generate_catalog.py
```

All scripts use `typer` for CLI, `rich` for output, and follow the conventions in `.github/instructions/python.instructions.md`.

---

## Agent Prerequisites

Each agent has different external dependencies. Install only what you need for the agents you use. 
> _Note: You might need to get admin access for some of these._

### Summary

| Agent | MCP Server | CLI Tools | Env Vars | Notes |
|-------|-----------|-----------|----------|-------|
| `ado-manager` | `server-azure-devops` | — | `ADO_ORG_URL`, `ADO_PAT`, `ADO_PROJECT` | ADO PAT with Work Items + Code scopes |
| `github-manager` | `server-github` | `gh` (GitHub CLI) | `GITHUB_TOKEN` | `gh` required for PR/branch operations |
| `office-writer` | — | — | — | Python conda env only (`python-docx`, `openpyxl`, `jinja2`) |
| `devops-engineer` | — | `terraform`, `az` | — | CLI tools for validation; not required for generation-only use |
| `coder` | — | — | — | Full conda env to run and test generated code |
| `tester` | — | — | — | `pytest` + `pytest-mock` (in conda env) |
| `code-reviewer` | — | `git` | — | `git diff` to produce diffs for review |
| `planner` | — | — | — | No external deps; optionally chains to `ado-manager` |
| `doc-writer` | — | — | — | No external deps; reads codebase, writes Markdown |
| `agent-skill-manager` | — | — | — | Needs conda env to run `validate_skill.py` and `validate_agent.py` |

---

### `ado-manager`

Requires live access to Azure DevOps to create/query work items, plan sprints, and read pipelines.

**MCP server**
```bash
npm install -g @modelcontextprotocol/server-azure-devops
```

**Environment variables**

| Variable | Description |
|----------|-------------|
| `ADO_ORG_URL` | `https://dev.azure.com/<your-org>` |
| `ADO_PAT` | Personal Access Token — create at `https://dev.azure.com/<org>/_usersSettings/tokens` |
| `ADO_PROJECT` | Default project name used by scripts |

**PAT scopes required:** `Work Items (Read & Write)`, `Code (Read)`, `Build (Read)`

**Python packages** (in conda env): `azure-devops`, `azure-identity`

---

### `github-manager`

Requires GitHub API access (via MCP) and the `gh` CLI for operations the MCP server does not cover, such as merging PRs, managing branch protection rules, and reading Actions workflow run logs.

**MCP server**
```bash
npm install -g @modelcontextprotocol/server-github
```

**CLI tool — GitHub CLI**
```bash
# Windows (winget)
winget install --id GitHub.cli

# macOS
brew install gh

# Authenticate after install
gh auth login
```

**Environment variables**

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | GitHub PAT — create at GitHub → Settings → Developer Settings → Fine-grained tokens |

**PAT scopes required:** `repo`, `read:org`, `workflow`

> Without `gh` CLI, the agent can still generate PR descriptions, scaffold workflows, and read repo contents. It cannot create/merge PRs, modify branch protection rules, or read live Actions logs.

---

### `office-writer`

Generates HTML presentations, Word documents, and Excel reports. No external API or credentials required — all generation happens locally via Python scripts.

**Python packages** (all in conda env):

| Package | Used for |
|---------|---------|
| `jinja2` | HTML presentation rendering (`ppt_builder.py`) |
| `python-docx` | Word document generation (`word_builder.py`) |
| `openpyxl` | Excel report generation (`excel_builder.py`) |

**Verify:**
```bash
python -c "import jinja2, docx, openpyxl; print('office-writer: OK')"
```

**Template files** (optional): place `.html` files in `templates/ppt/` for branded presentations. Falls back to a built-in theme if none found.

---

### `devops-engineer`

Generates CI/CD pipeline YAML and Terraform modules. The agent works without CLI tools (generation only), but the following are needed to validate generated output locally.

**CLI tool — Terraform**
```bash
# Windows (winget)
winget install --id Hashicorp.Terraform

# macOS
brew tap hashicorp/tap && brew install hashicorp/tap/terraform

# Verify
terraform -version   # must be >= 1.5
```

Used for: `terraform fmt` and `terraform validate` on generated modules before committing.

**CLI tool — Azure CLI**
```bash
# Windows
winget install --id Microsoft.AzureCLI

# macOS
brew install azure-cli

# Authenticate
az login

# Verify
az --version
```

Used for: resolving existing Azure resource IDs and data sources when scaffolding Terraform modules. Not required for pure YAML generation.

> The agent **never runs** `terraform apply` or any deployment commands — it generates config only.

---

### `coder`

Writes and runs Python code. Requires the full conda environment to execute and test generated scripts.

**Setup**
```bash
conda env create -f configs/envs/conda-env.yml
conda activate automation-central
```

No external API access or credentials required unless the code being written interacts with ADO, GitHub, or Azure (in which case the relevant agent's credentials apply).

---

### `tester`

Generates and runs pytest test suites. Requires `pytest` and `pytest-mock`.

**Verify:**
```bash
pytest --version       # included in conda env
python -m pytest --co  # dry-run: collect tests without executing
```

No external API access required. For integration tests that call live services, the relevant credentials (ADO PAT, GitHub token) must be set.

---

### `code-reviewer`

Reviews code diffs. Requires `git` to produce diffs for review.

**Generate a diff for review:**
```bash
git diff main...HEAD          # all changes on current branch vs main
git diff HEAD~1               # last commit only
git diff --staged             # staged changes before commit
```

Paste the output into the agent chat, or point it at a file path and it will read the code directly.

No credentials or MCP server required.

---

### `planner`

Decomposes features and requirements into structured backlog items. Works entirely from conversation context and codebase file access — no external tools or credentials required.

Optionally chains to `ado-manager` to create the resulting items in ADO. If you plan to do this, ensure `ado-manager` prerequisites are met first.

---

### `doc-writer`

Reads code and generates Markdown documentation (READMEs, ADRs, runbooks, API docs). No external tools, MCP servers, or credentials required.

Works best when pointed at a file path — it reads the source and cross-checks any commands it documents against the actual codebase.

---

### `agent-skill-manager`

Creates and validates new skills and agents. Requires the conda environment to run the validator scripts.

**Setup** (same conda env as `coder`):
```bash
conda env create -f configs/envs/conda-env.yml
conda activate automation-central
```

**Verify validators work:**
```bash
python scripts/repo/validate_skill.py .claude/skills/meta/add-skill
python scripts/repo/validate_agent.py .claude/agents/agent-skill-manager.agent.md
```

No external API or credentials required. The validators only read local files.

---

## Automation Catalog

### ADO Board Management

| Skill | Description | Has Script |
|-------|-------------|-----------|
| `/create-work-items` | Freetext → ADO work items (single or bulk) | ✅ `create_work_items.py` |
| `/sprint-planning` | Plan and populate a sprint from the backlog | — (MCP) |
| `/release-notes` | Closed items → stakeholder or internal release notes | ✅ `release_notes.py` |
| `/pr-linker` | Link GitHub PRs to ADO items via `AB#ID` tags | — (MCP) |

### Office Documents

| Skill | Description | Has Script |
|-------|-------------|-----------|
| `/ppt-from-outline` | Bullet outline → slide plan → `.html` presentation | ✅ `ppt_builder.py` |
| `/word-doc` | SOPs, ADRs, specs, RCA, reports → `.docx` file | ✅ `word_builder.py` |
| `/excel-report` | Data → formatted `.xlsx` with charts and conditional formatting | ✅ `excel_builder.py` |

### Communication

| Skill | Description |
|-------|-------------|
| `/meeting-minutes` | Transcript or notes → structured minutes with action items |
| `/email-draft` | Draft a stakeholder email |
| `/teams-announcement` | Sprint updates, release comms, incident resolved |

### DevOps / CI-CD

| Skill | Description |
|-------|-------------|
| `/pr-description` | Git diff → PR body (has script: `pr_description.py`) |
| `/commit-message` | Staged diff → conventional commit message (`feat`, `fix`, `chore`, etc.) |
| `/ado-pipeline-yaml` | Generate `azure-pipelines.yml` for any stack |
| `/gh-actions-workflow` | Generate GitHub Actions workflow YAML |

### Infrastructure

| Skill | Description |
|-------|-------------|
| `/terraform-module` | Scaffold a complete Terraform module |
| `/arch-diagram` | Generate Mermaid architecture diagrams (C4, sequence, deployment) |
| `/incident-runbook` | Structured operational runbook |

### Data / ML

| Skill | Description | Has Script |
|-------|-------------|-----------|
| `/schema-docs` | DDL or live DB → schema Markdown + Mermaid ER diagram | ✅ `schema_documenter.py` |
| `/pipeline-docs` | Airflow/ADF/dbt config → pipeline documentation | ✅ `pipeline_documenter.py` |
| `/model-card` | ML model → model card with metrics, limitations, responsible AI |

### Coding

| Skill | Description |
|-------|-------------|
| `/plan-task` | Feature → decomposed subtasks with acceptance criteria |
| `/code-review` | Code → review findings by severity (BLOCK/WARN/NIT) |
| `/write-tests` | Code → pytest test suite |

### Documentation

| Skill | Description |
|-------|-------------|
| `/write-readme` | Codebase path or description → complete README |
| `/write-adr` | Decision description → Architecture Decision Record |
| `/write-runbook` | Service description → operational runbook (diagnosis, remediation, escalation) |
| `/write-api-docs` | Source code or OpenAPI spec → API reference documentation |

### Meta (Repo Management)

| Skill | Description |
|-------|-------------|
| `/add-skill` | Create + validate + register a new skill (runs validator, updates catalog) |
| `/add-agent` | Create + validate both Claude and Copilot agent files, updates catalog |
| `/new-skill` | Scaffold a new SKILL.md stub (no validation) |
| `/new-agent` | Scaffold a new .agent.md stub (no validation) |
| `/validate-skill` | Check a skill folder against repo standards |
| `/update-catalog` | Regenerate the automation catalog |

---

## Naming Conventions

All files and folders follow `<domain>-<action>` in kebab-case.

| Type | Convention | Example |
|------|-----------|---------|
| Skill folder | `<action>/` inside domain folder | `.claude/skills/ado/create-work-items/` |
| Skill file | always `SKILL.md` | `.claude/skills/ado/create-work-items/SKILL.md` |
| Agent file | `<domain>-<role>.agent.md` | `.claude/agents/ado-manager.agent.md` |
| Copilot prompt | `<action>.prompt.md` | `.github/prompts/pr-description.prompt.md` |
| Python script | `<action>_<noun>.py` (snake_case) | `scripts/ado/create_work_items.py` |
| Template file | descriptive kebab-case | `templates/ppt/team-update.html` |

**Domains:**

| Domain | Covers |
|--------|--------|
| `ado` | Azure DevOps — work items, sprints, pipelines, PRs |
| `office` | PowerPoint, Word, Excel, non-tech doc outputs |
| `devops` | CI/CD, GitHub Actions, ADO Pipelines, git workflows |
| `data-ml` | Schemas, pipelines, model cards, experiment tracking |
| `infra` | Terraform, Bicep, cloud infra, architecture diagrams |
| `comms` | Teams, Outlook, meeting minutes, stakeholder updates |
| `coding` | Code review, test generation, task planning, SCM |
| `docs` | Technical documentation — READMEs, ADRs, runbooks, API docs |
| `meta` | Repo self-maintenance — scaffold, validate, catalog |

---

## MCP Server Reference

| Server | What it enables | Install command |
|--------|----------------|----------------|
| `azure-devops` | ADO work items, sprints, boards, pipelines | `npm i -g @modelcontextprotocol/server-azure-devops` |
| `github` | PRs, issues, diffs, repo contents | `npm i -g @modelcontextprotocol/server-github` |
| `ms-graph` | Outlook email, Teams messages, SharePoint/OneDrive | `npm i -g @modelcontextprotocol/server-msgraph` |
| `microsoft-teams` | Draft and send Teams channel messages directly | via MS Graph MCP |
| `filesystem` | Read/write local files | Built into Claude Code |

Full MCP setup guide: `configs/mcp/local/README.md`

---

## Environment Variables

| Variable | Required by | Description |
|----------|------------|-------------|
| `ADO_ORG_URL` | ADO scripts + MCP | `https://dev.azure.com/<your-org>` |
| `ADO_PAT` | ADO scripts + MCP | ADO Personal Access Token |
| `ADO_PROJECT` | ADO scripts | Default ADO project name |
| `GITHUB_TOKEN` | GitHub MCP + scripts | GitHub PAT |
| `AZURE_TENANT_ID` | MS Graph MCP + auth | Azure AD tenant ID |
| `AZURE_CLIENT_ID` | MS Graph MCP + auth | Azure AD app client ID |
| `AZURE_CLIENT_SECRET` | MS Graph MCP + auth | Azure AD app client secret |
| `SCHEMA_DB_URL` | `schema_documenter.py` | SQLAlchemy connection string (optional) |

Store these in environment variables or a `.env` file (which is in `.gitignore`). **Never commit credentials.**

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide — branching, skill/agent/prompt creation, validators, PR checklist, naming conventions, and review criteria.

---

## What Can You Do?

Open this repo in VS Code and you can ask your AI assistant to:

| Just say... | What happens |
|-------------|-------------|
| "Create a presentation about Q3 results" | Builds a slide plan, asks for your OK, then generates an HTML presentation you open in your browser |
| "Write meeting minutes from these notes" | Turns messy bullet points into structured minutes with action items and owners |
| "Draft an email to stakeholders about the release" | Produces a polished email ready to send |
| "Create work items for this feature" | Breaks your description into ADO Epics, Features, Stories, and Tasks |
| "Write an SOP for the deployment process" | Generates a Word document following the SOP template |
| "Generate a sprint report" | Pulls data from ADO and formats a status report |
| "Review this code" | Checks your diff against the team checklist and flags issues by severity |
| "Write tests for this module" | Generates a pytest test suite with edge cases |
| "Scaffold a Terraform module for a storage account" | Produces `main.tf`, `variables.tf`, `outputs.tf` with team conventions |
| "Generate a PR description" | Reads your git diff and writes a structured PR body |
| "Plan this feature into subtasks" | Decomposes a feature into implementation tasks with acceptance criteria |
| "Document this database schema" | Generates Markdown docs + a Mermaid ER diagram from your DDL |

**How it works:** Type `/` in Claude Code or Copilot Chat to see all available commands, or just describe what you need in plain English and the right agent/skill activates automatically.

---

## Architecture Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| AI frameworks | Claude Code + GitHub Copilot | Team uses both; shared scripts ensure feature parity |
| Skills location | `.claude/skills/<domain>/<name>/` | Claude Code standard; domain grouping keeps it navigable |
| Copilot equivalent | `.github/prompts/` + `.github/agents/` | Copilot uses prompts (no native skills) + agent modes |
| Scripts | Python in `scripts/` | Framework-agnostic; called by skills when execution > text |
| MCP strategy | Local-first, remote path documented | No shared server yet; designed for easy migration |
| Catalog | Auto-generated via `generate_catalog.py` | Prevents drift as skills accumulate |
| Contribution | PR + validator gate + 1 reviewer | Low friction; `validate_skill.py` catches structural issues |
| Tag convention | `snake_case` (`environment`, `team`, `managed_by`) | Consistent with Terraform HCL conventions |
| Presentations | HTML (not `.pptx`) | Self-contained, no binary deps, template-driven CSS, opens in any browser |
