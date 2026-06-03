# PR-001 — Batch Validator Script (`validate_all.py`)

**Phase:** 0 — Production Gate
**Type:** New script (meta tooling)
**Story Points:** 3
**Priority:** P1 — Critical
**Depends on:** —
**Blocks:** PR-002 (sync-check), PR-003 (CI pipeline)

---

## Problem Statement

`validate_skill.py` and `validate_agent.py` run on one file at a time. There is no command that validates the entire repo in one pass. The pre-PR checklist relies on contributors remembering to run validators manually on every file they touched. This is error-prone and unscalable as the skill/agent count grows.

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | Script walks all `.claude/skills/<domain>/<name>/` directories and validates each |
| R2 | Script walks all `.claude/agents/*.agent.md` and validates each |
| R3 | Script walks all `.github/agents/*.agent.md` and validates each |
| R4 | Script collects all findings and prints a unified summary table |
| R5 | Script exits with code 0 only if zero ERROR-level findings exist across all files |
| R6 | Script accepts an optional `--path` argument to validate a single domain or agent directory |
| R7 | Script reports a count of files validated, errors, and warnings at the end |
| R8 | Follows `scripts/repo/` conventions: typer CLI, rich output, UTF-8 stdout reconfigure |

---

## User Stories

**US-1 — Contributor pre-PR check**
> As a contributor adding a new skill, I want to run a single command to validate the entire repo, so I know nothing is broken before I open a PR.

*Acceptance Criteria:*
1. Running `python scripts/repo/validate_all.py` with a clean repo exits 0 and prints a green summary.
2. Running it after introducing a broken SKILL.md exits 1 and prints the ERROR row for that file.
3. Running it after introducing a broken agent exits 1 and identifies which agent file failed.
4. Output includes a count: `N files validated — X errors, Y warnings`.

**US-2 — CI integration**
> As a maintainer, I want the batch validator to be callable from a CI step with a non-zero exit code on any failure, so broken PRs are blocked automatically.

*Acceptance Criteria:*
1. Script is invocable with `python scripts/repo/validate_all.py` (no interactive prompts).
2. Exit code is 1 if any file has an ERROR-level finding; 0 otherwise.
3. Warnings do not cause a non-zero exit.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Create `scripts/repo/validate_all.py` with typer CLI entry point and UTF-8 reconfigure | Dev | 1h |
| T2 | Implement `validate_skills_tree()` — walks `.claude/skills/`, calls `check_skill()` from `validate_skill.py` | Dev | 1h |
| T3 | Implement `validate_agents_tree()` — walks `.claude/agents/` and `.github/agents/`, calls `check_agent()` from `validate_agent.py` | Dev | 1h |
| T4 | Implement unified summary renderer using `rich.table.Table` — columns: File, Level, Finding | Dev | 30m |
| T5 | Add `--path` optional argument to scope validation to a subtree | Dev | 30m |
| T6 | Print final count line and set exit code correctly | Dev | 15m |
| T7 | Update `CONTRIBUTING.md` pre-PR checklist to reference `validate_all.py` | Dev | 15m |
| T8 | Update `INSTRUCTIONS.md §11` pre-PR checklist line | Dev | 15m |
| T9 | Manual smoke test against current repo state — confirm clean pass | Dev | 30m |

**Total estimate: ~5.5h → 3 story points**

---

## Acceptance Criteria (PR-level)

1. `python scripts/repo/validate_all.py` exits 0 on the current clean repo.
2. Introducing a deliberate SKILL.md error causes exit 1 with the file path and error clearly shown.
3. Introducing a deliberate agent error (missing `description` frontmatter) causes exit 1.
4. `--path .claude/skills/ado` validates only ADO skills.
5. Script follows the standard skeleton in `INSTRUCTIONS.md §4.5` (typer, rich, pathlib, no bare print).
6. `CONTRIBUTING.md` and `INSTRUCTIONS.md` updated.
7. `validate_agent.py` and `validate_skill.py`: check functions (`check_skill`, `check_agent`) are importable without running the CLI (no side effects at module level — guards behind `if __name__ == "__main__"`).

---

## PR Title

`feat(meta): add validate_all.py batch validator for skills and agents`
