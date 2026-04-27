---
name: pr-description
description: Generate a structured PR description from a git diff, file list, or change summary
domain: devops
requires_script: true
script: scripts/git/pr_description.py
---

## Usage

Invoke with `/pr-description` then provide one of:
- A `git diff` output (paste directly)
- A list of changed files + brief description of each change
- A plain-text summary of what the PR does

Optionally specify:
- Linked ADO work item number
- Any breaking changes

## Output

```markdown
## What
[One sentence: what change does this PR make?]

## Why
[One sentence: what problem does it solve or what value does it add?]

## How
[Brief technical summary: approach, key decisions, anything non-obvious]

## How to test
1. [Step 1]
2. [Step 2]
3. [Expected result]

## Checklist
- [ ] Tests added or updated
- [ ] Docs updated if behaviour changed
- [ ] No secrets committed
- [ ] ADO work item linked: #[number]
```

## Steps

1. If a git diff is provided, read it to understand what changed and why
2. If a diff is not available, use the provided summary
3. Write "What" as a noun phrase ("Add X", "Fix Y", "Refactor Z")
4. Write "Why" in terms of user or business value, not technical mechanics
5. Write "How" only if the approach is non-obvious — skip if the diff speaks for itself
6. Write test steps that a reviewer can follow to verify the change
7. If an ADO item number is provided, include it in the checklist

## Script (optional)

If `scripts/git/pr_description.py` is available and git is accessible, you can run:
```bash
python scripts/git/pr_description.py --diff "$(git diff main)"
```
to generate the raw diff for input.
