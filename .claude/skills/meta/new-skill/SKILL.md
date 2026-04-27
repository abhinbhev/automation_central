---
name: new-skill
description: Scaffold a new skill — creates the folder and a SKILL.md stub with all required fields
domain: meta
requires_script: false
---

## Usage

Invoke with `/new-skill` then provide:
- **Skill name** (will become the folder name and invoke command, e.g., `sprint-report`)
- **Domain** (`ado` / `office` / `devops` / `data-ml` / `infra` / `comms` / `coding` / `meta`)
- **One-line description** of what it does
- **Does it need a Python script?** (yes/no)
- **What inputs does the user provide?**
- **What output does the skill produce?**

## Output

Creates the following file at `.claude/skills/<domain>/<skill-name>/SKILL.md`:

```markdown
---
name: <skill-name>
description: <one-liner>
domain: <domain>
requires_script: <true|false>
---

## Usage

Invoke with `/<skill-name>` then provide:
- [Input 1]
- [Input 2]

## Output

[Description of what the skill produces]

## Steps

1. [Step 1]
2. [Step 2]
3. [Step 3]
```

## Steps

1. Collect the skill details from the user (ask if any are missing)
2. Validate the name follows `<action>` kebab-case convention
3. Validate the domain is one of the allowed values
4. Generate the SKILL.md content
5. Show it to the user for review
6. Confirm before writing the file
7. Remind the user to run `python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>` and `python scripts/repo/generate_catalog.py`
