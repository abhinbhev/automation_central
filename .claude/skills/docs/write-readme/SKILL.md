---
name: write-readme
description: Generate a complete README for a project, module, or script from the codebase or a description
domain: docs
requires_script: false
---

## Usage

Invoke with `/write-readme` then provide one of:
- A path to read (e.g. `scripts/ado/`) — the agent will explore the code and generate the README
- A description of the project/module if no code exists yet
- An existing README to rewrite or expand

Optionally specify:
- **Audience:** engineers (default) | ops | external consumers | new joiners
- **Level:** project-level (full README) | module-level (shorter, focused on API/usage)

## Output

A complete `README.md` with:

```markdown
# [Project / Module Name]

> [One-line description — what it does and for whom]

## Overview
[2–3 sentences: problem it solves, how it fits in the broader system]

## Prerequisites
[Runtime versions, env vars, dependencies]

## Installation / Setup
[Step-by-step commands — tested, copy-pasteable]

## Usage
[CLI examples, function call examples, or API examples with real values]

## Configuration
[All env vars and config options in a table: name | required | default | description]

## Project Structure
[File tree with one-line description of each file/folder]

## How it works
[Brief technical explanation — architecture, data flow, key decisions]

## Testing
[How to run tests; what is and isn't covered]

## Contributing
[Link to CONTRIBUTING.md or brief contribution guide]

## Related
[Links to ADRs, runbooks, ADO items, or related repos]

---
Last updated: [date] | Owner: [team/person] | Version: [x.y]
```

## Steps

1. Read all files in the target path (or the provided description)
2. Identify: purpose, entry points, config, dependencies, usage patterns
3. Draft the full README — populate every section, no placeholders
4. If commands or steps are included, cross-check them against the actual code
5. Show the draft and ask for feedback
6. Write to the correct path on approval
