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
- **Relevant skills** — which existing skills (by `domain/name`) apply to this agent? (scan `.claude/skills/`)
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
skills:
  - domain/skill-name
  - domain/skill-name
---

You are a [role] specialist for a cross-functional engineering team at ABI.

## Capabilities
- ...

## Workflow
1. ...

## Boundaries
- ...

## Relevant Skills

Read these skill definitions at the start of every session:

- `.claude/skills/domain/skill-name/SKILL.md`
- `.claude/skills/domain/skill-name/SKILL.md`
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

## Relevant Skills

Read these skill definitions at the start of every session:

- `.claude/skills/domain/skill-name/SKILL.md`
- `.claude/skills/domain/skill-name/SKILL.md`
```

## Steps

1. Collect all required details — ask for any that are missing
2. Check the name is `kebab-case` (lowercase, hyphens only, no underscores)
3. Check for naming conflicts: scan `.claude/agents/` and `.github/agents/` for existing files
4. Ask which existing skills are relevant — scan `.claude/skills/<domain>/` for each applicable domain
5. **Write both agent files in the same operation — never create or update one without the other:**
   - `.claude/agents/<name>.agent.md`: `skills:` frontmatter, body with capabilities/workflow/boundaries, `## Relevant Skills` section
   - `.github/agents/<name>.agent.md`: Copilot frontmatter schema (no `skills:`), same body content, `## Relevant Skills` section mirroring the Claude agent
6. Run `python scripts/repo/validate_agent.py .claude/agents/<name>.agent.md`
7. Run `python scripts/repo/validate_agent.py .github/agents/<name>.agent.md`
8. If either validator reports errors → fix them and re-run until **both pass**
9. Run `python scripts/repo/generate_catalog.py`
10. Ask: "Should I create new skills for this agent?"
11. Report: paths created, both validator results, catalog item count

## Validation Checklist (enforced before completing)

- [ ] Agent name is kebab-case
- [ ] No naming conflict with existing agents
- [ ] `.claude/agents/<name>.agent.md` created with `name` + `description` frontmatter
- [ ] `.claude/agents/<name>.agent.md` has `skills:` frontmatter listing relevant skills as `domain/skill-name`
- [ ] `.claude/agents/<name>.agent.md` has `## Relevant Skills` body section
- [ ] `.github/agents/<name>.agent.md` created with `description` frontmatter
- [ ] `.github/agents/<name>.agent.md` has `## Relevant Skills` body section
- [ ] Both `name` values match their filename stems
- [ ] Both files have meaningful body content (capabilities + boundaries)
- [ ] Each `skills:` entry resolves to an existing SKILL.md on disk
- [ ] No secrets or credentials in either file
- [ ] Both validators pass with 0 errors
- [ ] Catalog regenerated after creation
