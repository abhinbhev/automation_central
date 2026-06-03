# PR-018 — Patch-Notes Newsletter Agent + Skill

**Phase:** 3 — Intelligence & Self-Improvement
**Type:** New agent pair + new skill + script enhancement
**Story Points:** 5
**Priority:** P3 — Medium
**Depends on:** PR-012 (MS Graph mail via `outlook-manager` pattern)
**Blocks:** —

---

## Problem Statement

TODO #15 identifies the need for a patch-notes newsletter agent that automatically generates release notes from merged PRs and distributes them to stakeholders on a regular cadence (e.g. monthly). Currently, `scripts/ado/release_notes.py` exists and generates release notes from ADO work items, but there is no agent or skill that orchestrates the full newsletter workflow: collect merged PRs → format as newsletter → distribute via email or Teams.

---

## Scope

### New Agent Pair
- `.claude/agents/patch-notes-agent.agent.md`
- `.github/agents/patch-notes-agent.agent.md`

### New Skills
- `.claude/skills/comms/patch-notes/SKILL.md`
- `.github/skills/patch-notes/SKILL.md`

### Script Enhancement
- `scripts/ado/release_notes.py` — extend with `--newsletter` flag that formats output as a stakeholder-friendly newsletter (not a developer changelog)

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `patch-notes-agent` agent pair: Claude + Copilot |
| R2 | Agent orchestrates: pull closed ADO items + merged PRs → format newsletter → distribute |
| R3 | Newsletter format: executive summary, highlights (new automations), improvements, deprecated items, team call-to-action |
| R4 | `comms/patch-notes` skill: full newsletter generation workflow |
| R5 | `release_notes.py --newsletter` flag: outputs stakeholder-friendly newsletter Markdown (vs developer changelog) |
| R6 | Distribution options: (a) Markdown file for manual send, (b) MS Graph mail draft (if MCP available), (c) Teams channel post draft |
| R7 | Agent boundary: never sends automatically — always presents draft for review and explicit confirmation |
| R8 | Skill supports: `--period month|quarter` to scope the release period |
| R9 | Both agents pass `validate_agent.py`; both skills pass validators |
| R10 | Catalog and sync check clean |

---

## User Stories

**US-1 — Maintainer doing monthly newsletter**
> As a maintainer, I want to run `/patch-notes` and get a formatted newsletter covering the past month's merged automations and improvements, so I can send it to stakeholders without manually collating changes.

*Acceptance Criteria:*
1. Invoking `/patch-notes` asks: period (month/quarter), stakeholder list, distribution channel (email/Teams/file).
2. Produces a newsletter with sections: Executive Summary, New Automations, Improvements, Deprecated, Next Steps.
3. Newsletter is non-technical — written for stakeholders, not engineers.
4. Agent presents draft for review before offering to send.

**US-2 — Stakeholder**
> As a stakeholder receiving the newsletter, I want a clear summary of what new automations are available and how to use them, so I can adopt new tools without reading the repo.

*Acceptance Criteria:*
1. Each "New Automation" entry includes: name, what it does (1-2 sentences), and how to invoke it.
2. Newsletter includes a "Quick Links" section with links to the catalog and `CONTRIBUTING.md`.
3. Newsletter is formatted for email readability (short paragraphs, clear headings).

**US-3 — Distribution**
> As a maintainer, I want to choose how to distribute: email draft (Outlook), Teams channel post, or saved Markdown file.

*Acceptance Criteria:*
1. If MS Graph MCP unavailable: outputs Markdown file to `working_directory/patch-notes-<YYYY-MM>.md`.
2. If MS Graph MCP available: produces email draft ready for review in `outlook-manager` format.
3. Teams distribution option produces a `teams-manager`-compatible announcement draft.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Define newsletter format and section structure | Dev | 30m |
| T2 | Create `.claude/agents/patch-notes-agent.agent.md` | Dev | 45m |
| T3 | Create `.github/agents/patch-notes-agent.agent.md` | Dev | 30m |
| T4 | Run `validate_agent.py` on both | Dev | 10m |
| T5 | Extend `scripts/ado/release_notes.py` with `--newsletter` flag and newsletter formatter | Dev | 1.5h |
| T6 | Create `.claude/skills/comms/patch-notes/SKILL.md` | Dev | 45m |
| T7 | Run `validate_skill.py` on patch-notes | Dev | 5m |
| T8 | Create `.github/skills/patch-notes/SKILL.md` | Dev | 20m |
| T9 | Add distribution option logic to skill body (file/email/Teams fallback pattern) | Dev | 20m |
| T10 | Run `generate_catalog.py` and `sync_check.py` | Dev | 10m |
| T11 | Update `README.md` agent table | Dev | 10m |

**Total estimate: ~6h → 5 story points**

---

## Newsletter Section Structure

```markdown
# automation_central — May 2026 Update

## What's New This Month
Brief executive summary (2-3 sentences).

## New Automations
- **`/eda-report`** — Generate exploratory data analysis reports from schema or summary stats. Invoke in Claude Code or Copilot Chat.
- **`/patch-notes`** — (This skill!) Auto-generate and distribute monthly automation newsletters.

## Improvements
- `/create-work-items` — Now supports bulk creation from a JSON spec.
- Validation CI gate added — all new skills are automatically validated on PR.

## Deprecated / Removed
- None this month.

## How to Get Started
See the [Automation Catalog](../docs/automation-catalog.md) for the full list of available skills.
Questions? Ask the `info-agent` — type `@info-agent` and ask anything about the repo.

## Next Steps / Call to Action
- Try `/orchestrate` for multi-step cross-domain workflows.
- Submit feedback on any skill: `/submit-feedback`.
```

---

## Acceptance Criteria (PR-level)

1. Both agent files exist and pass `validate_agent.py`.
2. Both `patch-notes` skills (Claude + Copilot) pass validators.
3. `release_notes.py --newsletter` produces the newsletter format (not the developer changelog format).
4. Agent boundary explicitly states "never send without confirmation."
5. Skill body includes all three distribution options (file, email draft, Teams draft).
6. Catalog updated; `sync_check.py` clean.

---

## PR Title

`feat(comms): add patch-notes-agent and patch-notes skill for monthly automation newsletters`
