---
name: incident-runbook
description: Generate an operational runbook for a service or incident type — detection, triage, mitigation steps, escalation contacts, and post-incident actions.
domain: infra
requires_script: false
---

## Usage

Invoke with `/incident-runbook` then provide:
- Service or system name (e.g., "data ingestion pipeline", "API gateway")
- Incident type(s) to cover (e.g., high latency, job failure, auth outage)
- Known failure modes and their mitigations (or describe what you know)
- On-call contacts and escalation path (or use `[TBD]`)

## Output

A structured runbook Markdown document, ready to publish to Confluence or SharePoint.

## Runbook Structure

```markdown
# Runbook: <Service> — <Incident Type>

**Last updated:** YYYY-MM-DD
**Owner:** [team/person]
**Severity:** P1 / P2 / P3

---

## 1. Overview
Brief description of the service and what this runbook covers.

## 2. Symptoms
How operators know this incident is occurring.
- Alerts fired: [alert name / threshold]
- Observable behaviour: [e.g., queue depth spike, 5xx rate > 1%]
- User-reported signs: [e.g., login failures]

## 3. Triage Checklist
Quick checks to narrow down the cause:
- [ ] Check service health dashboard: [URL]
- [ ] Check recent deployments: [deployment URL]
- [ ] Check dependency status: [dependency dashboards]
- [ ] Review logs: [log query or link]

## 4. Mitigation Steps
Ordered steps to restore service:

### Scenario A: [Most likely cause]
1. Step 1
2. Step 2

### Scenario B: [Second most likely cause]
1. ...

## 5. Escalation
| Condition | Escalate to | Contact |
|---|---|---|
| No resolution in 30 min | [Team Lead] | [contact] |
| Data loss suspected | [Data Owner] | [contact] |
| Customer impact | [Eng Manager] | [contact] |

## 6. Post-Incident Actions
- [ ] Update this runbook if a new failure mode was discovered
- [ ] Create an ADO work item for the root cause fix
- [ ] Complete an RCA if P1 or customer-impacting (use `/word-doc` skill with type `rca`)
- [ ] Send comms if external teams were affected (use `/teams-announcement` skill)

## 7. Related Resources
- Monitoring dashboard: [link]
- Architecture diagram: [link]
- Related runbooks: [links]
```

## Steps

1. Identify the service and incident type(s) to document
2. Structure the symptoms section — what alerts/signals indicate the incident
3. Write the triage checklist — quick checks to narrow down root cause
4. Write mitigation steps per scenario (most likely failure modes first)
5. Build the escalation table — ask for contacts or use `[TBD]`
6. Add post-incident action items (these are standard across runbooks)
7. Ask if the user wants to link to existing dashboards, ADO queries, or log workspaces

## Tone

- Imperative voice: "Check the queue depth", not "You should check..."
- Written for someone waking up at 3am — no assumed context
- Every step should be unambiguous and independently executable
