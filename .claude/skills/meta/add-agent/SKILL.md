---
name: add-agent
description: Create, validate, and register a new agent for both Claude Code and GitHub Copilot in one atomic workflow — scaffolds both .agent.md files, runs validators on each, and updates the catalog
domain: meta
requires_script: true
script: scripts/repo/validate_agent.py
---

## Usage

Invoke with `/add-agent` then provide:
- **Agent name** — kebab-case (e.g. `data-engineer`). Becomes the filename stem
- **Role description** — one sentence: what this agent specialises in (used as `description` frontmatter)
- **Capabilities** — bullet list of what the agent can do
- **Tools** — list of tools the agent needs (e.g. `[read, edit, search, execute, azure-devops/*]`)
- **Boundaries** — what the agent must NOT do (keeps scope clear, prevents overlap with other agents)
- **Target framework** — `both` (default) / `claude-only` / `copilot-only`

## Output

1. `.claude/agents/<name>.agent.md` — Claude Code agent with `name` + `description` frontmatter
2. `.github/agents/<name>.agent.md` — Copilot agent with `description` + `tools` frontmatter
3. Validator output for both files
4. Catalog update

Agent file structure:

**Claude Code** (`.claude/agents/<name>.agent.md`):
```markdown
---
name: <name>
description: <one-liner>
---

You are a [role] specialist for a cross-functional engineering team at ABI.

## Capabilities
- ...

## Workflow
1. ...

## Boundaries
- ...
```

**Copilot** (`.github/agents/<name>.agent.md`):
```markdown
---
description: <one-liner>
tools: [read, edit, ...]
---

You are a [role] specialist...

## Capabilities
...

## Boundaries
...
```

## Steps

1. Collect all required details — ask for any that are missing
2. Check the name is `kebab-case` (lowercase, hyphens only, no underscores)
3. Check for naming conflicts: scan `.claude/agents/` and `.github/agents/` for existing files
4. Write `.claude/agents/<name>.agent.md` — body must be >50 chars with capabilities and boundaries
5. Write `.github/agents/<name>.agent.md` — same content, adapted for Copilot frontmatter schema
6. Run `python scripts/repo/validate_agent.py .claude/agents/<name>.agent.md`
7. Run `python scripts/repo/validate_agent.py .github/agents/<name>.agent.md`
8. If either validator reports errors → fix them and re-run until **both pass**
9. Run `python scripts/repo/generate_catalog.py`
10. Ask: "Should I create matching skills or Copilot prompts for this agent?"
11. Report: paths created, both validator results, catalog item count

## Validation Checklist (enforced before completing)

- [ ] Agent name is kebab-case
- [ ] No naming conflict with existing agents
- [ ] `.claude/agents/<name>.agent.md` created with `name` + `description` frontmatter
- [ ] `.github/agents/<name>.agent.md` created with `description` frontmatter
- [ ] Both `name` values match their filename stems
- [ ] Both files have meaningful body content (capabilities + boundaries)
- [ ] No secrets or credentials in either file
- [ ] Both validators pass with 0 errors
- [ ] Catalog regenerated after creation
