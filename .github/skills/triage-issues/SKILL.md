---
name: triage-issues
description: "Triage and structure GitHub issues from freetext, bug reports, or discussion threads"
mode: ask
---

Triage the following bug reports, feature requests, or discussion into well-structured GitHub issues.

For each issue, produce:

```
**Title:** [Concise, action-oriented — e.g. "Fix: ...", "Add: ...", "Chore: ..."]
**Type:** bug | enhancement | documentation | chore
**Priority:** critical | high | medium | low
**Labels:** [comma-separated list]
**Suggested assignee:** [name or "unassigned" — base on area of code or recent contributors]

**Description:**
[What is happening / what is wanted. Be specific.]

**Steps to reproduce (bugs only):**
1. ...
2. ...

**Expected behaviour:** ...
**Actual behaviour:** ...

**Acceptance criteria:**
- [ ] ...
- [ ] ...

**Linked ADO item:** AB#[ID] (if known, else "none — suggest linking")
```

**Triage rules:**
- A `critical` bug blocks production or causes data loss — flag for immediate attention
- Separate compound issues into individual items — one concern per issue
- Add `needs-triage` label if more information is needed before estimating
- Flag any security-relevant issues with `security` label and do not publicly disclose exploit details

Show all issues for review before creating.
