# PR-006 — Validator Hardening

**Phase:** 1 — Hardening & Coverage
**Type:** Script improvements + refactor
**Story Points:** 3
**Priority:** P2 — High
**Depends on:** PR-001 (batch validator — imports check functions)
**Blocks:** —

---

## Problem Statement

Three specific weaknesses in the current validators and catalog generator reduce the reliability of the quality gate:

1. **`validate_skill.py` line 77:** A SKILL.md referencing a non-existent script path exits with WARN (not ERROR). This means a skill with a broken script reference passes CI and ships a broken catalog entry.
2. **`generate_catalog.py`:** Silently skips malformed SKILL.md files (missing `name` = just skipped). A stale or broken frontmatter block produces a silent gap in the catalog.
3. **`generate_catalog.py`'s `render_catalog()` function:** 67 lines — above the 40-line threshold set in `python.instructions.md`. Difficult to test individual rendering sections.
4. **`.vscode/settings.json`:** Still contains `"*.prompt.md": "markdown"` — a dead file association from the removed prompts primitive.

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `validate_skill.py`: missing `script:` path when `requires_script: true` must be an ERROR (exit 1), not a WARN |
| R2 | `generate_catalog.py`: add `--strict` flag that calls `check_skill()` for every scanned SKILL.md and aborts if any ERROR found |
| R3 | `generate_catalog.py`: `render_catalog()` refactored into 3 private functions under 40 lines each |
| R4 | `.vscode/settings.json`: remove `"*.prompt.md": "markdown"` dead file association |
| R5 | No change to the external CLI signature of either script (backwards compatible) |
| R6 | All existing tests (post-PR-007) must pass after refactor |

---

## User Stories

**US-1 — Contributor**
> As a contributor adding a skill with `requires_script: true`, I want the validator to ERROR (not warn) if the script path doesn't exist, so I can't accidentally ship a broken skill reference.

*Acceptance Criteria:*
1. `validate_skill.py` on a SKILL.md with `requires_script: true` and a non-existent `script:` path exits 1 with an ERROR message.
2. `validate_skill.py` on a SKILL.md with `requires_script: false` and no `script:` exits 0.
3. Existing passing skills still pass after this change.

**US-2 — CI maintainer**
> As a CI maintainer, I want `generate_catalog.py --strict` to fail loudly if any SKILL.md is malformed, so the catalog only publishes clean entries.

*Acceptance Criteria:*
1. `generate_catalog.py --strict` with all current skills passes (exits 0).
2. `generate_catalog.py --strict` with a deliberately broken SKILL.md fails with the file path and error.
3. `generate_catalog.py` without `--strict` still silently skips malformed files (backward compat).

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | `validate_skill.py` line ~77: change `("WARN", ...)` to `("ERROR", ...)` for missing script path | Dev | 10m |
| T2 | Verify all current skills still pass after T1 (no skill has a broken script ref currently) | Dev | 15m |
| T3 | `generate_catalog.py`: import `check_skill` from `validate_skill` module | Dev | 15m |
| T4 | `generate_catalog.py`: add `--strict` typer option; when set, run `check_skill()` on each found SKILL.md and abort on any ERROR | Dev | 45m |
| T5 | `generate_catalog.py`: extract `_render_claude_skills(skills: dict) -> list[str]` | Dev | 20m |
| T6 | `generate_catalog.py`: extract `_render_agents(agents: list) -> list[str]` | Dev | 15m |
| T7 | `generate_catalog.py`: extract `_render_copilot_skills(github_skills: list) -> list[str]` | Dev | 15m |
| T8 | `generate_catalog.py`: `render_catalog()` becomes thin orchestrator calling the three helpers | Dev | 15m |
| T9 | `.vscode/settings.json`: remove `"*.prompt.md": "markdown"` line | Dev | 5m |
| T10 | Update CI workflow (PR-003) to use `generate_catalog.py --strict` | Dev | 10m |
| T11 | Verify `generate_catalog.py` produces identical output before/after refactor | Dev | 20m |

**Total estimate: ~3.5h → 3 story points**

---

## Acceptance Criteria (PR-level)

1. `validate_skill.py` on a skill with a missing script path exits 1 (was exit 0).
2. `generate_catalog.py` output is byte-for-byte identical before and after refactor on a clean repo.
3. `generate_catalog.py --strict` exits 0 on the clean repo.
4. `generate_catalog.py --strict` exits 1 on a repo with a broken SKILL.md, printing the file and error.
5. `render_catalog()` and each helper are under 40 lines.
6. `.vscode/settings.json` has no `*.prompt.md` entry.
7. All `validate_all.py` runs still pass (no regressions).

---

## PR Title

`fix(meta): harden validators — missing script is ERROR, catalog strict mode, refactor render`
