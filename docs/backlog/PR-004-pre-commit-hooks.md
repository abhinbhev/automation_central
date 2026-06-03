# PR-004 — Pre-Commit Hooks

**Phase:** 0 — Production Gate
**Type:** Developer tooling / repo configuration
**Story Points:** 3
**Priority:** P1 — Critical
**Depends on:** PR-001 (validate_all.py)
**Blocks:** —

---

## Problem Statement

`INSTRUCTIONS.md §12` states "Never bypass the validators with `--no-verify` or skip-flag commits" — but there are no hooks configured to make this rule enforceable. A developer can commit broken SKILL.md files, Python with unused imports, or hardcoded credentials without any local gate firing. Pre-commit hooks provide a fast, local feedback loop before anything reaches CI.

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `.pre-commit-config.yaml` at repo root |
| R2 | Hook: `ruff` linting on all `scripts/**/*.py` files |
| R3 | Hook: `ruff format --check` on all `scripts/**/*.py` files |
| R4 | Hook: local hook running `validate_all.py` when `.claude/**` or `.github/agents/**` files are staged |
| R5 | Hook: `detect-secrets` (or `gitleaks`) secret scan on all staged files |
| R6 | Hook: standard `end-of-file-fixer` and `trailing-whitespace` for all Markdown files |
| R7 | All pre-commit hook versions pinned |
| R8 | Setup instructions added to `CONTRIBUTING.md` (one-time `pre-commit install` step) |
| R9 | `pre-commit` added to `configs/envs/conda-env.yml` and `configs/envs/requirements.txt` dev dependencies |

---

## User Stories

**US-1 — Developer workflow**
> As a developer, I want pre-commit hooks to catch linting and validation errors before I push, so I don't waste CI cycles or get embarrassing review comments about trailing whitespace.

*Acceptance Criteria:*
1. `git commit` on a Python file with an unused import fails with a ruff message identifying the line.
2. `git commit` on a SKILL.md with a missing `## Steps` section fails with the validator error.
3. `git commit` on a file containing a string matching the secret pattern fails with a `detect-secrets` alert.
4. `git commit` with a clean changeset succeeds.

**US-2 — Onboarding**
> As a new team member, I want setup instructions for pre-commit hooks to be in `CONTRIBUTING.md`, so I don't need to ask how to configure my local environment.

*Acceptance Criteria:*
1. `CONTRIBUTING.md` contains a "Local Setup" section with `pip install pre-commit && pre-commit install`.
2. The section explains what each hook does in one line each.
3. Instructions explain how to bypass for emergency commits (`--no-verify`) and document that CI will still catch issues.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Create `.pre-commit-config.yaml` with `repos:` stubs | Dev | 20m |
| T2 | Add `ruff` hook (lint + format check) for `scripts/**/*.py` | Dev | 20m |
| T3 | Add `detect-secrets` hook for all files (exclude `*.env.example` and `configs/mcp/`) | Dev | 30m |
| T4 | Create local hook for `validate_all.py` scoped to `.claude/` and `.github/agents/` staged files | Dev | 30m |
| T5 | Add `trailing-whitespace`, `end-of-file-fixer`, `check-yaml` from `pre-commit-hooks` | Dev | 15m |
| T6 | Pin all hook revisions | Dev | 15m |
| T7 | Add `pre-commit` to `conda-env.yml` and `requirements.txt` | Dev | 10m |
| T8 | Update `CONTRIBUTING.md` with setup section | Dev | 20m |
| T9 | Test locally: trigger each hook with a deliberate violation | Dev | 30m |

**Total estimate: ~3.5h → 3 story points**

---

## `.pre-commit-config.yaml` Skeleton

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: <pinned-sha>
    hooks:
      - id: trailing-whitespace
        types: [markdown]
      - id: end-of-file-fixer
      - id: check-yaml

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: <pinned-sha>
    hooks:
      - id: ruff
        args: [--fix]
        files: ^scripts/
      - id: ruff-format
        files: ^scripts/

  - repo: https://github.com/Yelp/detect-secrets
    rev: <pinned-sha>
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: configs/mcp/

  - repo: local
    hooks:
      - id: validate-skills-agents
        name: Validate skills and agents
        entry: python scripts/repo/validate_all.py
        language: system
        pass_filenames: false
        files: ^(\.claude/|\.github/agents/)
```

---

## Acceptance Criteria (PR-level)

1. `.pre-commit-config.yaml` exists at repo root with all hooks configured.
2. All hook `rev:` values are pinned (no `@latest` or branch names).
3. Running `pre-commit run --all-files` on the current repo passes clean.
4. `CONTRIBUTING.md` has setup instructions.
5. `conda-env.yml` and `requirements.txt` include `pre-commit`.
6. `.secrets.baseline` file committed (from `detect-secrets scan > .secrets.baseline` initial run).

---

## PR Title

`chore(meta): add pre-commit hooks for linting, validation, and secret scanning`
