---
name: release-notes
description: "Generate release notes from ADO work items or a commit list"
mode: ask
---

Generate release notes from the provided list of work items, commits, or PR titles.

Group items by category:
- **New Features** — new capabilities added
- **Improvements** — enhancements to existing features
- **Bug Fixes** — issues resolved
- **Breaking Changes** — anything that requires action from users/consumers
- **Infrastructure / DevOps** — pipeline, infra, or tooling changes

For each item:
- One-line summary (plain language, not jargon)
- ADO item number or PR link if available

End with a "Known Issues" section if any items are deferred.

Audience: internal team + stakeholders. Tone: factual and clear.
