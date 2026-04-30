---
name: pr-description
description: "Generate a structured PR description from a git diff or summary"
mode: ask
---

Write a pull request description based on the provided diff or change summary.

Use this structure:

## What
<!-- One sentence: what change does this PR make? -->

## Why
<!-- One sentence: what problem does it solve or what value does it add? -->

## How
<!-- Brief technical summary: approach taken, key decisions -->

## How to test
<!-- Numbered steps to verify the change works -->

## Checklist
- [ ] Tests added or updated
- [ ] Docs updated if needed
- [ ] No secrets committed
- [ ] ADO work item linked

Keep it concise — reviewers should understand the change in under 2 minutes of reading.
