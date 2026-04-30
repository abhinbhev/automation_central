---
name: add-skill
description: "Create, validate, and register a new skill in automation_central — handles both Claude Code skills (.claude/skills/) and Copilot Skills (.github/skills/), scaffolds SKILL.md, runs the validator, fixes errors, and updates the catalog in one workflow"
mode: agent
---

Create a new skill in `automation_central`. First confirm **which type**:

- **Claude Code skill** — invoked as `/skill-name` in Claude Code, lives in `.claude/skills/<domain>/<name>/`
- **Copilot Skill** — invoked as `/skill-name` in Copilot Chat, lives in `.github/skills/<name>/`

---

## Claude Code Skill Workflow

**Provide:** skill name (kebab-case), domain, one-line description, whether a Python script is needed, inputs, output.

### 1. Pre-flight checks
- Name is `kebab-case`: if not, stop and correct it
- Domain is valid (`ado`, `office`, `devops`, `data-ml`, `infra`, `comms`, `coding`, `meta`, `docs`): if not, stop and flag
- No naming conflict: check `.claude/skills/<domain>/` for an existing folder with this name
- If `requires_script: true`: verify `scripts/<domain>/<script>.py` exists on disk

### 2. Create the SKILL.md

> **SYNC RULE:** Always create or update **both** the Claude and Copilot versions together:
> - Claude: `.claude/skills/<domain>/<skill-name>/SKILL.md`
> - Copilot: `.github/skills/<skill-name>/SKILL.md`
> Never leave one side stale.

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

Fix any errors and re-run until the result is **PASS**.

### 4. Update the catalog

```bash
python scripts/repo/generate_catalog.py
```

### 5. Report
- Path of file created
- Validator result (paste the output)
- Catalog item count after update

**Checklist — all must pass:**
- [ ] Folder name is kebab-case inside a valid domain directory
- [ ] Frontmatter: `name`, `description`, `domain`, `requires_script`
- [ ] `name` matches folder name exactly
- [ ] All three sections present: `## Usage`, `## Output`, `## Steps`
- [ ] Script path exists on disk (if `requires_script: true`)
- [ ] No secrets or credentials anywhere
- [ ] Catalog regenerated

---

## Copilot Skill Workflow

**Provide:** skill name (kebab-case), mode (`ask` or `agent`), one-line description, body content.

### 1. Pre-flight checks
- Name is `kebab-case`
- No naming conflict: check `.github/skills/` for an existing folder with this name

### 2. Create the SKILL.md

Write to `.github/skills/<skill-name>/SKILL.md`:

```markdown
---
name: <skill-name>
description: "<one-liner>"
mode: <ask|agent>
---

[Full skill instruction content]
```

- `description` **must be double-quoted**
- No `domain`, `requires_script`, or `## Usage`/`## Output`/`## Steps` sections

### 3. Update the catalog

```bash
python scripts/repo/generate_catalog.py
```

### 4. Report
- Path of file created
- Catalog item count after update

**Checklist — all must pass:**
- [ ] Folder name is kebab-case, matches `name` in frontmatter
- [ ] `description` is double-quoted
- [ ] `mode` is `ask` or `agent`
- [ ] No Claude-only frontmatter fields or required sections
- [ ] No secrets or credentials anywhere
- [ ] Catalog regenerated
