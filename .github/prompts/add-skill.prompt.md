---
mode: agent
description: Create, validate, and register a new skill in automation_central — scaffolds SKILL.md, runs the validator, fixes errors, and updates the catalog in one workflow
---

Create a new skill in `automation_central` following the full creation + validation workflow.

**Provide:**
- **Skill name** — kebab-case action, e.g. `sprint-report` (becomes the folder name and `/invoke` command)
- **Domain** — one of: `ado`, `office`, `devops`, `data-ml`, `infra`, `comms`, `coding`, `meta`, `docs`
- **One-line description** — shown in the catalog
- **Needs a Python script?** — yes/no. If yes, the script path under `scripts/<domain>/`
- **Inputs** — what the user provides when invoking
- **Output** — what the skill produces

---

## Workflow (execute every step — do not skip validation)

### 1. Pre-flight checks
- Name is `kebab-case` (lowercase, hyphens only): if not, stop and correct it
- Domain is valid: if not, stop and flag — do not create the folder
- No naming conflict: check `.claude/skills/<domain>/` for an existing folder with this name
- If `requires_script: true`: verify `scripts/<domain>/<script>.py` exists on disk

### 2. Create the SKILL.md

Write to `.claude/skills/<domain>/<skill-name>/SKILL.md`:

```markdown
---
name: <skill-name>
description: <one-liner>
domain: <domain>
requires_script: <true|false>
[script: scripts/<domain>/<script>.py]
---

## Usage

Invoke with `/<skill-name>` then provide:
- [inputs]

## Output

[What the skill produces]

## Steps

1. [Step 1]
2. [Step 2]
```

All sections must be fully populated — no placeholder text.

### 3. Validate

```bash
python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>
```

If any errors are reported → fix them and re-run until the result is **PASS**.

### 4. Update the catalog

```bash
python scripts/repo/generate_catalog.py
```

### 5. Report

Output:
- Path of file created
- Validator result (paste the output)
- Catalog item count after update

---

**Validation checklist — all must pass before this task is complete:**
- [ ] Folder name is kebab-case
- [ ] Folder is inside a valid domain directory
- [ ] `SKILL.md` exists at the correct path
- [ ] Frontmatter has: `name`, `description`, `domain`, `requires_script`
- [ ] `name` matches folder name exactly
- [ ] All three sections present: `## Usage`, `## Output`, `## Steps`
- [ ] Script path exists (if `requires_script: true`)
- [ ] No secrets or credentials anywhere in the file
- [ ] Catalog regenerated
