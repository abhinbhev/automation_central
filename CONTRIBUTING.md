# Contributing

Anyone on the team can add a new automation. Here's the process.

> Working with an AI agent (Claude Code, Copilot)? Point it at [`INSTRUCTIONS.md`](INSTRUCTIONS.md) first — that file holds the full operating contract (wirings, validators, file structures). This file is the human contributor's quick guide.

## Branching

```
main              ← stable, always works
skill/<name>      ← new or updated skill
agent/<name>      ← new or updated agent
script/<name>     ← new or updated script
fix/<description> ← bug fix
```

Branch from `main`, open a PR back to `main`, get one reviewer.

## Adding a Skill (Claude Code)

1. Create a folder under `.claude/skills/<domain>/<skill-name>/`
2. Add a `SKILL.md` file — use the scaffold skill to generate a stub:
   - In Claude Code, type `/new-skill` and follow the prompts
   - Or copy the template from `.claude/skills/meta/new-skill/SKILL.md`
3. If the skill needs a Python script, add it under `scripts/<domain>/`
4. Run the validator:
   ```bash
   python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>
   ```
5. Regenerate the catalog:
   ```bash
   python scripts/repo/generate_catalog.py
   ```
6. Open a PR — fill in the PR template

## Adding an Agent (Claude Code + Copilot)

1. Add **both** files simultaneously:
   - `.claude/agents/<name>.agent.md` — frontmatter: `name`, `description`, `skills: [domain/name, ...]`
   - `.github/agents/<name>.agent.md` — frontmatter: `description`, `tools: [...]`
2. Use `/add-agent` skill to scaffold (handles both files, skills linking, validation), or copy an existing agent as reference
3. Identify relevant skills by scanning `.claude/skills/<domain>/` — add them to:
   - `skills:` frontmatter in the Claude agent (format: `domain/skill-name`)
   - `## Relevant Skills` section in **both** agent files (full SKILL.md paths)
4. Run validators on both files:
   ```bash
   python scripts/repo/validate_agent.py .claude/agents/<name>.agent.md
   python scripts/repo/validate_agent.py .github/agents/<name>.agent.md
   ```
5. Regenerate catalog: `python scripts/repo/generate_catalog.py`
6. Open a PR

## Adding a Copilot Skill

1. Create `.github/skills/<action>/SKILL.md`
2. Follow naming: `<action>` (kebab-case, no domain prefix needed)
3. Set `mode: ask` for review/analysis skills; `mode: agent` for skills that read/write files
4. Frontmatter: `name` (matches folder), `description` (double-quoted with `"..."`), `mode`
5. Body: full skill instruction content
6. Test in Copilot Chat (`/` autocomplete) before opening a PR

## Agent Required Structure

Every `.agent.md` pair must contain:

**Claude Code** (`.claude/agents/<name>.agent.md`):
```markdown
---
name: <name>                   # matches filename stem
description: <one-liner>
skills:                        # list relevant skills as domain/skill-name
  - ado/create-work-items
---

## Capabilities
...

## Boundaries
...

## Relevant Skills

Read these skill definitions at the start of every session:

- `.claude/skills/ado/create-work-items/SKILL.md`
```

**Copilot** (`.github/agents/<name>.agent.md`):
```markdown
---
description: <one-liner>
tools: [read, edit, ...]
---

## Capabilities
...

## Boundaries
...

## Relevant Skills

Read these skill definitions at the start of every session:

- `.claude/skills/ado/create-work-items/SKILL.md`
```

## SKILL.md Required Sections

**Claude Code** (`.claude/skills/<domain>/<name>/SKILL.md`):

```markdown
---
name: <skill-name>          # matches folder name
description: <one-liner>    # shown in catalog
domain: <ado|office|devops|data-ml|infra|comms|coding|meta|docs>
requires_script: <true|false>
---

## Usage
<!-- How to invoke, what input to provide -->

## Output
<!-- What the skill produces -->

## Steps
<!-- What the skill does, step by step -->
```

**Copilot** (`.github/skills/<name>/SKILL.md`):

```markdown
---
name: <skill-name>          # matches folder name, no domain prefix
description: "<one-liner>"  # double-quoted
mode: <ask|agent>           # ask = analysis only; agent = reads/writes files
---

<!-- Full skill instruction content — free-form, no required sections -->
```

## PR Checklist

- [ ] Skill/agent follows naming conventions (kebab-case)
- [ ] `SKILL.md` has all required sections
- [ ] Agent has `skills:` frontmatter and `## Relevant Skills` section in both `.claude/` and `.github/` files
- [ ] Each `skills:` entry resolves to a real SKILL.md on disk
- [ ] Validator passes (`validate_skill.py` or `validate_agent.py`)
- [ ] Catalog regenerated (`generate_catalog.py`)
- [ ] No secrets or credentials committed
- [ ] Tested end-to-end at least once

## Naming Conventions

See [README.md#naming-conventions](README.md#naming-conventions) for the full reference.

| Item | Convention | Example |
|------|-----------|---------|
| Skill folders | `kebab-case` | `create-work-items` |
| Copilot Skill folders | `kebab-case` | `create-work-items` |
| Agent files | `kebab-case.agent.md` | `ado-manager.agent.md` |
| Python scripts | `snake_case.py` | `create_work_items.py` |
| Python functions | `snake_case` | `build_patch_document()` |
| Terraform resources | `snake_case` | `azurerm_resource_group.main` |

## Review Criteria

Reviewers check:
1. Does it actually work? (test evidence in PR)
2. Is the SKILL.md clear enough that a teammate can use it without asking?
3. No secrets or sensitive data committed
4. Naming follows conventions
5. Catalog is up to date

## Key Commands

```bash
# Validate a skill before PRing
python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>

# Validate an agent file
python scripts/repo/validate_agent.py .claude/agents/<name>.agent.md

# Rebuild the automation catalog
python scripts/repo/generate_catalog.py
```
