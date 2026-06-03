# PR-010 — Quickstart Guides for All Skills and Agents

**Phase:** 1 — Hardening & Coverage
**Type:** Documentation + validator update
**Story Points:** 5
**Priority:** P2 — High
**Depends on:** —
**Blocks:** —

---

## Problem Statement

TODO #12 identifies the lack of quickstart guides. Currently, a new team member must read `README.md`, `INSTRUCTIONS.md`, and the individual SKILL.md to understand how to use any given automation. There is no "5-second invocation" reference. Skills vary in how much context they need upfront, and users frequently invoke skills with too little input and get generic output. A standardised `## Quickstart` section in every SKILL.md provides the minimum-viable invocation example.

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | Every Claude Code SKILL.md gains a `## Quickstart` section with a minimal working example |
| R2 | Every Copilot SKILL.md gains a `## Quickstart` section |
| R3 | `## Quickstart` section contains: invocation syntax, minimum required input (one concrete example), and expected output summary |
| R4 | `validate_skill.py` updated to WARN (not ERROR) if `## Quickstart` is absent — makes it optional but encouraged |
| R5 | Both `add-skill` and `new-skill` scaffold templates updated to include a `## Quickstart` stub |
| R6 | Both Copilot `add-skill` SKILL.md updated to include the `## Quickstart` stub |
| R7 | `README.md` "How to Use" section updated to reference quickstart sections |
| R8 | `CONTRIBUTING.md` "SKILL.md Required Sections" updated to list `## Quickstart` as recommended |

---

## User Stories

**US-1 — New team member**
> As someone who just joined the team, I want to see a working example for each skill without reading through the full instructions, so I can get value from the repo in my first hour.

*Acceptance Criteria:*
1. Every SKILL.md has a `## Quickstart` section with at least one copy-pasteable invocation.
2. The quickstart includes the exact text to type and describes what output to expect.
3. A new user following the quickstart for `/create-work-items` can produce a valid ADO work item without reading anything else.

**US-2 — Experienced user**
> As a regular user who already knows most skills, I want a quick reference for skills I use occasionally, so I don't need to re-read the full SKILL.md each time.

*Acceptance Criteria:*
1. The `## Quickstart` section is placed consistently (e.g., immediately after frontmatter / at top of body) so it's the first thing seen.
2. For script-backed skills, the quickstart includes both the chat invocation AND the equivalent CLI command.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Update `validate_skill.py` to WARN (not error) on missing `## Quickstart` | Dev | 15m |
| T2 | Update `add-skill/SKILL.md` scaffold template to include `## Quickstart` stub | Dev | 15m |
| T3 | Update `new-skill/SKILL.md` scaffold template | Dev | 10m |
| T4 | Update `.github/skills/add-skill/SKILL.md` | Dev | 10m |
| T5 | Write `## Quickstart` for all 9 `ado` and `comms` skills (Claude + Copilot) | Dev | 1.5h |
| T6 | Write `## Quickstart` for all 7 `coding` and `devops` skills | Dev | 1.5h |
| T7 | Write `## Quickstart` for all `office`, `docs`, and `infra` skills | Dev | 1.5h |
| T8 | Write `## Quickstart` for all `data-ml` and `meta` skills | Dev | 1h |
| T9 | Write `## Quickstart` for all 25 Copilot skills (mirror/adapt from Claude) | Dev | 1.5h |
| T10 | Update `README.md` "How to Use" section | Dev | 20m |
| T11 | Update `CONTRIBUTING.md` recommended sections | Dev | 15m |
| T12 | Run `generate_catalog.py` — no catalog changes expected, but confirm clean | Dev | 5m |

**Total estimate: ~10h → 5 story points**

---

## Quickstart Section Format (Standard)

```markdown
## Quickstart

**Invoke:** `/skill-name` in Claude Code (or Copilot Chat)

**Minimum input:**
> "Create a User Story for the login feature: users should be able to reset their password via email."

**Output:** A formatted work item preview table with Title, Description, Acceptance Criteria, Type=Story, Priority=2. Confirm to create in ADO.

**CLI equivalent (if script-backed):**
`python scripts/ado/create_work_items.py --spec specs/login-story.json`
```

---

## Acceptance Criteria (PR-level)

1. All 37 Claude SKILL.md files have a `## Quickstart` section.
2. All 25 (→37 post-PR-005) Copilot SKILL.md files have a `## Quickstart` section.
3. `validate_skill.py` WARNs (but does not ERROR) on a SKILL.md missing `## Quickstart`.
4. `add-skill` and `new-skill` scaffold templates include the `## Quickstart` stub.
5. `validate_all.py` on the updated repo shows 0 errors (WARNs for any remaining missing quickstarts are acceptable until this PR's scope is complete).

---

## PR Title

`docs: add Quickstart sections to all skills and agents for faster onboarding`
