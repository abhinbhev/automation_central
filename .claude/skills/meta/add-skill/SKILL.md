---
name: add-skill
description: Create, validate, and register a new skill in one atomic workflow — scaffolds SKILL.md, runs the validator, fixes any errors, and updates the catalog
domain: meta
requires_script: true
script: scripts/repo/validate_skill.py
---

## Usage

Invoke with `/add-skill` then provide:
- **Skill name** — kebab-case action (e.g. `sprint-report`). This becomes the folder name and the `/invoke` command
- **Domain** — one of: `ado`, `office`, `devops`, `data-ml`, `infra`, `comms`, `coding`, `meta`, `docs`
- **One-line description** — shown in the catalog and used for discovery
- **Does it need a Python script?** — yes/no. If yes, provide the script path under `scripts/<domain>/`
- **Inputs** — what does the user need to provide when invoking the skill?
- **Output** — what does the skill produce?

## Output

1. `.claude/skills/<domain>/<skill-name>/SKILL.md` — fully populated, all required sections
2. Validator result: `python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>`
3. Catalog update: `python scripts/repo/generate_catalog.py`

SKILL.md structure created:
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

## Steps

1. Collect all required details — ask for any that are missing
2. Check the name is `kebab-case` (lowercase, hyphens only, no underscores)
3. Check the domain is valid — if not, stop and flag it; do not create the folder
4. Check for naming conflicts: scan `.claude/skills/<domain>/` for an existing folder with the same name
5. If `requires_script: true`, verify the script path exists on disk before writing
6. Write `.claude/skills/<domain>/<skill-name>/SKILL.md` — all sections fully populated, no placeholder text
7. Run `python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>`
8. If the validator reports errors → fix each one and re-run until the result is **PASS**
9. Run `python scripts/repo/generate_catalog.py`
10. Report: path created, validator result, catalog item count

## Validation Checklist (enforced before completing)

- [ ] Folder name is kebab-case
- [ ] Folder is inside a valid domain directory
- [ ] `SKILL.md` exists at the correct path
- [ ] Frontmatter has: `name`, `description`, `domain`, `requires_script`
- [ ] `name` in frontmatter matches folder name exactly
- [ ] `domain` value is in the allowed set
- [ ] All three sections present: `## Usage`, `## Output`, `## Steps`
- [ ] If `requires_script: true`, script path exists on disk
- [ ] No secrets or credentials in any field
- [ ] Catalog regenerated after creation
