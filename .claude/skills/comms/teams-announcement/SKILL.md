---
name: teams-announcement
description: Draft a Microsoft Teams channel announcement — sprint updates, release announcements, incident resolved, team news, or general comms.
domain: comms
requires_script: false
---

## Usage

Invoke with `/teams-announcement` then provide:
- Announcement type (see supported types)
- Key content: what happened, what changed, what people need to know
- Target channel and audience (e.g., `#engineering-general`, management, whole team)
- Urgency: `info`, `action-required`, or `urgent`

## Supported Announcement Types

| Type | Example |
|---|---|
| `sprint-update` | End-of-sprint summary, what shipped, what's next |
| `release` | New version / feature live in production |
| `incident-resolved` | Service restored, brief summary of impact |
| `outage` | Service degradation or planned maintenance |
| `team-news` | New joiner, role change, team restructure |
| `decision` | Important decision made, sharing context with the team |
| `general` | Any other announcement |

## Output

A ready-to-paste Teams message formatted with **bold headings**, clear bullet points, and appropriate emoji for scanability. No corporate filler.

### Sprint Update Example

```
**Sprint 42 — Wrapped ✅**

What shipped:
• Auth service migrated to Azure AD (#1042)
• API rate limiting live across all endpoints (#1048)
• 3 bugs squashed (details in the sprint board)

**Next sprint starts Monday.** Planning doc → [link]

Questions? Drop them here or ping @sprint-lead.
```

### Release Example

```
🚀 **v2.4.0 is live in production**

What's new:
• Corporate SSO via Azure AD
• Improved API reliability with rate limiting

No action needed for users — rollout is automatic.
Full release notes → [link]
```

## Steps

1. Identify the announcement type and urgency
2. Extract the key facts: what, when, impact, action needed
3. Draft the message with the appropriate structure
4. Keep it short: announcements should be scannable in 15 seconds
5. Add a CTA or link if relevant
6. Ask if the user wants to adjust tone or length before posting

## Tone Guidelines

| Audience | Tone |
|---|---|
| Engineering team | Direct, technical shorthand OK, emoji fine |
| Management | Professional, outcome-focused, no jargon |
| Whole org | Plain language, no acronyms, brief |

## Do Not

- Write wall-of-text announcements
- Use corporate filler ("I am pleased to announce...")
- Include sensitive data (user PII, credentials, incident root cause before confirmed)
