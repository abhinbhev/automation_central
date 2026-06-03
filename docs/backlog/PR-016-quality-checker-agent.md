# PR-016 — Quality-Checker Agent + Mandatory PR Check

**Phase:** 3 — Intelligence & Self-Improvement
**Type:** New agent pair + CI integration
**Story Points:** 8
**Priority:** P3 — Medium
**Depends on:** PR-003 (CI pipeline — the quality check must run in CI)
**Blocks:** —

---

## Problem Statement

TODO #9 identifies the need for a "dummy agent that acts as a new user and rates the quality of other agents' outputs." The goal is to catch regressions in skill quality — a skill might be technically valid (passes `validate_skill.py`) but produce useless output. No human reviewer would notice this without actually testing the skill. A `quality-checker` agent simulates a naive user, invokes a skill with a sample input, and scores the output against a rubric. This becomes a mandatory gate in the PR process for any new or modified skill.

---

## Scope

### New Agent Pair
- `.claude/agents/quality-checker.agent.md`
- `.github/agents/quality-checker.agent.md`

### New Script
- `scripts/meta/quality_check.py` — runs a skill against a sample input and scores the output

### New Skills
- `.claude/skills/meta/quality-check/SKILL.md`
- `.github/skills/quality-check/SKILL.md`

### CI Integration
- New job in `.github/workflows/validate.yml`: runs quality check on modified skills

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `quality-checker` agent pair: Claude + Copilot |
| R2 | Agent persona: naive new user who tests skills and reports quality findings |
| R3 | `scripts/meta/quality_check.py` — reads a SKILL.md, generates a test invocation from the `## Usage` section, scores the response on a rubric |
| R4 | Quality rubric (scored 1-5 each): Completeness, Format adherence, Actionability, Correctness/accuracy, Clarity |
| R5 | Script outputs a JSON report: `{ skill, score_total, score_breakdown, pass, findings }` |
| R6 | Pass threshold: total score ≥ 18/25 (72%) |
| R7 | `meta/quality-check` skill invokes `quality_check.py` for a given skill path |
| R8 | CI job: on any PR that modifies a `.claude/skills/**` or `.github/skills/**` file, run `quality_check.py` on the changed skills |
| R9 | CI job is advisory (warn, not block) in Phase 3 — promoted to blocking in Phase 4 after rubric is calibrated |
| R10 | `## Example Inputs` section added to SKILL.md contract (optional for now — quality checker uses it when present) |
| R11 | Both agents pass `validate_agent.py` |
| R12 | Catalog and sync check clean |

---

## User Stories

**US-1 — PR author**
> As a contributor adding a new skill, I want an automated quality check to tell me if my skill produces useful output, so I can improve it before asking for human review.

*Acceptance Criteria:*
1. Opening a PR with a new skill triggers the quality-check CI job.
2. The job reports a score breakdown (Completeness, Format, Actionability, Correctness, Clarity).
3. A score below 18/25 generates a CI warning with the specific failing dimensions.
4. In Phase 3, a low score does not block the merge — it generates a WARN annotation.

**US-2 — Reviewer**
> As a reviewer, I want the quality check score on the PR so I can focus my review on the lowest-scoring dimensions rather than re-running the skill myself.

*Acceptance Criteria:*
1. Quality check results are posted as a CI job summary visible in the PR.
2. Summary includes: score, pass/fail, and the specific findings for each dimension.

**US-3 — Skill regression detection**
> As a maintainer, I want the quality check to run on modified skills, so edits to existing SKILL.md content don't accidentally degrade the skill's output quality.

*Acceptance Criteria:*
1. Modifying a SKILL.md body triggers the quality check on that skill.
2. A skill that scored 22/25 before and 14/25 after a body edit generates a WARN in CI.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Design quality rubric: 5 dimensions, 1-5 scale, scoring criteria for each level | Dev | 1h |
| T2 | Create `scripts/meta/quality_check.py` — reads SKILL.md, extracts usage/example, runs LLM eval against rubric | Dev | 2h |
| T3 | Implement JSON output schema and pass/fail threshold logic | Dev | 30m |
| T4 | Create `.claude/agents/quality-checker.agent.md` | Dev | 45m |
| T5 | Create `.github/agents/quality-checker.agent.md` | Dev | 30m |
| T6 | Run `validate_agent.py` on both | Dev | 10m |
| T7 | Create `.claude/skills/meta/quality-check/SKILL.md` | Dev | 30m |
| T8 | Create `.github/skills/quality-check/SKILL.md` | Dev | 20m |
| T9 | Run validators on skills | Dev | 10m |
| T10 | Add CI job to `.github/workflows/validate.yml`: detect changed skill files, run `quality_check.py` on each | Dev | 45m |
| T11 | Test CI job on a deliberately weak skill (missing steps, vague output) | Dev | 30m |
| T12 | Run `generate_catalog.py` and `sync_check.py` | Dev | 10m |

**Total estimate: ~8h → 8 story points**

---

## Quality Rubric

| Dimension | 1 (Poor) | 3 (Acceptable) | 5 (Excellent) |
|-----------|----------|----------------|---------------|
| **Completeness** | Output is missing major sections | Most sections present, minor gaps | All expected sections present |
| **Format adherence** | Output format doesn't match `## Output` spec | Mostly matches, minor deviations | Exactly matches stated format |
| **Actionability** | Output requires significant rework to use | Usable with some edits | Ready to use as-is |
| **Correctness** | Contains factual errors or misunderstands input | Mostly correct, minor issues | Fully correct and accurate |
| **Clarity** | Difficult to read or understand | Reasonably clear | Clear, concise, well-structured |

Pass threshold: ≥ 18/25

---

## Acceptance Criteria (PR-level)

1. Both agent files exist and pass `validate_agent.py`.
2. `quality_check.py` reads a SKILL.md and produces a valid JSON report.
3. Running on the current `create-work-items` skill produces a score ≥ 18/25.
4. Running on a deliberately stripped skill (only frontmatter, no body) produces score < 18/25.
5. CI job runs on PRs modifying skill files and posts results.
6. CI job is `continue-on-error: true` in Phase 3 (advisory, not blocking).
7. Catalog and `sync_check.py` clean.

---

## PR Title

`feat(meta): add quality-checker agent and CI quality-check job for new/modified skills`
