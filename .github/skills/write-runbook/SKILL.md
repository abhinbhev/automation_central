---
name: write-runbook
description: "Generate an operational runbook for a service, pipeline, or incident type — diagnosis, remediation, escalation, rollback"
mode: agent
---

Generate an operational runbook for the following service or scenario.

**Provide:**
- Service or system name
- Trigger: what alert, error, or event sends someone to this runbook?
- Description of the service and what a healthy state looks like
- Known failure modes or past incidents (if any)

**Optionally specify:**
- Runbook type: `incident` | `deployment` | `maintenance` | `on-call`
- Escalation contacts or on-call rotation

**Clarify before writing if:**
- The trigger/alert is not defined — a runbook without a clear entry point is unusable
- The deployment platform (AKS, Azure Functions, App Service, etc.) is unknown, as commands differ

---

## Runbook structure (always produce all sections)

```markdown
# Runbook: [Service] — [Type]
**Owner:** [team] | **On-call:** [contact] | **Last updated:** YYYY-MM-DD

## Service Overview
[What it does, key dependencies, healthy-state indicators]

**Key links:** Azure Portal | GitHub | ADO | Monitoring dashboard

---

## Trigger / Alert
[Alert name, threshold, monitoring source]

---

## Diagnosis

### Step 1 — Confirm the issue
[Commands to verify the problem]

### Step 2 — Check dependencies
[What to check upstream/downstream]

### Step 3 — Read logs
[Where logs are, what to grep for]

### Symptom → Cause table
| Symptom | Likely cause | Go to |
|---------|-------------|-------|

---

## Remediation

### Option A — [Primary fix]
[When to use, commands, expected outcome]

### Option B — Rollback
[When to use (e.g. A didn't resolve in 30 min), rollback commands]

---

## Escalation
| Condition | Action | Contact |
|-----------|--------|---------|

---

## Post-Incident
1. Create ADO bug with timeline and root cause
2. Update this runbook if any steps were wrong
3. Log in incident tracker
4. Schedule post-mortem if P1/P2
```

**Rules:**
- All commands must be cross-checked against the actual codebase or deployment config
- Flag any command that cannot be verified — do not invent commands
- No section left empty — if something is unknown, ask before drafting
- Show for review before writing to `docs/runbooks/<service-name>.md`
