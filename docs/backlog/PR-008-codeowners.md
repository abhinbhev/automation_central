# PR-008 — CODEOWNERS + PR Review Enforcement

**Phase:** 1 — Hardening & Coverage
**Type:** Repository configuration
**Story Points:** 1
**Priority:** P2 — High
**Depends on:** PR-003 (CI pipeline — CODEOWNERS is only meaningful if there is a PR process to enforce it)
**Blocks:** —

---

## Problem Statement

The PR template says "1 reviewer minimum" but GitHub has no configured `CODEOWNERS` file to enforce reviewer assignment. High-stakes paths — `INSTRUCTIONS.md`, `scripts/repo/`, `.github/workflows/`, and root configuration files — can have PRs merged without review from the people who own those areas. As the team grows and external contributors add skills, unreviewed changes to the validation contract or CI gate could silently break the entire system.

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `.github/CODEOWNERS` file at repo root |
| R2 | `INSTRUCTIONS.md` requires owner approval (highest-stakes file) |
| R3 | `scripts/repo/` (validators, catalog generator) requires owner approval |
| R4 | `.github/workflows/` requires owner approval |
| R5 | `configs/` requires owner approval |
| R6 | `.claude/agents/` requires at least one reviewer |
| R7 | `.github/agents/` requires at least one reviewer |
| R8 | `.github/instructions/` requires at least one reviewer |
| R9 | New skills in `.claude/skills/<domain>/` and `.github/skills/` can be merged with any reviewer (lower bar — skills are lower risk) |
| R10 | `CONTRIBUTING.md` updated to document the CODEOWNERS structure |

---

## User Stories

**US-1 — Contributor**
> As a contributor adding a new skill, I want the PR system to tell me who to request review from, so I don't need to ask in Teams.

*Acceptance Criteria:*
1. Opening a PR that only touches `.claude/skills/` or `.github/skills/` shows the default reviewer (anyone).
2. Opening a PR that touches `INSTRUCTIONS.md` shows the designated owner(s) as required reviewers.
3. Opening a PR that touches `scripts/repo/` requires approval from the repo owner(s).

**US-2 — Maintainer**
> As a maintainer, I want structural changes (validators, CI, INSTRUCTIONS) to require my explicit approval, so nothing breaks the quality gate without my knowledge.

*Acceptance Criteria:*
1. A PR touching `.github/workflows/validate.yml` cannot be merged without the designated owner's approval.
2. A PR touching only a SKILL.md body can be merged by any reviewer.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Create `.github/CODEOWNERS` file | Dev | 20m |
| T2 | Add ownership rules for `INSTRUCTIONS.md`, `CONTRIBUTING.md`, `README.md` | Dev | 5m |
| T3 | Add ownership rules for `scripts/repo/`, `.github/workflows/`, `configs/` | Dev | 5m |
| T4 | Add ownership rules for `.claude/agents/` and `.github/agents/` | Dev | 5m |
| T5 | Add ownership rules for `.github/instructions/` | Dev | 5m |
| T6 | Add catch-all default reviewer for everything else (skills, templates) | Dev | 5m |
| T7 | Update `CONTRIBUTING.md` with a short note on CODEOWNERS | Dev | 10m |
| T8 | Verify CODEOWNERS syntax via GitHub's web UI CODEOWNERS validator | Dev | 10m |

**Total estimate: ~1h → 1 story point**

---

## CODEOWNERS Skeleton

```
# automation_central CODEOWNERS
# Format: <path pattern>  @<github-username>

# Structural files — require repo owner approval
INSTRUCTIONS.md           @<owner>
CONTRIBUTING.md           @<owner>
README.md                 @<owner>

# Quality gate scripts — require repo owner approval
scripts/repo/             @<owner>
.github/workflows/        @<owner>
configs/                  @<owner>

# Agent definitions — require at least one reviewer
.claude/agents/           @<owner>
.github/agents/           @<owner>

# Instructions / standards — require at least one reviewer
.github/instructions/     @<owner>

# Skills — any reviewer acceptable (lower risk, higher volume)
.claude/skills/           @<owner>
.github/skills/           @<owner>

# Default catch-all
*                         @<owner>
```

---

## Acceptance Criteria (PR-level)

1. `.github/CODEOWNERS` exists with all required path rules.
2. GitHub UI shows CODEOWNERS as valid (no syntax errors).
3. A test PR touching `INSTRUCTIONS.md` shows the designated owner as a required reviewer.
4. `CONTRIBUTING.md` mentions CODEOWNERS in the PR workflow section.

---

## PR Title

`chore(meta): add CODEOWNERS to enforce review assignment by path`
