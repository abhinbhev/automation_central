---
mode: agent
description: Capture an architecture or technical decision as a structured ADR with context, options, decision, and consequences
---

Write an Architecture Decision Record (ADR) for the following decision.

**Provide:**
- The decision being made or already made
- The context: what problem, constraint, or requirement forced a decision?
- Options that were considered (even briefly)
- The chosen option and the reason

**Clarify before writing if:**
- The ADR status is unknown (`Proposed` / `Accepted` / `Deprecated` / `Superseded`)
- The ADO work item reference is relevant and unknown

First, check `docs/adr/` to determine the next available ADR number.

---

## ADR structure (always produce all sections)

```markdown
# NNNN — [Decision Title]

**Status:** Accepted
**Date:** YYYY-MM-DD
**Owner:** [Team / Person]
**ADO item:** AB#[ID]

---

## Context
[What situation forced a decision? Current state, pain point, constraint.
Factual — not advocacy for the chosen option.]

## Decision
[One or two sentences. "We will use X for Y because Z."]

## Options Considered

| Option | Pros | Cons | Rejected because |
|--------|------|------|-----------------|
| Option A (chosen) | ... | ... | — |
| Option B | ... | ... | [reason] |

## Consequences

**Positive:**
- ...

**Negative / Trade-offs:**
- ...

**Risks:**
- ...

## Implementation Notes
[Non-obvious steps to act on this decision — config changes, migrations, comms]

## Related
- ADR-NNNN: [related decision]
- Runbook: [link if operational impact]
- ADO: AB#[ID]
```

**Rules:**
- Context section must not advocate — save that for the Decision section
- Options table must include the chosen option as the first row
- Consequences must list at least one negative trade-off — no decision is free
- Show the draft for review before writing to `docs/adr/NNNN-<kebab-title>.md`
