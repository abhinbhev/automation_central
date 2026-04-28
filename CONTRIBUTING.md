# Contributing

Anyone on the team can add a new automation. Here's the process.

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

## Adding an Agent (Claude Code)

1. Add `.claude/agents/<name>.agent.md`
2. Use `/new-agent` skill to scaffold, or copy an existing agent as reference
3. Run: `python scripts/repo/validate_agent.py .claude/agents/<name>.agent.md`
4. Add matching Copilot version to `.github/agents/<name>.agent.md` if applicable
5. Open a PR

## Adding a Copilot Prompt

1. Add `.github/prompts/<name>.prompt.md`
2. Follow naming: `<domain>-<action>.prompt.md`
3. Test in Copilot Chat before PRing

## Adding a Copilot Prompt

1. Add `.github/prompts/<action>.prompt.md`
2. Follow naming: `<action>.prompt.md` (kebab-case, no domain prefix needed)
3. Set `mode: ask` for review/analysis prompts; `mode: agent` for prompts that read/write files
4. Test in Copilot Chat (`/` autocomplete) before opening a PR

## SKILL.md Required Sections

Every `SKILL.md` must contain:

```markdown
---
name: <skill-name>          # matches folder name
description: <one-liner>    # shown in catalog
domain: <ado|office|devops|data-ml|infra|comms|coding|meta>
requires_script: <true|false>
---

## Usage
<!-- How to invoke, what input to provide -->

## Output
<!-- What the skill produces -->

## Steps
<!-- What the skill does, step by step -->
```

## PR Checklist

- [ ] Skill/agent follows naming conventions (`<domain>-<action>`)
- [ ] `SKILL.md` has all required sections
- [ ] Validator passes (`validate_skill.py` or `validate_agent.py`)
- [ ] Catalog regenerated (`generate_catalog.py`)
- [ ] No secrets or credentials committed
- [ ] Tested end-to-end at least once
- [ ] Catalog regenerated: `python scripts/repo/generate_catalog.py`

## Naming Conventions

See [README.md#naming-conventions](README.md#naming-conventions) for the full reference.

| Item | Convention | Example |
|------|-----------|---------|
| Skill folders | `kebab-case` | `create-work-items` |
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
