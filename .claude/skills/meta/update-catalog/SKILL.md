---
name: update-catalog
description: Rebuild docs/automation-catalog.md by reading all SKILL.md and .agent.md files
domain: meta
requires_script: true
script: scripts/repo/generate_catalog.py
---

## Usage

Invoke with `/update-catalog` (no input required).

Or run directly:
```bash
python scripts/repo/generate_catalog.py
```

## Output

Overwrites the automation catalog in `README.md#automation-catalog` by running the generator script, which produces a fresh catalog containing:
- All Claude Code skills grouped by domain
- All Claude Code agents
- All GitHub Copilot prompts

## When to run

Run this after:
- Adding a new skill
- Adding a new agent
- Renaming or removing a skill/agent
- Changing a skill's `description` in its frontmatter

## Steps

1. Run `scripts/repo/generate_catalog.py`
2. The script scans `.claude/skills/`, `.claude/agents/`, and `.github/prompts/`
3. It reads frontmatter from each file
4. It writes `docs/automation-catalog.md`
5. Report how many items were found and whether the catalog was updated
