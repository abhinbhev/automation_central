---
name: write-adr
description: Capture an architecture or technical decision as a structured ADR with context, decision, and consequences
domain: docs
requires_script: false
---

## Usage

Invoke with `/write-adr` then provide:
- A description of the decision being made or already made
- The context: what problem prompted this decision?
- Options considered (even if brief)
- The chosen option and why

Optionally specify:
- **ADR number** (e.g. `0012`) — the agent will check `docs/adr/` to auto-increment if not given
- **Status:** `Proposed` | `Accepted` | `Deprecated` | `Superseded by ADR-NNNN`

## Output

A complete ADR at `docs/adr/NNNN-<kebab-title>.md`:

```markdown
# NNNN — [Decision Title]

**Status:** Accepted
**Date:** YYYY-MM-DD
**Owner:** [Team / Person]
**ADO item:** AB#[ID] (if applicable)

---

## Context

[What situation, constraint, or requirement forced a decision?
What is the current state? What pain point exists?
Keep it factual — this is not the place to argue for the decision.]

## Decision

[State the decision clearly in one or two sentences.
"We will use X for Y because Z."]

## Options Considered

| Option | Pros | Cons | Rejected because |
|--------|------|------|-----------------|
| Option A (chosen) | ... | ... | — |
| Option B | ... | ... | [reason] |
| Option C | ... | ... | [reason] |

## Consequences

**Positive:**
- ...

**Negative / Trade-offs:**
- ...

**Risks:**
- ...

## Implementation Notes

[Any non-obvious steps required to act on this decision — config changes, migrations, comms needed]

## Related

- ADR-NNNN: [related decision]
- Runbook: [link if operational impact]
- ADO: AB#[ID]
```

## Steps

1. Ask for any missing inputs (context, options, outcome)
2. Check `docs/adr/` for the next available ADR number
3. Draft the full ADR — all sections populated, no placeholders
4. Show for review and ask if options table is complete
5. Write to `docs/adr/NNNN-<kebab-title>.md` on approval
