# PR-017 — Feedback Loop + `resolve-feedback` Skill

**Phase:** 3 — Intelligence & Self-Improvement
**Type:** New script + new skills
**Story Points:** 5
**Priority:** P3 — Medium
**Depends on:** PR-014 (usage tracking — feedback complements usage data)
**Blocks:** —

---

## Problem Statement

TODO #8 identifies the need for a feedback loop: users should be able to rate skill outputs, and there should be a periodic resolution process that reviews feedback and generates improvement plans. Currently, there is no mechanism to capture qualitative feedback on skill quality or to systematically act on it. This PR adds a lightweight feedback capture mechanism and a `resolve-feedback` skill that the `agent-skill-manager` can run monthly to generate improvement plans.

---

## Scope

### New Script
- `scripts/meta/feedback_collector.py` — appends structured feedback to `working_directory/feedback_log.jsonl`

### New Skills
- `.claude/skills/meta/submit-feedback/SKILL.md` — user-facing: rate a skill output
- `.claude/skills/meta/resolve-feedback/SKILL.md` — maintainer-facing: review feedback and generate improvement plan
- `.github/skills/submit-feedback/SKILL.md` (Copilot)
- `.github/skills/resolve-feedback/SKILL.md` (Copilot)

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `scripts/meta/feedback_collector.py` appends a feedback event to `working_directory/feedback_log.jsonl` |
| R2 | Feedback event schema: `{ "ts": ISO8601, "skill": "<name>", "rating": 1-5, "comment": "<optional text>", "framework": "claude|copilot" }` |
| R3 | `working_directory/feedback_log.jsonl` added to `.gitignore` |
| R4 | `/submit-feedback` skill: prompts user for skill name, rating (1-5), and optional comment; calls `feedback_collector.py` |
| R5 | `/resolve-feedback` skill: reads `feedback_log.jsonl`, aggregates by skill, identifies low-rated skills (avg < 3), generates a structured improvement plan |
| R6 | Improvement plan format: skill name, average rating, rating distribution, sample comments, recommended actions |
| R7 | `/resolve-feedback` is intended to be run monthly by the `agent-skill-manager` or a maintainer |
| R8 | Both submit and resolve skills have Claude and Copilot counterparts |
| R9 | All skills and scripts follow repo standards |
| R10 | `agent-skill-manager` agent updated to include `/submit-feedback` and `/resolve-feedback` in its skill list |

---

## User Stories

**US-1 — User after invoking a skill**
> As a user, I want to quickly rate a skill output (1-5) with an optional comment, so I can flag poor outputs for improvement without filing a formal issue.

*Acceptance Criteria:*
1. Invoking `/submit-feedback` asks: which skill, rating (1-5), optional comment.
2. The feedback is appended to `working_directory/feedback_log.jsonl`.
3. The process takes under 30 seconds.
4. No PII is stored — only the skill name, rating, comment, and timestamp.

**US-2 — Maintainer doing monthly review**
> As a maintainer, I want to run `/resolve-feedback` once a month and get a prioritised list of skills to improve, so I can plan improvement work for the next sprint.

*Acceptance Criteria:*
1. `/resolve-feedback` produces a Markdown report with skills sorted by average rating (ascending).
2. Skills with fewer than 3 ratings are flagged as "insufficient data."
3. Each skill entry shows: average rating, number of ratings, sample comments (if any), and 2-3 recommended actions.
4. The report is saved to `working_directory/feedback-report-<YYYY-MM>.md`.

**US-3 — Systematic improvement**
> As a maintainer, I want the feedback process to produce actionable ADO work items for low-rated skills, so improvement tasks are tracked like all other work.

*Acceptance Criteria:*
1. `/resolve-feedback` optionally creates ADO tasks for skills with avg rating < 3 (with user confirmation).
2. Each ADO task title: `Improve skill quality: <skill-name> (avg rating: X.X/5)`.
3. Task description includes the sample comments from the feedback log.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Create `scripts/meta/feedback_collector.py` — append feedback event to JSONL | Dev | 30m |
| T2 | Define feedback event schema with dataclass validation | Dev | 20m |
| T3 | Create `.claude/skills/meta/submit-feedback/SKILL.md` | Dev | 30m |
| T4 | Create `.github/skills/submit-feedback/SKILL.md` | Dev | 15m |
| T5 | Create report generation logic in `feedback_collector.py` (or separate `feedback_report.py`) | Dev | 1h |
| T6 | Create `.claude/skills/meta/resolve-feedback/SKILL.md` — read log, aggregate, generate plan | Dev | 45m |
| T7 | Create `.github/skills/resolve-feedback/SKILL.md` | Dev | 20m |
| T8 | Add optional ADO task creation step to `resolve-feedback` skill (reuse `create_work_items.py`) | Dev | 30m |
| T9 | Add `working_directory/feedback_log.jsonl` to `.gitignore` | Dev | 5m |
| T10 | Update `agent-skill-manager` (Claude + Copilot) skills list and `## Relevant Skills` | Dev | 20m |
| T11 | Run all validators, `generate_catalog.py`, `sync_check.py` | Dev | 15m |
| T12 | Write unit tests for `feedback_collector.py` | Dev | 30m |

**Total estimate: ~6h → 5 story points**

---

## Feedback Event Schema

```json
{
  "ts": "2026-05-13T15:30:00+05:30",
  "skill": "create-work-items",
  "rating": 4,
  "comment": "Output was well structured but missed the area path field",
  "framework": "claude"
}
```

---

## Acceptance Criteria (PR-level)

1. `feedback_collector.py` appends a valid event to `working_directory/feedback_log.jsonl`.
2. `/submit-feedback` skill invokes `feedback_collector.py` and confirms submission.
3. `/resolve-feedback` reads the log and produces a Markdown improvement plan.
4. Low-rated skills (avg < 3) are highlighted and have recommended actions.
5. Both submit and resolve skills exist for Claude and Copilot.
6. All validators pass; catalog and sync check clean.
7. `feedback_log.jsonl` is in `.gitignore`.

---

## PR Title

`feat(meta): add feedback loop — submit-feedback and resolve-feedback skills with feedback_collector.py`
