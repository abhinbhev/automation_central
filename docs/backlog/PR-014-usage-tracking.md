# PR-014 — Usage Tracking and Analytics

**Phase:** 3 — Intelligence & Self-Improvement
**Type:** New script + meta skill
**Story Points:** 5
**Priority:** P3 — Medium
**Depends on:** —
**Blocks:** PR-017 (feedback loop needs usage data)

---

## Problem Statement

TODO #7 identifies the absence of usage tracking. Currently there is no way to know which skills are being used, which agents are popular, which workflows are never invoked, or whether automation adoption is growing. Without this data, improvements are driven by assumptions rather than evidence. The feedback loop (PR-017) and quality checker (PR-016) both depend on having a usage signal to prioritise what to improve.

The implementation must be lightweight (file-based, no external service dependency) and privacy-respecting (no PII, no prompt content — only skill names, agent names, and timestamps).

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `scripts/meta/usage_tracker.py` — appends structured JSON event to a local log file |
| R2 | Log file: `working_directory/usage_log.jsonl` (JSONL format, one event per line) |
| R3 | Event schema: `{ "ts": ISO8601, "framework": "claude|copilot", "type": "skill|agent", "name": "<name>", "domain": "<domain>|null" }` |
| R4 | No PII, no prompt content, no output content logged — only the invocation metadata |
| R5 | `scripts/meta/usage_report.py` — reads `usage_log.jsonl` and generates a Markdown report |
| R6 | Report includes: top 10 skills by invocation count, top agents, usage by domain, usage over time (weekly buckets) |
| R7 | `working_directory/usage_log.jsonl` added to `.gitignore` (local only — not committed) |
| R8 | New Claude skill: `.claude/skills/meta/usage-report/SKILL.md` — invokes `usage_report.py` and displays results |
| R9 | New Copilot skill: `.github/skills/usage-report/SKILL.md` |
| R10 | Usage tracking is opt-in per-session — a skill or agent can log an event by calling `usage_tracker.py` |
| R11 | `usage_tracker.py` is safe to run when no log file exists (creates it on first run) |

---

## User Stories

**US-1 — Maintainer**
> As a maintainer, I want to know which skills and agents are actually being used, so I can prioritise improvements and identify abandoned automations for deprecation.

*Acceptance Criteria:*
1. Running `/usage-report` produces a Markdown table showing invocation counts per skill.
2. Report shows weekly trends for the past 4 weeks.
3. Report highlights skills with zero invocations in the past 30 days as candidates for review.

**US-2 — Team lead**
> As a team lead, I want a summary of automation adoption (how many skills invoked per week) to include in sprint reviews.

*Acceptance Criteria:*
1. `usage_report.py --format markdown` produces a copy-pasteable summary table.
2. `usage_report.py --since 2026-04-01` filters to a date range.
3. Output includes: total invocations, unique skills used, most active domain.

**US-3 — Privacy boundary**
> As a team member, I want to be certain usage tracking never logs what I asked or what the output was — only that I invoked a skill.

*Acceptance Criteria:*
1. `usage_log.jsonl` entries contain only `ts`, `framework`, `type`, `name`, `domain` — no other fields.
2. `usage_tracker.py` has no parameter for logging content or user identity.
3. `working_directory/usage_log.jsonl` is in `.gitignore`.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Create `scripts/meta/` directory | Dev | 5m |
| T2 | Create `scripts/meta/usage_tracker.py` — appends JSON event to JSONL file | Dev | 45m |
| T3 | Define event schema and validate it in `usage_tracker.py` using a `UsageEvent` dataclass | Dev | 20m |
| T4 | Create `scripts/meta/usage_report.py` — reads JSONL, generates report | Dev | 1.5h |
| T5 | Implement `--since` date filter and `--format` (markdown/json) options | Dev | 30m |
| T6 | Implement "zero-usage skills" section: cross-reference catalog against log | Dev | 30m |
| T7 | Add `working_directory/usage_log.jsonl` to `.gitignore` | Dev | 5m |
| T8 | Create `.claude/skills/meta/usage-report/SKILL.md` | Dev | 30m |
| T9 | Run `validate_skill.py` on usage-report | Dev | 5m |
| T10 | Create `.github/skills/usage-report/SKILL.md` | Dev | 20m |
| T11 | Run `generate_catalog.py` | Dev | 5m |
| T12 | Add `usage_tracker` + `usage_report` to `agent-skill-manager` skills list | Dev | 10m |
| T13 | Write unit tests for `usage_tracker.py` and `usage_report.py` | Dev | 45m |

**Total estimate: ~7h → 5 story points**

---

## Event Schema

```json
{
  "ts": "2026-05-13T15:30:00+05:30",
  "framework": "claude",
  "type": "skill",
  "name": "create-work-items",
  "domain": "ado"
}
```

---

## Acceptance Criteria (PR-level)

1. `scripts/meta/usage_tracker.py` appends a valid event to `working_directory/usage_log.jsonl`.
2. Running it twice produces two lines in the JSONL file.
3. `scripts/meta/usage_report.py` reads the log and produces a Markdown report with invocation counts.
4. `working_directory/usage_log.jsonl` is in `.gitignore`.
5. Both `usage-report` Claude and Copilot skills pass validators.
6. Event schema contains no PII or content fields.
7. Unit tests pass for both scripts.

---

## PR Title

`feat(meta): add usage tracking and analytics — usage_tracker.py, usage_report.py, usage-report skill`
