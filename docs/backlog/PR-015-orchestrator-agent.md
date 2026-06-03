# PR-015 — Orchestrator Agent

**Phase:** 3 — Intelligence & Self-Improvement
**Type:** New agent pair + meta skill
**Story Points:** 8
**Priority:** P3 — Medium
**Depends on:** PR-011 (data-engineer), PR-012 (teams/outlook), PR-013 (info-agent) — orchestrator is most useful when the full agent set exists
**Blocks:** —

---

## Problem Statement

TODO #6 identifies the need for an overall orchestrator agent. Currently, users must know which domain agent to select before starting a session. Cross-domain tasks (e.g., "document this feature, create ADO stories for it, and send a Teams announcement when done") require manual agent switching. An `orchestrator` agent reads the intent, decomposes it, delegates to domain agents, and coordinates the result — without the user needing to understand the agent topology.

**Key design constraints:**
- The orchestrator does not implement domain logic itself — it delegates.
- It must prevent infinite delegation loops (no agent-to-agent calls that cycle back).
- It reads the full catalog at session start to know what is available.
- It asks for confirmation before any irreversible action (ADO creation, sending messages).

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `.claude/agents/orchestrator.agent.md` and `.github/agents/orchestrator.agent.md` |
| R2 | Agent reads `docs/automation-catalog.md` at session start |
| R3 | Agent decomposes multi-step requests into subtasks and maps each to an agent or skill |
| R4 | Agent presents a delegation plan before executing: "I'll use X for step 1, Y for step 2" |
| R5 | Agent requests confirmation before any action that modifies ADO, sends messages, or writes files |
| R6 | Agent explicitly lists domains it does NOT handle directly (redirects to domain agents) |
| R7 | Agent has a circuit-breaker boundary: if it cannot confidently map a subtask to an agent, it says so and asks the user to clarify |
| R8 | Boundaries include: "Never call another orchestrator" and "Never bypass confirmation for irreversible actions" |
| R9 | Both agents pass `validate_agent.py` |
| R10 | New meta skill: `meta/orchestrate` — usage instructions for the orchestrator (Claude + Copilot) |
| R11 | Catalog and sync check clean |

---

## User Stories

**US-1 — Power user with a cross-domain task**
> As a senior engineer, I want to give the orchestrator a natural language description of a multi-step workflow and have it figure out which agents and skills to use, so I don't need to context-switch manually.

*Acceptance Criteria:*
1. Given "document this Python module, create ADO stories for the next sprint, and draft a Teams announcement": the orchestrator identifies 3 subtasks, maps them to `doc-writer`, `ado-manager`, and `teams-manager` respectively.
2. The orchestrator presents the plan as a numbered list before taking action.
3. The orchestrator asks for confirmation before creating ADO items.

**US-2 — New user**
> As a new user, I want to describe my goal in plain language and have the orchestrator tell me what it can do, so I don't need to know the catalog first.

*Acceptance Criteria:*
1. Saying "I need help writing a PR description" results in the orchestrator identifying `devops-engineer` + `/pr-description` skill.
2. The orchestrator explains what it will do before doing it.
3. For ambiguous requests ("help me with my project"), the orchestrator asks a clarifying question rather than guessing.

**US-3 — Loop prevention**
> As a maintainer, I want the orchestrator to have explicit loop-prevention rules so it can't accidentally create recursive delegation chains.

*Acceptance Criteria:*
1. The orchestrator agent body explicitly states it cannot call another orchestrator.
2. The orchestrator agent does not list itself in its own `skills:` or delegation targets.
3. If a subtask maps to an unknown agent, the orchestrator surfaces this gap to the user rather than attempting to handle it.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Design orchestrator delegation model — map of intent patterns to domain agents | Dev | 1h |
| T2 | Define circuit-breaker rules and loop-prevention boundaries | Dev | 30m |
| T3 | Create `.claude/agents/orchestrator.agent.md` with delegation plan format and boundaries | Dev | 1.5h |
| T4 | Create `.github/agents/orchestrator.agent.md` | Dev | 45m |
| T5 | Run `validate_agent.py` on both files | Dev | 10m |
| T6 | Create `.claude/skills/meta/orchestrate/SKILL.md` — usage guide for the orchestrator | Dev | 30m |
| T7 | Create `.github/skills/orchestrate/SKILL.md` | Dev | 20m |
| T8 | Run validators, generate catalog, sync check | Dev | 15m |
| T9 | Update `README.md` — add orchestrator to agent table and "Getting Started" section | Dev | 20m |
| T10 | Test with 3 representative multi-domain scenarios (doc) | Dev | 30m |

**Total estimate: ~6.5h → 8 story points**

---

## Delegation Intent Map (Draft)

| User Intent Signals | Delegate To |
|--------------------|-------------|
| "PR description", "commit message", "git" | `devops-engineer` |
| "ADO", "sprint", "work item", "epic", "story", "task" | `ado-manager` |
| "document", "README", "ADR", "API docs", "runbook" | `doc-writer` |
| "code review", "test", "implement", "scaffold" | `coder` / `tester` |
| "Teams", "announcement", "channel post" | `teams-manager` |
| "email", "Outlook", "meeting invite" | `outlook-manager` |
| "schema", "pipeline", "model card", "EDA", "stored proc" | `data-engineer` |
| "PowerPoint", "Excel", "Word", "deck", "report" | `office-writer` |
| "Terraform", "infra", "CI/CD", "pipeline yaml" | `devops-engineer` |
| "what skill", "how do I", "where is", "explain" | `info-agent` |

---

## Acceptance Criteria (PR-level)

1. Both agent files exist and pass `validate_agent.py` with zero errors.
2. Both agent bodies include: delegation plan format, loop-prevention rules, confirmation-before-action boundaries.
3. `meta/orchestrate` skill (Claude + Copilot) exists and passes validators.
4. Catalog and `sync_check.py` clean.
5. `README.md` updated with orchestrator description.

---

## PR Title

`feat(meta): add orchestrator agent for cross-domain task delegation`
