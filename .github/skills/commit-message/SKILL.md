---
name: commit-message
description: "Generate a conventional commit message from staged changes, a diff, or a description of what changed"
mode: ask
---

Generate a commit message for the following change.

**Provide one of:**
- Output of `git diff --staged` (preferred — staged changes only)
- Output of `git diff HEAD` (all uncommitted changes)
- A plain-English description of what changed and why

**Optionally specify:**
- Linked ADO work item: `AB#<ID>`
- Whether this is a breaking change
- Scope (module, folder, or feature area — e.g. `auth`, `scripts/ado`)

---

## Format — Conventional Commits

```
<type>(<scope>): <short summary>

[body — what and why, not how; omit if summary is self-explanatory]

[footer — BREAKING CHANGE: ... and/or AB#ID]
```

**Types:**

| Type | Use when |
|------|---------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Restructure with no behaviour change |
| `test` | Adding or updating tests |
| `chore` | Tooling, deps, config — no production code |
| `ci` | CI/CD pipeline changes |
| `perf` | Performance improvement |
| `revert` | Reverts a previous commit |

**Rules:**
- Summary line: imperative mood, lowercase, no trailing period, max 72 chars
  - ✅ `add bulk work item creation from JSON spec`
  - ❌ `Added bulk work item creation` / `Adds bulk work item creation.`
- Body explains *what* changed and *why* — the diff shows *how*
- `BREAKING CHANGE:` footer required if existing behaviour is altered
- `AB#ID` in footer links the commit to an ADO work item

---

## Output

Produce the commit message in a code block, ready to copy-paste:

```
feat(scripts/ado): add bulk work item creation from JSON spec

Supports creating multiple items in a single call by accepting a JSON
array. Avoids N individual API calls when seeding a sprint backlog.

AB#1042
```

**Also flag (do not silently ignore):**
- If the diff contains unrelated changes that should be separate commits
- If there are unstaged changes that look like they belong with the staged ones
- If a breaking change is present but wasn't mentioned
