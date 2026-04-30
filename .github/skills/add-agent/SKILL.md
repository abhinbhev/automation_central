---
name: add-agent
description: "Create, validate, and register a new agent for both Claude Code and GitHub Copilot — scaffolds both .agent.md files, runs validators on each, and updates the catalog"
mode: agent
---

Create a new agent in `automation_central` for both Claude Code and GitHub Copilot.

**Provide:**
- **Agent name** — kebab-case, e.g. `data-engineer`
- **Role description** — one sentence: what this agent specialises in
- **Capabilities** — bullet list of what it can do
- **Tools** — list needed, e.g. `[read, edit, search, execute, azure-devops/*]`
- **Boundaries** — what it must NOT do (keeps scope clear)
- **Relevant skills** — which existing skills (by `domain/name`) apply? Scan `.claude/skills/` to suggest
- **Target framework** — `both` (default) / `claude-only` / `copilot-only`

---

## Workflow (execute every step — do not skip validation)

### 1. Pre-flight checks
- Name is `kebab-case`: if not, correct it first
- No naming conflict: check `.claude/agents/` and `.github/agents/` for existing files

### 2. Create both agent files simultaneously

> **SYNC RULE:** Both files must always be written together. Never create or update one without the other.

**`.claude/agents/<name>.agent.md`:**
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

**`.github/agents/<name>.agent.md`:**
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

Both files must have:
- Meaningful body content (capabilities + boundaries) — not just stubs
- A `## Relevant Skills` section listing each linked skill's full path
- Each `skills:` entry (Claude only) must resolve to a real `SKILL.md` on disk
- No secrets or credentials

### 3. Validate both files

```bash
python scripts/repo/validate_agent.py .claude/agents/<name>.agent.md
python scripts/repo/validate_agent.py .github/agents/<name>.agent.md
```

If any errors are reported → fix them and re-run until **both pass**.

### 4. Update the catalog

```bash
python scripts/repo/generate_catalog.py
```

### 5. Offer to continue

Ask: "Should I also create matching skills or Copilot prompts for this agent?"

### 6. Report

Output:
- Paths of files created
- Validator results for both files (paste output)
- Catalog item count after update

---

**Validation checklist — all must pass before this task is complete:**
- [ ] Agent name is kebab-case
- [ ] No naming conflict with existing agents
- [ ] `.claude/agents/<name>.agent.md` created — `name` + `description` frontmatter present
- [ ] `.claude/agents/<name>.agent.md` has `skills:` frontmatter listing relevant skills as `domain/skill-name`
- [ ] `.claude/agents/<name>.agent.md` has a `## Relevant Skills` body section
- [ ] `.github/agents/<name>.agent.md` created — `description` frontmatter present
- [ ] `.github/agents/<name>.agent.md` has a `## Relevant Skills` body section mirroring the Claude agent
- [ ] Each `skills:` entry resolves to an existing SKILL.md on disk
- [ ] `name` matches the filename stem (Claude agent)
- [ ] Both files have capabilities and boundaries defined
- [ ] No secrets or credentials in either file
- [ ] Both validators pass with 0 errors
- [ ] Catalog regenerated
