---
name: write-runbook
description: Generate an operational runbook for a service, pipeline, or incident type — covers diagnosis, remediation, escalation, and rollback
domain: docs
requires_script: false
---

## Usage

Invoke with `/write-runbook` then provide:
- **Service or system name**
- **Trigger:** what alert, error, or event prompts someone to open this runbook?
- **Description:** what does the service do? what does a healthy state look like?
- Any known failure modes or past incidents to document

Optionally specify:
- Runbook type: `incident` | `deployment` | `maintenance` | `on-call`
- On-call contacts or escalation chain

## Output

A complete runbook at `docs/runbooks/<service-name>.md`:

```markdown
# Runbook: [Service Name] — [Type]

**Service:** [name]
**Owner:** [team]
**On-call:** [rotation or contact]
**Last updated:** YYYY-MM-DD
**Linked ADO:** AB#[ID] (if applicable)

---

## Service Overview

[2–3 sentences: what the service does, its dependencies, and what a healthy state looks like]

**Key links:**
- Azure Portal: [link]
- GitHub repo: [link]
- ADO board: [link]
- Monitoring dashboard: [link]

---

## Trigger / Alert

[What alert or signal sends someone to this runbook?
Include: alert name, threshold, source (Azure Monitor / Grafana / etc.)]

---

## Diagnosis

### Step 1 — Confirm the issue
```bash
# Commands to verify the problem exists
```

### Step 2 — Check dependencies
[What upstream/downstream services to check, and how]

### Step 3 — Read logs
```bash
# Where to find logs and what to look for
```

### Symptom → Cause table

| Symptom | Likely cause | Go to |
|---------|-------------|-------|
| [error message / behaviour] | [root cause] | Remediation A |

---

## Remediation

### Option A — [Name of fix]

**When to use:** [condition]

```bash
# Step-by-step commands
```

**Expected outcome:** [what success looks like]

### Option B — Rollback

**When to use:** when remediation A doesn't resolve within [X] minutes

```bash
# Rollback commands
```

---

## Escalation

| Condition | Action | Contact |
|-----------|--------|---------|
| Issue not resolved in 30 min | Page on-call lead | [name / Teams handle] |
| Data loss risk | Escalate to engineering manager | [name] |
| External dependency down | Raise with [vendor] | [contact] |

---

## Post-Incident

1. Create ADO bug item with timeline and root cause
2. Update this runbook if any steps were wrong or missing
3. Add a row to the [incident log](../incident-log.xlsx)
4. Schedule a blameless post-mortem if severity was P1/P2
```

## Steps

1. Ask for any missing inputs (trigger, service description, failure modes)
2. Read any related code, pipeline YAML, or existing docs to populate accurate commands
3. Draft the full runbook — populate all sections, no placeholders
4. Flag any commands that could not be verified against the codebase
5. Show for review; ask if escalation chain and contacts are correct
6. Write to `docs/runbooks/<service-name>.md` on approval
