# INSTRUCTIONS.md — Operating Guide for AI Agents

> **Audience:** any AI agent (Claude Code, GitHub Copilot, future LLM tooling) working inside `automation_central`.
> **Purpose:** the single canonical reference for how this repo is wired and how to extend it without breaking anything.
> **Read order:** this file → `.claude/CLAUDE.md` (or `.github/copilot-instructions.md`) → `CONTRIBUTING.md` (only if contributing) → the relevant skill or agent file.

If anything in this file conflicts with a skill, agent, prompt, validator, or catalog generator, **this file is the source of truth** — fix the other place to match (and update the catalog).

---

## Table of Contents

1. [What this repo is](#1-what-this-repo-is)
2. [The four primitives](#2-the-four-primitives)
3. [How the primitives wire together](#3-how-the-primitives-wire-together)
4. [File and folder contracts](#4-file-and-folder-contracts)
5. [Naming conventions](#5-naming-conventions)
6. [Domains](#6-domains)
7. [Validators and the catalog](#7-validators-and-the-catalog)
8. [Standard workflows](#8-standard-workflows)
9. [Coding standards](#9-coding-standards)
10. [MCP servers and what to assume](#10-mcp-servers-and-what-to-assume)
11. [Pre-PR checklist (mandatory)](#11-pre-pr-checklist-mandatory)
12. [Things never to do](#12-things-never-to-do)
13. [How to update this file](#13-how-to-update-this-file)

---

## 1. What this repo is

Central hub for an Anheuser-Busch InBev cross-functional engineering team's AI-assisted automation. It supports **two AI frameworks in parallel** — Claude Code and GitHub Copilot — by providing parallel asset trees that share the same Python scripts and templates underneath.

Anyone on the team opens the repo in VS Code and gets:
- **Slash commands** (skills/prompts) for repeated workflows
- **Agent modes** (specialised personas)
- **Python scripts** for execution that text alone can't do (API calls, file generation)

The repo's own automations also maintain themselves — `agent-skill-manager` agent and `meta/*` skills add, validate, and catalog new entries.

---

## 2. The four primitives

| Primitive | Lives in | Used by | Invoke as |
|---|---|---|---|
| **Skill** | `.claude/skills/<domain>/<name>/SKILL.md` | Claude Code | `/skill-name` in Claude chat |
| **Agent** (paired) | `.claude/agents/<name>.agent.md` **and** `.github/agents/<name>.agent.md` | Both frameworks | Selected from agent picker |
| **Copilot Skill** | `.github/skills/<name>/SKILL.md` | Copilot Chat / agents | `/skill-name` in Copilot Chat |
| **Script** | `scripts/<domain>/<action>.py` | Skills, agents, humans | `python scripts/<domain>/<action>.py …` |

**Counts as of 2026-04-29:** 33 Claude skills, 10 agents (× 2 = 20 agent files), 21 Copilot skills, 14 scripts. The opening lines of `README.md` carry these numbers — update them when counts change, or just leave the numbers off if you don't want to maintain them.

### Why two frameworks?

Some team members use Claude Code, some use Copilot. Claude uses Skills natively; Copilot uses its own Skill format (`.github/skills/`). Agent files are paired so both frameworks see the same persona. Copilot Skills replace what were previously `.prompt.md` files — they provide richer structured metadata for agent discovery.

### What goes where

| Decision | Choice | Reason |
|---|---|---|
| File generation, API calls, multi-step execution | **Script** | Framework-agnostic; reusable from skill or shell |
| Reusable workflow for Claude Code | **Claude Skill** (`.claude/skills/`) | Slash-command invocable, domain-grouped |
| Reusable workflow for Copilot | **Copilot Skill** (`.github/skills/`) | Slash-command invocable, agent-discoverable via description |
| Persistent persona with capabilities and boundaries | **Agent pair** | Agents pull in skills as context |
| Structured skill definition for Copilot agent discovery | **Copilot Skill** (`.github/skills/`) — pair with every Claude skill where applicable | Provides metadata + progressive loading; agents use it for context |

If a workflow needs both an LLM step and a Python step (e.g., "generate Excel"), the **skill** drafts the spec and the **script** consumes the spec. Two phases, one skill. See [`/excel-report`](.claude/skills/office/excel-report/SKILL.md) for the canonical pattern.

---

## 3. How the primitives wire together

```
┌────────────────────┐        ┌────────────────────┐
│  .claude/agents/   │        │  .github/agents/   │
│  <name>.agent.md   │        │  <name>.agent.md   │
│                    │        │                    │
│ skills:            │        │ tools: [...]       │
│   - domain/skill1  │        │ (no skills field)  │
│   - domain/skill2  │        │                    │
│                    │        │ ## Relevant Skills │
│ ## Relevant Skills │◄──────►│   - …/SKILL.md     │
│   - …/SKILL.md     │  pair  │   - …/SKILL.md     │
└─────────┬──────────┘        └─────────┬──────────┘
          │                             │
          │      both reference         │
          ▼                             ▼
┌──────────────────────────────────────────────────┐
│  .claude/skills/<domain>/<skill-name>/SKILL.md   │
│                                                  │
│  ## Usage  ## Output  ## Steps                   │
│  optional: requires_script: true / script: …     │
└────────────────────────┬─────────────────────────┘
                         │ if requires_script
                         ▼
┌──────────────────────────────────────────────────┐
│  scripts/<domain>/<action>.py                    │
│  typer CLI, type-hinted, pytest-tested           │
└──────────────────────────────────────────────────┘

      .github/skills/<name>/SKILL.md
      (Copilot equivalent of a Claude skill — invoked as /skill-name in
       Copilot Chat; agents load it for session context via description)
```

### Wiring rules (enforced by validators)

1.**Every Claude agent lists its skills twice.** Once in frontmatter (`skills: [domain/name, …]`) and once in the body (`## Relevant Skills` with full SKILL.md paths). The validator errors if any skill in frontmatter doesn't resolve to an actual `SKILL.md` file.
2. **Every Copilot agent has the body section.** Frontmatter is `description` + `tools` (no `skills` key — Copilot doesn't read it), but `## Relevant Skills` body section is required so the agent can read SKILL.md content at session start.
3. **Skill names in frontmatter match folder names exactly.** `name: create-work-items` ↔ folder `create-work-items/`.
4. **Agent `name` (Claude) matches filename stem.** `name: ado-manager` ↔ file `ado-manager.agent.md`.
5. **Scripts referenced by `requires_script: true` must exist on disk** when the SKILL.md is committed.
6. **Skills appearing in any agent’s \skills:\ must exist on disk.**

If you add a skill, the chain is: SKILL.md → at least one agent references it → catalog regenerated. If you add an agent, the chain is: both \.agent.md\ files → both reference the same skills → both pass validators → catalog regenerated.

### Pairing model summary

| What is paired | Pair members | Must match |
|---|---|---|
| Agent | \.claude/agents/X.agent.md\ + \.github/agents/X.agent.md\ | Same ame\/stem, same \description\, same \## Relevant Skills\ list |
| Claude Skill ↔ Copilot Skill | \.claude/skills/<domain>/X/SKILL.md\ + \.github/skills/X/SKILL.md\ (when both exist) | Same overall behaviour and output format |
| Script | (no pair — single source) | n/a |

---

## 4. File and folder contracts

### 4.1 SKILL.md

Required frontmatter:

```yaml
---
name: <skill-name>          # kebab-case, MUST match folder name
description: <one-liner>    # shown in /catalog autocomplete
domain: <one of the 9 domains>
requires_script: <true|false>
script: scripts/<domain>/<action>.py   # required only if requires_script: true
---
```

Required body sections (in any order, all three must appear):
- `## Usage` — how to invoke and what input to provide
- `## Output` — what the skill produces (format, structure)
- `## Steps` — numbered list of what the skill does

You may add additional sections (`## Boundaries`, `## Examples`, `## Templates`, etc.) freely. Validator only checks for the three required ones.

### 4.2 Claude `.agent.md`

```yaml
---
name: <name>                # kebab-case, MUST match filename stem
description: <one-liner>
skills:                     # WARNed if absent. Each entry must resolve on disk
  - domain/skill-name
  - domain/skill-name
---
```

Required body:
- Free-form persona description, capabilities, and boundaries (>50 chars)
- `## Relevant Skills` section listing each linked skill's `SKILL.md` path

### 4.3 Copilot `.agent.md`

```yaml
---
description: <one-liner>
tools: [read, edit, search, execute, …]   # recommended, not required
---
```

Required body:
- Free-form persona description (>50 chars)
- `## Relevant Skills` section mirroring the Claude pair

### 4.4 GitHub Copilot Skill (`SKILL.md` under `.github/skills/<name>/`)

Copilot Skills are the Copilot-native equivalent of Claude Skills. They appear as `/skill-name` slash commands in Copilot Chat and are auto-loaded by Copilot agents based on their `description` field.

Required frontmatter:

```yaml
---
name: <skill-name>          # kebab-case, MUST match directory name
description: "<one-liner>"  # double-quoted — used for Copilot discovery and our catalog. Max 1024 chars.
mode: <ask | agent>         # CUSTOM FIELD — not a Copilot-native skill field; read by generate_catalog.py
                            # Copilot ignores it; do NOT remove it
---
```

Body is the full skill instruction content — free-form, no required sections.
No domain subdirectory — skills live flat under `.github/skills/`.
`generate_catalog.py` indexes this directory and includes skills in the catalog.

### 4.5 Script (`scripts/<domain>/<action>.py`)

Required:
- snake_case filename (`create_work_items.py`, not `create-work-items.py`)
- `typer` CLI entry point with a `main()` or `app()` function
- Type-annotated public functions
- `rich.console.Console` for output (never bare `print()`)
- Loads secrets from environment via `python-dotenv` — never hardcoded

Standard skeleton:

```python
"""<one-paragraph purpose>."""

from pathlib import Path
import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main(input_path: Path = typer.Option(..., help="…")) -> None:
    """<short docstring>."""
    ...


if __name__ == "__main__":
    app()
```

If a script reads or writes Unicode glyphs through `rich`, the script must call `sys.stdout.reconfigure(encoding="utf-8")` at the top — Windows cp1252 shells crash otherwise. The three repo scripts (`validate_skill.py`, `validate_agent.py`, `generate_catalog.py`) demonstrate the pattern.

---

## 5. Naming conventions

| Type | Convention | Example |
|---|---|---|
| Skill folder | `<action>` kebab-case | `create-work-items/` |
| Skill file | always `SKILL.md` | `SKILL.md` |
| Agent file | `<role>.agent.md` kebab-case | `ado-manager.agent.md` |
| Python script | `<action>_<noun>.py` snake_case | `create_work_items.py` |
| Python function | snake_case | `build_patch_document()` |
| Python type | PascalCase | `WorkItemSpec` |
| Terraform resource | snake_case | `azurerm_resource_group.main` |
| Terraform tag values | snake_case | `managed_by = "terraform"` |

**Why kebab vs snake**: filenames/folders that are user-visible (skill names appear as `/foo-bar` slash commands) use kebab-case. Python identifiers stay snake_case because Python convention. The Python file *names* follow snake_case so imports work cleanly.

---

## 6. Domains

There are **9 valid domains** (enforced by `validate_skill.py`):

| Domain | Covers | Example skills |
|---|---|---|
| `ado` | Azure DevOps — work items, sprints, pipelines, PRs | `create-work-items`, `sprint-planning` |
| `office` | PowerPoint, Word, Excel, non-tech outputs | `ppt-from-outline`, `word-doc`, `excel-report` |
| `devops` | CI/CD, GitHub Actions, ADO Pipelines, git workflows | `pr-description`, `commit-message`, `gh-actions-workflow` |
| `data-ml` | Schemas, pipelines, model cards, experiment tracking | `schema-docs`, `pipeline-docs`, `model-card` |
| `infra` | Terraform, cloud infra, architecture diagrams, infra runbooks | `terraform-module`, `arch-diagram`, `incident-runbook` |
| `comms` | Teams, Outlook, meeting minutes, stakeholder updates | `email-draft`, `meeting-minutes`, `teams-announcement` |
| `coding` | Code review, test generation, task planning | `code-review`, `plan-task`, `write-tests` |
| `docs` | Technical documentation — READMEs, ADRs, API docs, doc-style runbooks | `write-readme`, `write-adr`, `write-runbook` |
| `meta` | Repo self-maintenance — scaffold, validate, catalog | `add-skill`, `add-agent`, `update-catalog`, `validate-skill` |

**Adding a new domain** is a deliberate change: update `VALID_DOMAINS` in `scripts/repo/validate_skill.py`, `DOMAIN_ORDER` and `DOMAIN_LABELS` in `scripts/repo/generate_catalog.py`, the domain list in `.claude/skills/meta/add-skill/SKILL.md`, the domain list in `.claude/skills/meta/new-skill/SKILL.md`, and `README.md` / `CONTRIBUTING.md` tables. The agent-skill-manager's job description includes flagging when this is needed.

### Overlapping domains

Some skills could fit two domains. Resolve by **primary user**:
- `incident-runbook` (in `infra`) — written by the operator who diagnoses
- `write-runbook` (in `docs`) — written by the doc author for long-lived reference

Both produce similar Markdown but are owned by different agents (`devops-engineer` vs `doc-writer`). Keep them separate unless you're explicitly consolidating.

---

## 7. Validators and the catalog

Three Python tools maintain repo integrity. **Always run them in order** when changing skills or agents.

### `scripts/repo/validate_skill.py`

```bash
python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>
```

Checks:
- Folder name is kebab-case
- Folder is inside a valid domain
- `SKILL.md` exists with required frontmatter (`name`, `description`, `domain`, `requires_script`)
- `name` matches folder name
- All three required body sections present (`## Usage`, `## Output`, `## Steps`)
- If `requires_script: true`, the `script:` path exists on disk
- No secret patterns (PAT, password, token literals) in the file

Exits 0 on pass, 1 on fail.

### `scripts/repo/validate_agent.py`

```bash
python scripts/repo/validate_agent.py .claude/agents/<name>.agent.md
python scripts/repo/validate_agent.py .github/agents/<name>.agent.md
```

Checks:
- Filename ends `.agent.md` and stem is kebab-case
- Required frontmatter — Claude needs `name` + `description`; Copilot needs `description` only
- Body length > 50 chars
- Claude agents: `skills:` is a list of `domain/skill-name` strings; each resolves to a real `SKILL.md`
- Both: `## Relevant Skills` body section exists
- No secret patterns

WARNs (exit 0) when `skills:` is missing entirely on a Claude agent — preferred to either populate or set `skills: []` explicitly.

### `scripts/repo/generate_catalog.py`

```bash
python scripts/repo/generate_catalog.py
```

Scans `.claude/skills/`, `.claude/agents/`, `.github/prompts/` and writes `docs/automation-catalog.md`. **Never edit `docs/automation-catalog.md` by hand** — it gets overwritten on next run.

The catalog is the user-facing skill/agent/prompt directory. Keep it fresh: any time skill/agent/prompt counts, names, or descriptions change, run this script before opening a PR.

---

## 8. Standard workflows

### 8.1 Add a new skill

1. Choose `<domain>` (one of the 9) and a kebab-case `<name>`.
2. Decide if it needs a Python script. If yes, create `scripts/<domain>/<action>.py` first.
3. Create `.claude/skills/<domain>/<name>/SKILL.md` with full frontmatter and the three required body sections fully populated (no placeholders).
4. Run `python scripts/repo/validate_skill.py .claude/skills/<domain>/<name>`. Fix any errors and re-run.
5. Add the skill to at least one agent's `skills:` frontmatter and `## Relevant Skills` body — both Claude and Copilot pair members.
6. Re-run `validate_agent.py` on the agents you touched.
7. If a Copilot equivalent makes sense, create `.github/prompts/<name>.prompt.md`.
8. Run `python scripts/repo/generate_catalog.py`.
9. Open a PR using the template at `.github/pull_request_template.md`.

The `agent-skill-manager` agent can run all of this for you in one pass — invoke it with `/add-skill` (Claude) or `/add-skill` (Copilot prompt).

### 8.2 Add a new agent (pair)

1. Pick a kebab-case `<name>` not in use under either `.claude/agents/` or `.github/agents/`.
2. Identify which existing skills are relevant (scan `.claude/skills/<domain>/`). If none exist yet, plan to create them in the same PR.
3. Write `.claude/agents/<name>.agent.md`:
   - `name` + `description` + `skills:` frontmatter
   - Body covering capabilities, workflow, boundaries
   - `## Relevant Skills` section listing each `SKILL.md` path
4. Write `.github/agents/<name>.agent.md`:
   - `description` + `tools:` frontmatter (no `skills:` key — Copilot doesn't parse it)
   - Same body content adapted for Copilot
   - `## Relevant Skills` section mirroring the Claude version
5. Run `validate_agent.py` on **both** files. Fix until both pass.
6. Run `generate_catalog.py`.
7. Update `README.md` if the agent table needs a new row (under the `## Agent Modes` section and `## Agent Prerequisites` if the agent has external deps).

The `/add-agent` skill (Claude) and `/add-agent` prompt (Copilot) automate this.

### 8.3 Add a Copilot prompt (no skill counterpart needed)

1. Create `.github/prompts/<name>.prompt.md` with `mode` + `description` frontmatter.
2. `mode: ask` for analysis/output prompts that don't read or write files; `mode: agent` for prompts that must read/write the workspace.
3. Body is the brief Copilot follows. No required sections.
4. Run `generate_catalog.py`.

### 8.4 Add a script

1. Choose the right `scripts/<domain>/` subdirectory.
2. snake_case filename ending in `.py`.
3. Follow the standard skeleton in §4.5 above.
4. If the script generates Unicode console output, add the `sys.stdout.reconfigure(encoding="utf-8")` line at module top.
5. Add deps to `configs/envs/conda-env.yml` if any are new.
6. Test by running locally with realistic inputs.
7. Reference it from a SKILL.md (`requires_script: true` + `script: <path>`) — a script with no skill wrapper is rarely useful.
8. Update the `## Python Scripts` example block in README.md if the script is user-facing.

### 8.5 Modify an existing entry

| Change | Steps |
|---|---|
| Skill name (folder rename) | Rename folder + update `name:` frontmatter + update every agent's `skills:` and `## Relevant Skills` referencing it + run validators + regen catalog |
| Skill description | Update SKILL.md → regen catalog |
| Skill body content | Update SKILL.md → no validator changes needed unless a required section changed → regen catalog |
| Agent name | Rename both `.claude/` and `.github/` files + update `name:` frontmatter (Claude) + update README agent table + regen catalog |
| Agent skills list | Update both `skills:` frontmatter (Claude) and `## Relevant Skills` (both pair members) → run `validate_agent.py` on both |
| Script signature/path | Update SKILL.md `script:` field if path changed → run `validate_skill.py` |
| Domain added | Update `validate_skill.py` `VALID_DOMAINS`, `generate_catalog.py` `DOMAIN_ORDER` + `DOMAIN_LABELS`, `add-skill` SKILL.md, `new-skill` SKILL.md, README, CONTRIBUTING |

### 8.6 Decommission an entry

1. Identify all references: grep for the skill/agent/prompt name across `.claude/`, `.github/`, `scripts/`, `README.md`, `CONTRIBUTING.md`, `PROGRESS.md`, `INSTRUCTIONS.md`.
2. Remove the file(s).
3. Remove every reference. Validators will fail loudly if you miss an agent's `skills:` entry.
4. Regenerate catalog.

---

## 9. Coding standards

The full Python contract lives in `.github/instructions/python.instructions.md`. Summary:

- Python 3.11+, type-annotated signatures
- `typer` for CLIs, `rich` for output, `httpx` for HTTP, `pathlib.Path` for paths
- `python-dotenv` for secrets — never hardcoded
- Functions under 40 lines; extract helpers rather than nesting
- snake_case names, descriptive variables, no commented-out code
- pytest tests alongside the code; mock external dependencies

ADO and Terraform have their own instruction files (`.github/instructions/ado.instructions.md`, `.github/instructions/terraform.instructions.md`).

The `code-reviewer` agent uses these as the review checklist. The `coder` agent applies them when writing.

---

## 10. MCP servers and what to assume

Per the local setup in `configs/mcp/local/README.md`, three MCP servers are documented:

| Server | Purpose | Required env vars |
|---|---|---|
| `azure-devops` | ADO work items, sprints, boards, pipelines | `ADO_ORG_URL`, `ADO_PAT` |
| `github` | PRs, issues, diffs, repo contents | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| `ms-graph` | Outlook, SharePoint, OneDrive, Teams | `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` |

**What to assume in skill/prompt copy:**
- Don't assume the user has any MCP server running. Always offer a fallback (paste-the-output flow, or "save as Markdown") when an MCP call would otherwise be the only path.
- Skills reference MCP tools by name only (`azure-devops/*`). The skill text doesn't change when the team migrates from local to centralised MCP.
- If a skill's text says "post to Confluence" or "save to SharePoint", remember: there is currently no skill or script that wraps these. Either implement the integration or remove the offer.

---

## 11. Pre-PR checklist (mandatory)

Before considering any change "done":

- [ ] Naming follows kebab-case (skills, agents, prompts) or snake_case (Python)
- [ ] If you added a skill: `validate_skill.py` passes
- [ ] If you added/changed an agent: both `validate_agent.py` runs (Claude + Copilot) pass
- [ ] If you changed any frontmatter, name, or description: `generate_catalog.py` ran and `docs/automation-catalog.md` is up to date
- [ ] If you added a script: it's referenced from at least one SKILL.md
- [ ] No secrets, PATs, tokens, or connection strings in any committed file
- [ ] Every cross-reference resolves: skill paths in agents, script paths in SKILL.mds, README counts
- [ ] PR template at `.github/pull_request_template.md` filled in

The PR template auto-checks most of this. The validators and `generate_catalog.py` are quick — run them.

---

## 12. Things never to do

- **Never edit `docs/automation-catalog.md` by hand.** It is regenerated and your changes will be lost.
- **Never commit secrets.** `.gitignore` covers `.env`, `*.pem`, `*.key`. If in doubt, don't.
- **Never add a domain without updating the validator.** It will silently break `add-skill`.
- **Never break the agent pair invariant.** A new agent must add **both** `.claude/agents/X.agent.md` **and** `.github/agents/X.agent.md` in the same PR.
- **Never reference a skill in `skills:` frontmatter without creating its `SKILL.md` first.** The validator will fail.
- **Never bypass the validators with `--no-verify` or skip-flag commits.** If a hook fails, fix the underlying issue.
- **Never rename a skill, agent, or domain in isolation.** Find every reference (grep across `.claude/`, `.github/`, `scripts/`, `README.md`, `CONTRIBUTING.md`, `PROGRESS.md`, `INSTRUCTIONS.md`) and update each.
- **Never invent capabilities in skill/agent text.** If a skill says "posts to Slack", a Slack integration must exist. Aspirational copy misleads users.
- **Never delete `INSTRUCTIONS.md`, `CLAUDE.md`, `copilot-instructions.md`, or `pull_request_template.md`** without team-wide alignment.
- **Never push to `main` directly** for any contribution covered by the PR workflow in `CONTRIBUTING.md`.

---

## 13. How to update this file

`INSTRUCTIONS.md` describes the contract for working in the repo. It changes when the contract changes — not on every PR.

### Trigger this file's update when

- A new domain is added or removed
- A new primitive type is added (e.g., a new MCP-config layer, a new agent class)
- A frontmatter or section requirement changes in any validator
- A new validator or generator script is added
- A directory is renamed or restructured
- The wiring rules between skills/agents/prompts/scripts change
- The pre-PR checklist or "never do" list materially changes
- A standard workflow gains or loses a required step

### Do **not** update this file for

- Adding individual skills, agents, prompts, or scripts (the catalog covers these)
- Tweaking a skill's body content or output format
- Renaming a single skill (unless it's a `meta/*` skill referenced here)
- Changing prompt copy
- Bumping dependency versions

### Update process

1. Make the structural change first (validator, directory, script, etc.).
2. Run all validators and the catalog generator to confirm the new state is consistent.
3. Update `INSTRUCTIONS.md`:
   - Edit the relevant section directly
   - Update the Table of Contents if a section was added or removed
   - Update the dated "Counts as of …" line in §2 if you changed counts
4. Update **all** of the following downstream pointers if they reference the changed contract:
   - `.claude/CLAUDE.md` — the project-level Claude system prompt
   - `.github/copilot-instructions.md` — the Copilot equivalent
   - `README.md` — anything in §"Repo Structure", §"Naming Conventions", §"Architecture Decisions"
   - `CONTRIBUTING.md` — anything in §"Adding a Skill", §"Adding an Agent", §"Agent Required Structure", §"SKILL.md Required Sections", §"PR Checklist"
   - `.claude/skills/meta/add-skill/SKILL.md` and `add-agent/SKILL.md` and `new-skill/SKILL.md` and `new-agent/SKILL.md` if their workflow text needs to match
   - `.github/prompts/add-skill.prompt.md` and `add-agent.prompt.md` likewise
   - `.claude/agents/agent-skill-manager.agent.md` and `.github/agents/agent-skill-manager.agent.md` if their validation rules section needs to match
5. Run `python scripts/repo/generate_catalog.py` once more in case any frontmatter changed.
6. Open a PR titled `chore(meta): update INSTRUCTIONS.md for <reason>` with a short description of what structural change triggered the update.
7. Reviewers: check that downstream pointers are in sync — this is the single highest-leverage review on a meta-PR.

### When this file disagrees with another file

This file wins. Fix the other file in the same PR. The point of having `INSTRUCTIONS.md` is to have one canonical place; if every other file is allowed to drift, you're back where you started.

If a future change makes a section here genuinely wrong (not just stale), update this file in the same PR as the change. Don't leave behind a "TODO: this section is outdated" — fix it.

### What to **not** put in this file

- Specific skill, agent, or prompt names beyond a handful of canonical examples (the catalog handles individual entries)
- Code snippets longer than a small skeleton (link out to actual files)
- Counts you'll forget to update (the §2 "as of …" line is the deliberate exception, dated so its staleness is obvious)
- Decisions that aren't enforced by a validator, script, or required section
- Process for things humans handle out-of-band (sprint planning, retros, comms)

If a section is becoming a stale narrative rather than enforceable contract, cut it.
