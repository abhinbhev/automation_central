# PR-009 — Templates Cleanup + `requirements.txt`

**Phase:** 1 — Hardening & Coverage
**Type:** Housekeeping + dependency management
**Story Points:** 2
**Priority:** P2 — High
**Depends on:** —
**Blocks:** PR-003 (CI pipeline needs `requirements.txt`)

---

## Problem Statement

Two housekeeping issues affect developer experience and CI reliability:

1. **`templates/prompts/` directory exists** despite the architecture decision to remove `.github/prompts/` entirely. Any content here is a dead asset that confuses contributors about the current primitives model.
2. **No `requirements.txt` exists.** CI and non-conda developers have no pip-installable dependency specification. The only dependency file is `configs/envs/conda-env.yml`, which requires conda and may contain already-removed packages (e.g. `python-pptx` was explicitly removed but should be verified).

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `templates/prompts/` directory audited — contents documented or deleted |
| R2 | `configs/envs/requirements.txt` created, pip-installable, containing all runtime deps from `conda-env.yml` |
| R3 | `configs/envs/requirements-dev.txt` created with dev/test deps (pytest, ruff, pre-commit, detect-secrets) |
| R4 | `conda-env.yml` audited for removed packages (`python-pptx`) — remove any that are no longer used |
| R5 | `README.md` updated to document both conda and pip setup paths |
| R6 | `CONTRIBUTING.md` updated to reference `requirements-dev.txt` for the dev environment |

---

## User Stories

**US-1 — Non-conda developer**
> As a developer who doesn't use conda, I want a `requirements.txt` so I can set up the project with plain pip in any virtual environment.

*Acceptance Criteria:*
1. `pip install -r configs/envs/requirements.txt` succeeds in a clean venv.
2. All scripts in `scripts/` run without import errors after installing from `requirements.txt`.
3. `pip install -r configs/envs/requirements-dev.txt` installs pytest, ruff, and pre-commit.

**US-2 — CI**
> As a CI workflow, I need `requirements.txt` to install dependencies without conda.

*Acceptance Criteria:*
1. `.github/workflows/validate.yml` step `pip install -r configs/envs/requirements.txt` succeeds.
2. All CI script steps work after this install.

**US-3 — Contributor**
> As a contributor reading the repo, I want `templates/prompts/` to not exist (or to have a clear README explaining its purpose), so I'm not confused about whether prompts are still a thing.

*Acceptance Criteria:*
1. `templates/prompts/` either does not exist, or contains a `README.md` explaining it is for standalone prompt template files (not the `.github/prompts/` primitive which was removed).
2. No leftover `.prompt.md` files reference the removed prompts workflow.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | `ls templates/prompts/` — audit contents, determine if any files have value | Dev | 15m |
| T2 | If empty or stale: delete `templates/prompts/` directory | Dev | 5m |
| T3 | If contains useful content: add `templates/prompts/README.md` clarifying its purpose is standalone prompt templates, not the removed `.github/prompts/` primitive | Dev | 20m |
| T4 | Audit `configs/envs/conda-env.yml` for `python-pptx` and any other removed packages | Dev | 15m |
| T5 | Remove `python-pptx` from `conda-env.yml` if present | Dev | 5m |
| T6 | Create `configs/envs/requirements.txt` from the conda env runtime packages | Dev | 30m |
| T7 | Create `configs/envs/requirements-dev.txt` with pytest, ruff, pre-commit, detect-secrets, pytest-httpx, pytest-cov | Dev | 15m |
| T8 | Update `README.md` — add pip venv setup as alternative to conda | Dev | 20m |
| T9 | Update `CONTRIBUTING.md` — reference `requirements-dev.txt` for dev setup | Dev | 10m |
| T10 | Verify `pip install -r requirements.txt` in a clean venv | Dev | 20m |

**Total estimate: ~2.5h → 2 story points**

---

## Acceptance Criteria (PR-level)

1. `configs/envs/requirements.txt` exists and installs cleanly in a fresh Python 3.11 venv.
2. `configs/envs/requirements-dev.txt` exists and includes all dev/test deps.
3. `conda-env.yml` does not contain `python-pptx`.
4. `templates/prompts/` is either deleted or has an explanatory `README.md`.
5. `README.md` documents both the conda and pip setup paths.

---

## PR Title

`chore: add requirements.txt, clean up templates/prompts, audit conda env`
