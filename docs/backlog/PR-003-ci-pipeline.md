# PR-003 — CI Pipeline: GitHub Actions Validation Workflow

**Phase:** 0 — Production Gate
**Type:** New CI/CD configuration
**Story Points:** 3
**Priority:** P1 — Critical
**Depends on:** PR-001 (validate_all.py), PR-002 (sync_check.py)
**Blocks:** PR-008 (CODEOWNERS)

---

## Problem Statement

There are no GitHub Actions workflows in `.github/workflows/`. Every quality gate (validator, catalog freshness, sync check) is manual and optional. A PR with a broken SKILL.md, a missing agent pair, or a stale catalog can merge silently today. This is the single biggest structural gap between the current state and production-grade.

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | Workflow triggers on `pull_request` targeting `main` |
| R2 | Workflow triggers on `push` to `main` (for post-merge catalog freshness check) |
| R3 | Workflow uses path filters: only runs full validation when `.claude/**`, `.github/skills/**`, `.github/agents/**`, or `scripts/repo/**` change |
| R4 | Workflow installs Python 3.11 and project dependencies from `configs/envs/requirements.txt` |
| R5 | Step 1: run `python scripts/repo/validate_all.py` — fail PR if exit code 1 |
| R6 | Step 2: run `python scripts/repo/sync_check.py --strict` — fail PR if exit code 1 |
| R7 | Step 3: run `python scripts/repo/generate_catalog.py` then check if `docs/automation-catalog.md` is dirty (uncommitted changes) — fail if dirty |
| R8 | All steps have explicit `name:` fields |
| R9 | GitHub Actions versions pinned to exact SHA (not floating tags) per `.github/instructions/` standards |
| R10 | Secrets accessed via `env:` block, never hardcoded |
| R11 | Workflow file: `.github/workflows/validate.yml` |

---

## User Stories

**US-1 — PR author**
> As a contributor opening a PR that adds a new skill, I want the CI check to tell me immediately if my SKILL.md is malformed or my Copilot counterpart is missing, so I can fix it before review.

*Acceptance Criteria:*
1. A PR adding a malformed SKILL.md (missing `## Steps` section) fails CI with a descriptive error.
2. A PR adding a Claude skill without a Copilot counterpart fails CI at the sync-check step.
3. A PR that does not touch `.claude/**` or `.github/**` skips the validation job entirely.
4. A valid PR passes all three steps (validate, sync, catalog) and shows green checks.

**US-2 — Maintainer / reviewer**
> As a reviewer, I want to see CI results on every PR so I can focus my review on logic and content, not structural compliance.

*Acceptance Criteria:*
1. All three steps have distinct, readable names in the CI summary.
2. Failures show the exact file and finding (surfaced from the underlying script output).
3. The catalog freshness check step fails with a message listing which files changed.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Create `.github/workflows/validate.yml` with `on: [pull_request, push to main]` trigger and path filters | Dev | 30m |
| T2 | Add `setup-python@v5` step with Python 3.11, pinned to SHA | Dev | 20m |
| T3 | Add `pip install -r configs/envs/requirements.txt` step (requires PR-009 to create this file first — use conda env as fallback) | Dev | 20m |
| T4 | Add "Validate skills and agents" step running `validate_all.py` | Dev | 15m |
| T5 | Add "Check framework sync" step running `sync_check.py --strict` | Dev | 15m |
| T6 | Add "Verify catalog is up to date" step: run `generate_catalog.py`, then `git diff --exit-code docs/automation-catalog.md` | Dev | 20m |
| T7 | Pin all `uses:` action versions to full SHA (not `@v4` floating tags) | Dev | 15m |
| T8 | Add `configs/envs/requirements.txt` as a minimal pip-installable deps file if not yet present | Dev | 30m |
| T9 | Test workflow on a feature branch — confirm it passes on clean state | Dev | 30m |
| T10 | Update `CONTRIBUTING.md` to document "CI runs automatically on every PR" | Dev | 15m |

**Total estimate: ~3.5h → 3 story points**

---

## Workflow Skeleton

```yaml
name: Validate skills and agents
on:
  pull_request:
    paths:
      - '.claude/**'
      - '.github/skills/**'
      - '.github/agents/**'
      - 'scripts/repo/**'
  push:
    branches: [main]
    paths:
      - '.claude/**'
      - '.github/skills/**'
      - '.github/agents/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@<SHA>

      - name: Set up Python 3.11
        uses: actions/setup-python@<SHA>
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r configs/envs/requirements.txt

      - name: Validate all skills and agents
        run: python scripts/repo/validate_all.py

      - name: Check Claude/Copilot framework sync
        run: python scripts/repo/sync_check.py --strict

      - name: Verify automation catalog is up to date
        run: |
          python scripts/repo/generate_catalog.py
          git diff --exit-code docs/automation-catalog.md || (echo "Catalog is stale — run generate_catalog.py and commit the result" && exit 1)
```

---

## Acceptance Criteria (PR-level)

1. Workflow file exists at `.github/workflows/validate.yml`.
2. All `uses:` pins are full SHAs (verified manually or with `actionlint`).
3. Workflow passes on current `main` (clean repo).
4. Introducing a deliberate error in any SKILL.md on a branch causes the "Validate" step to fail.
5. Merging a Claude skill without a Copilot counterpart causes the "Sync" step to fail.
6. Running with a stale catalog causes the "Verify catalog" step to fail.
7. A PR that only changes `README.md` does not trigger the validation job (path filter works).

---

## PR Title

`ci: add GitHub Actions validation workflow for skills, agents, and catalog`
