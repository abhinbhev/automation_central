# PR-007 — pytest Test Suite for Repo Scripts

**Phase:** 1 — Hardening & Coverage
**Type:** New test files
**Story Points:** 8
**Priority:** P2 — High
**Depends on:** —
**Blocks:** —

---

## Problem Statement

`INSTRUCTIONS.md §9` mandates "pytest tests alongside the code; mock external dependencies" — but there is no `tests/` directory anywhere in the repo. The two validators (`validate_skill.py`, `validate_agent.py`) and the catalog generator (`generate_catalog.py`) are the highest-leverage targets because every other quality gate depends on them being correct. Bugs here silently break the entire validation pipeline. The ADO and office scripts make external API calls and require mock-based unit tests.

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `tests/` directory mirrors `scripts/` structure |
| R2 | Tests for `validate_skill.py`: cover all ERROR and WARN paths in `check_skill()` |
| R3 | Tests for `validate_agent.py`: cover all ERROR and WARN paths in `check_agent()` for both Claude and Copilot variants |
| R4 | Tests for `generate_catalog.py`: cover `parse_frontmatter`, `collect_skills`, `collect_agents`, `collect_github_skills`, and each `_render_*` helper (post-PR-006) |
| R5 | Tests for `sync_check.py` (post-PR-002): cover agent pair detection, description drift, and skill parity checks |
| R6 | ADO scripts (`create_work_items.py`, `sprint_report.py`, `release_notes.py`): at least one happy-path and one error-path test each, with external HTTP mocked via `pytest-httpx` or `unittest.mock` |
| R7 | Tests use `tmp_path` (pytest fixture) for all file system interactions — no tests write to the real repo |
| R8 | `pytest` and `pytest-httpx` added to dev dependencies |
| R9 | All tests pass in CI (wire into `.github/workflows/validate.yml` as a separate job) |
| R10 | Minimum coverage target: 80% of `scripts/repo/` (enforced via `pytest --cov`) |

---

## User Stories

**US-1 — Script author**
> As a developer modifying `validate_skill.py`, I want a test suite to tell me immediately if I've broken an existing check, so I can refactor with confidence.

*Acceptance Criteria:*
1. `pytest tests/repo/` passes on the current clean codebase.
2. Deliberately removing the `## Steps` check from `validate_skill.py` causes at least one test to fail.
3. Tests run in under 10 seconds total (no slow I/O — all file ops via `tmp_path`).

**US-2 — CI gate**
> As a maintainer, I want test results reported on every PR that changes a script, so regressions are caught before review.

*Acceptance Criteria:*
1. CI job `test` runs `pytest tests/ --cov=scripts/repo --cov-fail-under=80`.
2. CI job fails if coverage drops below 80%.
3. CI job is separate from the validate job and can fail independently.

---

## Test File Structure

```
tests/
  repo/
    test_validate_skill.py
    test_validate_agent.py
    test_generate_catalog.py
    test_sync_check.py          # after PR-002
    test_validate_all.py        # after PR-001
  ado/
    test_create_work_items.py
    test_sprint_report.py
    test_release_notes.py
  office/
    test_ppt_builder.py         # happy path only
    test_word_builder.py        # happy path only
    test_excel_builder.py       # happy path only
  conftest.py                   # shared fixtures (tmp skill dir, tmp agent file, sample frontmatter)
```

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Create `tests/` directory structure and `conftest.py` with shared fixtures | Dev | 30m |
| T2 | `test_validate_skill.py`: test valid skill passes; missing frontmatter fields; wrong domain; name mismatch; missing sections; broken script ref (post-PR-006 change to ERROR); secret pattern detected | Dev | 1.5h |
| T3 | `test_validate_agent.py`: test valid Claude agent passes; valid Copilot agent passes; missing `name` (Claude) errors; missing `description` (Copilot) errors; skills list resolves; missing `## Relevant Skills` warns | Dev | 1.5h |
| T4 | `test_generate_catalog.py`: test `parse_frontmatter` with valid/invalid YAML; `collect_skills` with tmp skill tree; `_render_claude_skills`; `_render_copilot_skills`; full catalog output matches expected snapshot | Dev | 1.5h |
| T5 | `test_sync_check.py`: agent pair present (pass); one side missing (error); description drift (warn); missing Copilot skill (warn); `--strict` promotes warn to error | Dev | 1h |
| T6 | `test_create_work_items.py`: mock `httpx.post` for work item creation; happy path returns item ID; API error raises `AzureDevOpsServiceError` | Dev | 1h |
| T7 | `test_sprint_report.py`: mock ADO sprint API; happy path returns Markdown report | Dev | 45m |
| T8 | `test_release_notes.py`: mock ADO work items API; happy path returns release notes | Dev | 45m |
| T9 | Add `pytest`, `pytest-httpx`, `pytest-cov` to `conda-env.yml` and `requirements.txt` | Dev | 10m |
| T10 | Update CI workflow (PR-003) to add `test` job running `pytest tests/ --cov=scripts/repo --cov-fail-under=80` | Dev | 20m |
| T11 | Run full suite locally, fix any issues | Dev | 30m |

**Total estimate: ~10h → 8 story points**

---

## Sample Test (illustrative)

```python
# tests/repo/test_validate_skill.py
from pathlib import Path
from scripts.repo.validate_skill import check_skill

def test_valid_skill_passes(tmp_path):
    skill_dir = tmp_path / "ado" / "create-work-items"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: create-work-items\ndescription: test\n"
        "domain: ado\nrequires_script: false\n---\n"
        "## Usage\nfoo\n## Output\nbar\n## Steps\n1. step\n"
    )
    findings = check_skill(skill_dir)
    assert findings == []

def test_missing_steps_section_errors(tmp_path):
    skill_dir = tmp_path / "ado" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: my-skill\ndescription: test\n"
        "domain: ado\nrequires_script: false\n---\n"
        "## Usage\nfoo\n## Output\nbar\n"
    )
    findings = check_skill(skill_dir)
    assert any(level == "ERROR" and "Steps" in msg for level, msg in findings)
```

---

## Acceptance Criteria (PR-level)

1. `pytest tests/` passes on the current clean repo.
2. `pytest tests/repo/ --cov=scripts/repo --cov-fail-under=80` passes.
3. No test writes to the real repo directories (all use `tmp_path`).
4. All external HTTP calls in ADO tests are mocked.
5. CI `test` job is separate from the `validate` job.
6. `pytest`, `pytest-httpx`, `pytest-cov` in both `conda-env.yml` and `requirements.txt`.

---

## PR Title

`test: add pytest suite for repo validators, catalog generator, and ADO scripts`
