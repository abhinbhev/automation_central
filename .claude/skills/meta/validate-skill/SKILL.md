---
name: validate-skill
description: Check that a skill folder and SKILL.md conform to repo standards
domain: meta
requires_script: true
script: scripts/repo/validate_skill.py
---

## Usage

Invoke with `/validate-skill` then provide:
- Path to the skill folder (e.g., `.claude/skills/ado/create-work-items`)

Or run directly:
```bash
python scripts/repo/validate_skill.py .claude/skills/<domain>/<skill-name>
```

## What is Validated

- [ ] Folder name is kebab-case
- [ ] Folder is inside a valid domain directory
- [ ] `SKILL.md` exists
- [ ] SKILL.md has required frontmatter: `name`, `description`, `domain`, `requires_script`
- [ ] `name` in frontmatter matches folder name
- [ ] `domain` is one of the allowed values
- [ ] SKILL.md has required sections: `## Usage`, `## Output`, `## Steps`
- [ ] If `requires_script: true`, the script path exists
- [ ] No secrets pattern detected in SKILL.md (PAT, password, token literals)

## Output

A pass/fail report:
```
✓ Folder name: create-work-items
✓ Domain: ado
✓ SKILL.md exists
✓ Frontmatter complete
✗ Missing section: ## Output
→ Add an ## Output section describing what the skill produces

Result: FAIL (1 error)
```

## Steps

1. Read the skill folder path
2. Run `scripts/repo/validate_skill.py <path>`
3. Report results
4. For each failure, explain what needs to be fixed
