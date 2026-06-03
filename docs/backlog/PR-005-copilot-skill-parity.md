# PR-005 — Copilot Skill Parity (12 Missing `.github/skills/` Counterparts)

**Phase:** 0 — Production Gate
**Type:** New content (Copilot SKILL.md files)
**Story Points:** 8
**Priority:** P1 — Critical
**Depends on:** —
**Blocks:** PR-011, PR-012, PR-013 (new agents — all must be in sync from creation)

---

## Problem Statement

The SYNC RULE mandates that every Claude skill has a Copilot counterpart and vice versa. Currently, 12 Claude skills exist only in `.claude/skills/` with no matching `.github/skills/<name>/SKILL.md`. Copilot users silently cannot access these workflows. This is a direct violation of the core pair-invariant documented in `INSTRUCTIONS.md §3`.

---

## Missing Copilot Skills

| Claude Skill Path | Copilot Folder | Domain |
|-------------------|----------------|--------|
| `.claude/skills/comms/meeting-minutes` | `.github/skills/meeting-minutes` | comms |
| `.claude/skills/comms/email-draft` | `.github/skills/email-draft` | comms |
| `.claude/skills/comms/teams-announcement` | `.github/skills/teams-announcement` | comms |
| `.claude/skills/data-ml/schema-docs` | `.github/skills/schema-docs` | data-ml |
| `.claude/skills/data-ml/pipeline-docs` | `.github/skills/pipeline-docs` | data-ml |
| `.claude/skills/data-ml/model-card` | `.github/skills/model-card` | data-ml |
| `.claude/skills/coding/plan-task` | `.github/skills/plan-task` | coding |
| `.claude/skills/coding/scaffold-stored-procedure` | `.github/skills/scaffold-stored-procedure` | coding |
| `.claude/skills/coding/scaffold-sp-wrapper` | `.github/skills/scaffold-sp-wrapper` | coding |
| `.claude/skills/coding/scaffold-at-prompts` | `.github/skills/scaffold-at-prompts` | coding |
| `.claude/skills/infra/arch-diagram` | `.github/skills/arch-diagram` | infra |
| `.claude/skills/devops/gh-actions-workflow` | `.github/skills/gh-actions-workflow` | devops |

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | Each Copilot SKILL.md has `name`, `description` (double-quoted), and `mode` frontmatter |
| R2 | `name` matches the folder name exactly (kebab-case) |
| R3 | `description` is consistent with (or a refined version of) the Claude counterpart's description |
| R4 | `mode` is `ask` for output-only skills, `agent` for skills that read/write workspace files |
| R5 | Body is the full skill instruction content adapted for Copilot context (no `## Usage`/`## Output`/`## Steps` required) |
| R6 | Each skill is registered in the catalog after creation (`generate_catalog.py` run) |
| R7 | `sync_check.py` (post-PR-002) reports zero WARN for Copilot skill parity after this PR |

---

## User Stories

**US-1 — Copilot user (comms domain)**
> As a Copilot user, I want to type `/meeting-minutes` and get a structured minutes document, the same way Claude Code users do.

*Acceptance Criteria:*
1. `.github/skills/meeting-minutes/SKILL.md` exists with valid frontmatter.
2. Invoking `/meeting-minutes` in Copilot Chat produces a structured minutes output.
3. Description in Copilot SKILL.md matches the Claude skill description.

**US-2 — Copilot user (data-ml domain)**
> As a Copilot user, I want access to `schema-docs`, `pipeline-docs`, and `model-card` skills so I can document data assets without switching to Claude Code.

*Acceptance Criteria:*
1. All three data-ml Copilot skills exist with appropriate `mode: agent` (they read files).
2. Each body provides enough context for Copilot to produce useful output without additional prompting.

**US-3 — Copilot user (coding domain)**
> As a Copilot user, I want `plan-task`, `scaffold-stored-procedure`, `scaffold-sp-wrapper`, and `scaffold-at-prompts` available so I can use the team's coding scaffolding tools.

*Acceptance Criteria:*
1. All four coding Copilot skills exist.
2. `scaffold-*` skills use `mode: agent` (they write files).
3. `plan-task` uses `mode: ask` (output only).

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Read each of the 12 Claude SKILL.md files and extract key instructions | Dev | 1h |
| T2 | Create `.github/skills/meeting-minutes/SKILL.md` | Dev | 20m |
| T3 | Create `.github/skills/email-draft/SKILL.md` | Dev | 20m |
| T4 | Create `.github/skills/teams-announcement/SKILL.md` | Dev | 20m |
| T5 | Create `.github/skills/schema-docs/SKILL.md` | Dev | 20m |
| T6 | Create `.github/skills/pipeline-docs/SKILL.md` | Dev | 20m |
| T7 | Create `.github/skills/model-card/SKILL.md` | Dev | 20m |
| T8 | Create `.github/skills/plan-task/SKILL.md` | Dev | 20m |
| T9 | Create `.github/skills/scaffold-stored-procedure/SKILL.md` | Dev | 30m |
| T10 | Create `.github/skills/scaffold-sp-wrapper/SKILL.md` | Dev | 30m |
| T11 | Create `.github/skills/scaffold-at-prompts/SKILL.md` | Dev | 30m |
| T12 | Create `.github/skills/arch-diagram/SKILL.md` | Dev | 20m |
| T13 | Create `.github/skills/gh-actions-workflow/SKILL.md` | Dev | 20m |
| T14 | Run `generate_catalog.py` and commit updated `docs/automation-catalog.md` | Dev | 10m |
| T15 | Run `sync_check.py` (post-PR-002) and confirm zero parity warnings | Dev | 15m |

**Total estimate: ~6.5h → 8 story points (scope, not complexity)**

---

## Mode Assignment Guide

| Skill | Mode | Reason |
|-------|------|--------|
| `meeting-minutes` | `ask` | Output only — no file writes |
| `email-draft` | `ask` | Output only |
| `teams-announcement` | `ask` | Output only |
| `schema-docs` | `agent` | Reads DB/DDL files |
| `pipeline-docs` | `agent` | Reads pipeline definition files |
| `model-card` | `ask` | Output only (may read model files — use `agent` if so) |
| `plan-task` | `ask` | Output only |
| `scaffold-stored-procedure` | `agent` | Writes `.py` files |
| `scaffold-sp-wrapper` | `agent` | Writes `.py` files |
| `scaffold-at-prompts` | `agent` | Writes prompt files |
| `arch-diagram` | `ask` | Output only (Mermaid/text) |
| `gh-actions-workflow` | `agent` | Writes `.yml` files |

---

## Acceptance Criteria (PR-level)

1. All 12 `.github/skills/<name>/SKILL.md` files exist with valid frontmatter.
2. All `name` values match their folder names.
3. All `description` values match or meaningfully correspond to the Claude counterpart.
4. `generate_catalog.py` runs clean and the catalog shows 37 Copilot skills (up from 25).
5. `sync_check.py` reports zero WARN for Copilot skill parity.
6. No `## Usage`/`## Output`/`## Steps` sections in any Copilot SKILL.md (Copilot format).

---

## PR Title

`feat(sync): add 12 missing Copilot skill counterparts to close parity gap`
