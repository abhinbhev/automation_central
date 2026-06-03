# PR-013 — Info Agent (Read-Only Repo Navigator)

**Phase:** 2 — Content Expansion
**Type:** New agent pair
**Story Points:** 3
**Priority:** P3 — Medium
**Depends on:** PR-005 (Copilot parity — agent should know about all skills)
**Blocks:** —

---

## Problem Statement

TODO #14 identifies the need for a read-only informational agent. New team members must read `README.md`, `INSTRUCTIONS.md`, `CONTRIBUTING.md`, and browse skill folders to understand what's available. This is a high-friction onboarding experience. Experienced users also need help finding the right skill for an unfamiliar task. An `info-agent` can answer "what skill should I use for X?" or "where do I find Y?" without having write access that could accidentally modify repo files.

The agent must be explicitly **read-only** — it has no `edit` or `execute` tools, making it safe for any team member to use without risk of unintended changes.

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `.claude/agents/info-agent.agent.md` and `.github/agents/info-agent.agent.md` |
| R2 | Claude agent: `tools` omitted or `tools: [read, search]` only — explicitly no `edit`, `execute`, or `write` |
| R3 | Copilot agent: `tools: [read, search]` only |
| R4 | Agent persona: answers questions about repo structure, skills catalog, agents, how to contribute, where to find resources |
| R5 | Agent explicitly refuses requests to create, edit, or delete files — redirects to `agent-skill-manager` |
| R6 | Agent explicitly refuses requests to run scripts — redirects to the appropriate domain agent |
| R7 | Agent reads `docs/automation-catalog.md` as its primary skill reference |
| R8 | Agent reads `INSTRUCTIONS.md` and `CONTRIBUTING.md` as its knowledge base |
| R9 | Both files pass `validate_agent.py` with zero errors |
| R10 | Agent skills list: empty (`skills: []`) — info-agent does not invoke other skills |

---

## User Stories

**US-1 — New team member**
> As a new team member, I want to ask "what can this repo do for me?" and get a structured overview of available automations, so I can start using the tools within my first day.

*Acceptance Criteria:*
1. Asking `info-agent` "what skills are available for ADO?" returns a summary of all ADO-domain skills with their descriptions.
2. Asking "how do I add a new skill?" returns the contribution workflow from `INSTRUCTIONS.md §8.1`.
3. Asking "what agent should I use for data work?" returns `data-engineer` with a brief description.

**US-2 — Existing user**
> As an existing user, I want to quickly find whether a skill exists for a specific task without browsing the catalog manually.

*Acceptance Criteria:*
1. Asking "is there a skill for generating release notes?" returns `/release-notes` with its description and invocation syntax.
2. Asking "how do I validate my new skill?" returns the `validate_skill.py` command.
3. Asking "can you create an ADO epic?" triggers a redirect: "I'm read-only — use the `ado-manager` agent for that."

**US-3 — Safety boundary**
> As a team lead, I want to be confident that `info-agent` can never accidentally modify files, so I can recommend it to non-technical users.

*Acceptance Criteria:*
1. Asking `info-agent` to "create a skill for me" returns a refusal and a pointer to `agent-skill-manager`.
2. The agent's `tools:` frontmatter does not include `edit`, `execute`, or `write`.
3. The agent body explicitly states its read-only constraint in a `## Boundaries` section.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Write `info-agent` persona outline — capabilities, knowledge sources, boundaries | Dev | 20m |
| T2 | Create `.claude/agents/info-agent.agent.md` with `skills: []` and read-only persona | Dev | 45m |
| T3 | Create `.github/agents/info-agent.agent.md` with `tools: [read, search]` | Dev | 30m |
| T4 | Run `validate_agent.py` on both files | Dev | 10m |
| T5 | Run `generate_catalog.py` | Dev | 5m |
| T6 | Run `sync_check.py` | Dev | 5m |
| T7 | Update `README.md` agent table | Dev | 10m |
| T8 | Add note in `CONTRIBUTING.md`: "Use `info-agent` to explore the repo before contributing" | Dev | 10m |

**Total estimate: ~2.5h → 3 story points**

---

## Agent Persona Outline

**Name:** `info-agent`
**Description:** Read-only repo navigator — answers questions about available skills, agents, contribution workflows, and where to find resources. Does not create, edit, or execute anything.

**Knowledge sources (read at session start):**
- `docs/automation-catalog.md` — primary skills/agents reference
- `INSTRUCTIONS.md` — structural rules and workflows
- `CONTRIBUTING.md` — how to contribute
- `README.md` — overview and setup

**Capabilities:**
- Explain what any skill does and how to invoke it
- Recommend the right agent for a given task
- Explain contribution workflows step-by-step
- Describe repo structure and naming conventions
- Point users to the right script or config file

**Boundaries:**
- Read and search only — never create, edit, or delete files
- Never run scripts or terminal commands
- Redirect file creation requests to `agent-skill-manager`
- Redirect domain task requests to the appropriate domain agent
- If unsure, recommend reading `INSTRUCTIONS.md` and offer to summarise relevant sections

---

## Acceptance Criteria (PR-level)

1. Both agent files exist and pass `validate_agent.py` with zero errors.
2. Neither file includes `edit`, `execute`, or `write` in its `tools:` list.
3. Both files have an explicit `## Boundaries` section stating read-only constraint.
4. `info-agent` appears in `docs/automation-catalog.md`.
5. Claude and Copilot `description` fields are identical.

---

## PR Title

`feat(meta): add info-agent — read-only repo navigator for onboarding and discovery`
