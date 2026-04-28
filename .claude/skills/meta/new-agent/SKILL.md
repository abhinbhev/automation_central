---
name: new-agent
description: Scaffold a new agent — creates .agent.md stubs for both Claude Code and GitHub Copilot
domain: meta
requires_script: false
---

## Usage

Invoke with `/new-agent` then provide:
- **Agent name** (kebab-case, e.g., `data-engineer`)
- **Role description** — one sentence: what this agent specialises in
- **Capabilities** — bullet list of what it can do
- **Boundaries** — what it should NOT do (keeps scope clear)
- **Relevant skills** — which existing skills apply? (scan `.claude/skills/` to suggest)
- **Target framework**: Claude Code only / Copilot only / Both (default: both)

## Output

**Claude Code** `.claude/agents/<name>.agent.md`:
```markdown
---
name: <name>
description: <one-liner>
skills:
  - domain/skill-name
---

You are a [role] agent...

## Capabilities
...

## Boundaries
...

## Relevant Skills

Read these skill definitions at the start of every session:

- `.claude/skills/domain/skill-name/SKILL.md`
```

**Copilot** `.github/agents/<name>.agent.md`:
```markdown
---
description: <one-liner>
tools: [read, edit, ...]
---

You are a [role] agent...

## Capabilities
...

## Boundaries
...

## Relevant Skills

Read these skill definitions at the start of every session:

- `.claude/skills/domain/skill-name/SKILL.md`
```

## Steps

1. Collect agent details (ask for missing ones)
2. Check for naming conflicts with existing agents
3. Scan `.claude/skills/` to suggest relevant skills by domain
4. Generate both agent files with:
   - `skills:` frontmatter in the Claude agent
   - `## Relevant Skills` section in both files
5. Show both for review
6. Confirm before writing files
7. Remind the user to run:
   - `python scripts/repo/validate_agent.py .claude/agents/<name>.agent.md`
   - `python scripts/repo/validate_agent.py .github/agents/<name>.agent.md`
   - `python scripts/repo/generate_catalog.py`
