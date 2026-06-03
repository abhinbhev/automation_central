# PR-012 — Teams Manager + Outlook Manager Agents and Skills

**Phase:** 2 — Content Expansion
**Type:** New agent pairs + new skills
**Story Points:** 8
**Priority:** P3 — Medium
**Depends on:** PR-005 (Copilot parity)
**Blocks:** PR-015 (orchestrator), PR-018 (patch-notes agent uses MS Graph mail)

---

## Problem Statement

TODOs #4 and #5 identify missing Teams and Outlook manager agents. The `comms` domain has 3 skills (`meeting-minutes`, `email-draft`, `teams-announcement`) but no dedicated communication agents. MS Graph MCP server is documented but no agent is configured to use it for sending or structuring comms. Communication workflows are currently ad-hoc — users invoke comms skills without a persona that understands messaging context, audience, or stakeholder protocols.

---

## Scope

### New Agent Pairs (2 pairs)
- `.claude/agents/teams-manager.agent.md` + `.github/agents/teams-manager.agent.md`
- `.claude/agents/outlook-manager.agent.md` + `.github/agents/outlook-manager.agent.md`

### Skills to Reference (existing)
- `comms/meeting-minutes`
- `comms/email-draft`
- `comms/teams-announcement`

### New Skills
- `comms/teams-channel-post` — structured Teams channel message (Claude + Copilot)
- `comms/meeting-invite` — draft a calendar meeting invite spec (Claude + Copilot)
- `comms/stakeholder-update` — structured stakeholder update for email or Teams (Claude + Copilot)

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `teams-manager` agent pair created and validated |
| R2 | `outlook-manager` agent pair created and validated |
| R3 | Both agents reference all `comms/` skills |
| R4 | New `comms/teams-channel-post` skill (Claude + Copilot) |
| R5 | New `comms/meeting-invite` skill (Claude + Copilot) |
| R6 | New `comms/stakeholder-update` skill (Claude + Copilot) |
| R7 | All skills pass `validate_skill.py` |
| R8 | All agents pass `validate_agent.py` |
| R9 | All skills have Copilot counterparts (SYNC RULE) |
| R10 | Each agent's boundaries include: "Always ask before sending — never send without explicit user confirmation" |
| R11 | Each skill body includes an MCP fallback: if `ms-graph` server is unavailable, output a formatted draft for manual send |
| R12 | Catalog updated; `sync_check.py` clean |

---

## User Stories

**US-1 — Teams announcements**
> As a team lead, I want a `teams-manager` agent that can draft, structure, and prepare Teams channel announcements for me, so I don't have to write them from scratch.

*Acceptance Criteria:*
1. Using `teams-manager` + `/teams-announcement` produces a formatted Teams message with subject, body, @mentions placeholder, and channel recommendation.
2. The agent asks for confirmation before preparing any send-ready output.
3. If MS Graph MCP is unavailable, the agent produces a Markdown draft for manual copy-paste.

**US-2 — Email drafting**
> As a manager, I want an `outlook-manager` agent that understands email context — tone, audience, thread continuation — and drafts emails I can review and send.

*Acceptance Criteria:*
1. Using `outlook-manager` + `/email-draft` produces a full email with To, Subject, Body sections.
2. The agent asks: audience, tone (formal/casual), any attachments to mention.
3. The agent never sends email autonomously — it always produces a draft for review.
4. MS Graph fallback: if MCP unavailable, output formatted draft for manual send.

**US-3 — Stakeholder updates**
> As a project manager, I want a `/stakeholder-update` skill to produce a structured status update suitable for either a Teams post or an email.

*Acceptance Criteria:*
1. Skill produces output with sections: Status (RAG), Summary, Key Updates, Blockers, Next Steps.
2. Output is dual-format: Teams-friendly (short, emoji) and email-friendly (full paragraphs).
3. Skill available in both Claude and Copilot.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Define teams-manager persona and boundaries | Dev | 20m |
| T2 | Create `.claude/agents/teams-manager.agent.md` | Dev | 45m |
| T3 | Create `.github/agents/teams-manager.agent.md` | Dev | 30m |
| T4 | Define outlook-manager persona and boundaries | Dev | 20m |
| T5 | Create `.claude/agents/outlook-manager.agent.md` | Dev | 45m |
| T6 | Create `.github/agents/outlook-manager.agent.md` | Dev | 30m |
| T7 | Create `.claude/skills/comms/teams-channel-post/SKILL.md` | Dev | 40m |
| T8 | Create `.github/skills/teams-channel-post/SKILL.md` | Dev | 20m |
| T9 | Create `.claude/skills/comms/meeting-invite/SKILL.md` | Dev | 40m |
| T10 | Create `.github/skills/meeting-invite/SKILL.md` | Dev | 20m |
| T11 | Create `.claude/skills/comms/stakeholder-update/SKILL.md` | Dev | 40m |
| T12 | Create `.github/skills/stakeholder-update/SKILL.md` | Dev | 20m |
| T13 | Run all validators on new files | Dev | 20m |
| T14 | Run `generate_catalog.py` and `sync_check.py` | Dev | 10m |
| T15 | Update `README.md` agent table | Dev | 10m |

**Total estimate: ~8h → 8 story points**

---

## Agent Persona Outlines

### `teams-manager`
**Description:** Microsoft Teams communication specialist — drafts announcements, channel posts, and meeting minutes for Teams. Requires explicit confirmation before preparing any send-ready output.
**Tools:** read, search (no execute — cannot send without confirmation)
**Key boundary:** Never send to Teams autonomously. Always produce a draft with confirmation prompt.

### `outlook-manager`
**Description:** Outlook email specialist — drafts, structures, and formats emails with appropriate tone and audience context. Produces drafts only; never sends without explicit user approval.
**Tools:** read, search (no execute)
**Key boundary:** Always present draft for review. Offer to refine tone or structure before finalising.

---

## Acceptance Criteria (PR-level)

1. Both agent pairs exist and pass `validate_agent.py` with zero errors.
2. All 3 new skills (both Claude and Copilot variants) exist and pass validators.
3. Every new skill body includes an explicit MCP fallback instruction.
4. Every agent file includes "always ask before sending" in the Boundaries section.
5. Catalog updated; `sync_check.py` reports zero new issues.
6. `README.md` agent table includes `teams-manager` and `outlook-manager`.

---

## PR Title

`feat(comms): add teams-manager and outlook-manager agents with 3 new comms skills`
