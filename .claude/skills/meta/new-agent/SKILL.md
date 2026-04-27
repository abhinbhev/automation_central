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
- **Target framework**: Claude Code only / Copilot only / Both (default: both)

## Output

**Claude Code** `.claude/agents/<name>.agent.md`:
```markdown
---
name: <name>
description: <one-liner>
---

You are a [role] agent...

## Capabilities
...

## Boundaries
...
```

**Copilot** `.github/agents/<name>.agent.md`:
Equivalent content formatted for Copilot's agent schema.

## Steps

1. Collect agent details (ask for missing ones)
2. Check for naming conflicts with existing agents
3. Generate both stubs
4. Show for review
5. Confirm before writing files
6. Remind the user to run `python scripts/repo/validate_agent.py .claude/agents/<name>.agent.md`
