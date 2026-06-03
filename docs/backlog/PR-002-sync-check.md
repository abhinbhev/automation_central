# PR-002 — Sync-Check Script (`sync_check.py`)

**Phase:** 0 — Production Gate
**Type:** New script (meta tooling)
**Story Points:** 5
**Priority:** P1 — Critical
**Depends on:** PR-001 (batch validator — for CI wiring)
**Blocks:** PR-003 (CI pipeline)

---

## Problem Statement

The SYNC RULE — "every Claude asset must have a Copilot counterpart and vice versa" — is documented in 4 places (`INSTRUCTIONS.md`, both `agent-skill-manager.agent.md` files, `add-skill` SKILL.md) but never mechanically enforced. Currently:
- 12 Claude skills have no `.github/skills/` counterpart.
- Nothing prevents an agent file from being updated in `.claude/agents/` without touching `.github/agents/`.
- `description` fields can silently diverge between pairs, misleading users of either framework.

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | For every `X.agent.md` in `.claude/agents/`, assert a matching file exists in `.github/agents/` |
| R2 | For every `X.agent.md` in `.github/agents/`, assert a matching file exists in `.claude/agents/` |
| R3 | For every matched agent pair, compare the `description` frontmatter field — WARN if they differ |
| R4 | For every skill folder `<name>` in `.claude/skills/<domain>/`, check whether `.github/skills/<name>/SKILL.md` exists — WARN if missing |
| R5 | Missing agent pair file is an ERROR (exit 1); missing Copilot skill counterpart is a WARN (exit 0) |
| R6 | Script prints a summary: N agent pairs checked, N skills checked, X errors, Y warnings |
| R7 | Script accepts `--strict` flag: treat all WARN as ERROR (useful in CI) |
| R8 | Follows `scripts/repo/` conventions |

---

## User Stories

**US-1 — Pair parity enforcement**
> As a maintainer, I want a script that tells me exactly which agent or skill files are out of sync between Claude and Copilot, so I can fix drift before it confuses users.

*Acceptance Criteria:*
1. Running `sync_check.py` after deleting a `.github/agents/` file reports an ERROR with the missing file path.
2. Running `sync_check.py` after editing only the Claude agent's description reports a WARN with both the Claude and Copilot values shown.
3. Running `sync_check.py --strict` with any WARN exits 1.
4. Running `sync_check.py` on the current repo (which has 12 missing Copilot skills) lists those 12 as WARN.

**US-2 — PR gate integration**
> As a maintainer, I want CI to run `sync_check.py --strict` on every PR that touches `.claude/` or `.github/`, so the SYNC RULE is technically enforced, not just documented.

*Acceptance Criteria:*
1. CI step runs `sync_check.py --strict` and fails if either framework's files are missing their pair.
2. CI step passes on a fully-synced repo.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Create `scripts/repo/sync_check.py` with typer CLI entry point | Dev | 30m |
| T2 | Implement `check_agent_pairs()` — scan both agent dirs, build sets, find symmetric difference | Dev | 1h |
| T3 | Implement `check_description_drift()` — parse frontmatter of both pair members, compare `description` | Dev | 1h |
| T4 | Implement `check_skill_parity()` — collect all `.claude/skills/<domain>/<name>` folder names, check `.github/skills/<name>` exists | Dev | 1h |
| T5 | Implement `--strict` flag logic: reclassify WARN→ERROR in output and exit code | Dev | 30m |
| T6 | Implement summary renderer (rich table) with ERROR/WARN rows and final count | Dev | 45m |
| T7 | Wire `sync_check` into `validate_all.py` as an optional step (or document it as a companion command) | Dev | 30m |
| T8 | Update `INSTRUCTIONS.md §11` pre-PR checklist to include `sync_check.py` | Dev | 15m |
| T9 | Update `CONTRIBUTING.md` to reference `sync_check.py` | Dev | 15m |
| T10 | Manual test: delete one agent pair file, confirm ERROR output | Dev | 30m |

**Total estimate: ~7h → 5 story points**

---

## Acceptance Criteria (PR-level)

1. `python scripts/repo/sync_check.py` runs clean on a fully-synced repo (exit 0).
2. Removing `.github/agents/tester.agent.md` causes exit 1 with a clear ERROR message.
3. Setting different `description` values in a Claude vs Copilot agent pair produces a WARN with both values shown.
4. Running with `--strict` after any WARN produces exit 1.
5. The 12 currently-missing Copilot skills are listed as WARN in output (verifiable pre-PR-005).
6. Script is importable without side effects (for wiring into `validate_all.py`).

---

## PR Title

`feat(meta): add sync_check.py to enforce Claude/Copilot pair parity`
