---
mode: agent
description: Generate a complete README for a project, module, or script from the codebase or a description
---

Generate a complete `README.md` for the specified project, module, or script.

**Input — provide one of:**
- A path to explore (the agent will read the code)
- A description of the project if code doesn't exist yet
- An existing README to rewrite or expand

**Clarify before writing if:**
- Target audience is not clear (engineers / ops / external consumers / new joiners)
- Whether this is a project-level README or a module/script-level README

---

## README structure (always produce all sections)

```markdown
# [Project / Module Name]
> [One-line description — what it does and for whom]

## Overview
[2–3 sentences: problem it solves, how it fits in the broader system]

## Prerequisites
[Runtime versions, env vars, required tools]

## Installation / Setup
[Step-by-step commands — tested and copy-pasteable]

## Usage
[CLI examples, function calls, or API examples with real values — not pseudocode]

## Configuration
[Table: name | required | default | description — for every env var and config option]

## Project Structure
[File tree with one-line description of each file/folder]

## How it works
[Brief technical explanation: architecture, data flow, key decisions]

## Testing
[How to run tests; what is and isn't covered]

## Contributing
[Link to CONTRIBUTING.md or brief guide]

## Related
[Links to ADRs, runbooks, ADO items, or related repos]

---
Last updated: [date] | Owner: [team/person] | Version: [x.y]
```

**Rules:**
- No placeholders — every section is fully populated or explicitly marked "N/A"
- All commands must be cross-checked against the actual codebase
- If a step cannot be verified, flag it explicitly
- Show the draft and ask for feedback before writing the file
