# Backlog — automation_central

> Generated from production-readiness review (2026-05-13).
> Each file maps to one pull request. Files are numbered by recommended merge order within each phase.
> Estimates use Fibonacci story points: 1 (≤4h) · 2 (≤1d) · 3 (≤2d) · 5 (≤3d) · 8 (≤5d) · 13 (≤2w)

---

## Phase 0 — Production Gate  *(do first — unblocks everything)*

| PR | Title | Points | Blocks |
|----|-------|--------|--------|
| [PR-001](PR-001-batch-validator.md) | Batch validator script (`validate_all.py`) | 3 | PR-002, PR-003 |
| [PR-002](PR-002-sync-check.md) | Sync-check script (`sync_check.py`) | 5 | PR-003 |
| [PR-003](PR-003-ci-pipeline.md) | CI pipeline — GitHub Actions validation workflow | 3 | — |
| [PR-004](PR-004-pre-commit-hooks.md) | Pre-commit hooks (ruff + validators + secret scan) | 3 | — |
| [PR-005](PR-005-copilot-skill-parity.md) | Copilot skill parity — 12 missing `.github/skills/` counterparts | 8 | — |

**Phase 0 total: 22 points**

---

## Phase 1 — Hardening & Coverage

| PR | Title | Points | Depends On |
|----|-------|--------|------------|
| [PR-006](PR-006-validator-hardening.md) | Validator hardening (WARN→ERROR, strict catalog, refactor) | 3 | PR-001 |
| [PR-007](PR-007-pytest-suite.md) | pytest test suite for repo scripts | 8 | — |
| [PR-008](PR-008-codeowners.md) | CODEOWNERS + PR review enforcement | 1 | PR-003 |
| [PR-009](PR-009-templates-cleanup.md) | Templates cleanup + `requirements.txt` | 2 | — |
| [PR-010](PR-010-quickstart-guides.md) | Quickstart sections for all skills and agents | 5 | — |

**Phase 1 total: 19 points**

---

## Phase 2 — Content Expansion

| PR | Title | Points | Depends On |
|----|-------|--------|------------|
| [PR-011](PR-011-de-agent.md) | Data Engineer agent (Claude + Copilot pair) | 5 | PR-005 |
| [PR-012](PR-012-teams-outlook-agents.md) | Teams Manager + Outlook Manager agents and skills | 8 | PR-005 |
| [PR-013](PR-013-info-agent.md) | Info agent (read-only repo navigator) | 3 | PR-005 |

**Phase 2 total: 16 points**

---

## Phase 3 — Intelligence & Self-Improvement

| PR | Title | Points | Depends On |
|----|-------|--------|------------|
| [PR-014](PR-014-usage-tracking.md) | Usage tracking + analytics script | 5 | — |
| [PR-015](PR-015-orchestrator-agent.md) | Orchestrator agent (delegates to domain agents) | 8 | PR-011, PR-012, PR-013 |
| [PR-016](PR-016-quality-checker-agent.md) | Quality-checker agent + mandatory PR check | 8 | PR-003 |
| [PR-017](PR-017-feedback-loop.md) | Feedback loop + `resolve-feedback` skill | 5 | PR-014 |
| [PR-018](PR-018-patch-notes-agent.md) | Patch-notes newsletter agent + skill | 5 | PR-012 |

**Phase 3 total: 31 points**

---

## Grand Total: 88 story points across 18 PRs
