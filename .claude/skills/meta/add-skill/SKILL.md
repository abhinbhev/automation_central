---
name: add-skill
description: Create, validate, and register a new skill in one atomic workflow — scaffolds SKILL.md, runs the validator, fixes any errors, and updates the catalog. Handles both Claude Code skills (.claude/skills/) and Copilot Skills (.github/skills/)
domain: meta
requires_script: true
script: scripts/repo/validate_skill.py
---

## Usage

Invoke with `/add-skill` then specify **which type** of skill to create:

**Claude Code skill** — invoke with `/skill-name` in Claude Code chat, lives in `.claude/skills/<domain>/`:
- **Skill name** — kebab-case action (e.g. `sprint-report`)
- **Domain** — one of: `ado`, `office`, `devops`, `data-ml`, `infra`, `comms`, `coding`, `meta`, `docs`
- **One-line description** — shown in the catalog and used for discovery
- **Does it need a Python script?** — yes/no. If yes, provide the script path under `scripts/<domain>/`
- **Inputs** — what does the user need to provide when invoking the skill?
- **Output** — what does the skill produce?

**Copilot Skill** — invoke with `/skill-name` in Copilot Chat, lives in `.github/skills/<name>/`:
- **Skill name** — kebab-case action (e.g. `sprint-report`)
- **Mode** — `ask` (analysis/output only) or `agent` (reads/writes files)
- **One-line description** — quoted; used by Copilot for auto-discovery
- **Body** — full skill instruction content (free-form)

## Output

**Claude Code skill:**
1. `.claude/skills/<domain>/<skill-name>/SKILL.md` — fully populated, all required sections
2. Validator result: `python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>`
3. Catalog update: `python scripts/repo/generate_catalog.py`

**Copilot Skill:**
1. `.github/skills/<skill-name>/SKILL.md` — frontmatter + body
2. Catalog update: `python scripts/repo/generate_catalog.py`

SKILL.md structure for Claude Code:
```markdown
---
name: <skill-name>
description: <one-liner>
domain: <domain>
requires_script: <true|false>
[script: scripts/<domain>/<script_name>.py]  ← only if requires_script: true
---

## Usage

Invoke with `/<skill-name>` then provide:
- [inputs]

## Output

[What the skill produces]

## Steps

1. [Step 1]
2. [Step 2]
...
```

SKILL.md structure for Copilot:
```markdown
---
name: <skill-name>
description: "<one-liner>"
mode: <ask|agent>
---

[Full skill instruction content]
```

## Steps

### Creating a Claude Code skill

1. Collect all required details — ask for any that are missing
2. Check the name is `kebab-case` (lowercase, hyphens only, no underscores)
3. Check the domain is valid — if not, stop and flag it; do not create the folder
4. Check for naming conflicts: scan `.claude/skills/<domain>/` for an existing folder with the same name
5. If `requires_script: true`, verify the script path exists on disk before writing
6. Write `.claude/skills/<domain>/<skill-name>/SKILL.md` — all sections fully populated, no placeholder text
7. **SYNC RULE:** Also create or update `.github/skills/<skill-name>/SKILL.md` — `description` double-quoted, same behaviour, `mode` set appropriately
8. Run `python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>`
9. If the validator reports errors → fix each one and re-run until the result is **PASS**
10. Run `python scripts/repo/generate_catalog.py`
11. Report: paths created, validator result, catalog item count

### Creating a Copilot Skill

1. Collect: skill name, description, mode, body content
2. Check the name is `kebab-case`
3. Check for naming conflicts: scan `.github/skills/` for an existing folder with the same name
4. Write `.github/skills/<skill-name>/SKILL.md` — description must be double-quoted
5. **SYNC RULE:** Also create or update `.claude/skills/<domain>/<skill-name>/SKILL.md` if a Claude equivalent exists or should exist
6. Run `python scripts/repo/generate_catalog.py`
7. Report: paths created, catalog item count

### Updating an existing skill

- **Always update both** `.claude/skills/<domain>/<name>/SKILL.md` **and** `.github/skills/<name>/SKILL.md` in the same operation
- Re-run the validator on the Claude skill after any changes
- Re-run `generate_catalog.py`

## Validation Checklist

**Claude Code skill — all must pass:**
- [ ] Folder name is kebab-case
- [ ] Folder is inside a valid domain directory
- [ ] `SKILL.md` exists at the correct path
- [ ] Frontmatter has: `name`, `description`, `domain`, `requires_script`
- [ ] `name` in frontmatter matches folder name exactly
- [ ] `domain` value is in the allowed set
- [ ] All three sections present: `## Usage`, `## Output`, `## Steps`
- [ ] If `requires_script: true`, script path exists on disk
- [ ] No secrets or credentials in any field
- [ ] Validator passes, catalog regenerated

**Copilot Skill — all must pass:**
- [ ] Folder name is kebab-case, matches `name` in frontmatter
- [ ] `description` is double-quoted
- [ ] `mode` is `ask` or `agent`
- [ ] No `domain`, `requires_script`, or Claude-only sections in the file
- [ ] No secrets or credentials in any field
- [ ] Catalog regenerated
