---
name: commit-message
description: Generate a conventional commit message from staged changes, a diff, or a description of what changed
domain: devops
requires_script: false
---

## Usage

Invoke with `/commit-message` then provide one of:
- Output of `git diff --staged` (preferred — staged changes only)
- Output of `git diff HEAD` (all uncommitted changes)
- A plain-English description of what changed and why

Optionally specify:
- Linked ADO work item number (e.g. `AB#1234`)
- Whether this is a breaking change
- Scope (e.g. `auth`, `pipeline`, `scripts/ado`)

## Commit Format

Follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

[body — what and why, not how; omit if summary is self-explanatory]

[footer — BREAKING CHANGE: ... and/or AB#ID]
```

### Types

| Type | When to use |
|------|------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code restructure with no behaviour change |
| `test` | Adding or updating tests |
| `chore` | Tooling, deps, config — no production code change |
| `ci` | CI/CD pipeline changes |
| `perf` | Performance improvement |
| `revert` | Reverts a previous commit |

### Rules

- Summary line: imperative mood, lowercase, no trailing period, max 72 chars
  - ✅ `add bulk work item creation from JSON spec`
  - ❌ `Added bulk work item creation` / `Adds bulk work item creation.`
- Body explains *what* changed and *why* — the diff shows *how*
- `BREAKING CHANGE:` footer required if existing behaviour is altered in a non-backwards-compatible way
- `AB#ID` in footer links the commit to an ADO work item (renders as hyperlink in ADO)

## Output

```
feat(scripts/ado): add bulk work item creation from JSON spec

Supports creating multiple items in a single call by accepting a JSON
array. Avoids N individual API calls when seeding a sprint backlog.

AB#1042
```

Or for a simple fix:

```
fix(office): prevent ppt_builder crash on empty outline sections
```

## Steps

1. Read the diff or description — understand what files changed, what behaviour changed, and why
2. Choose the correct `type` — when unsure between `feat` and `chore`, ask: would a user notice this change?
3. Set `scope` to the most specific folder or module affected; omit if change spans the whole repo
4. Write the summary line: imperative, lowercase, under 72 chars
5. Add a body only if the summary doesn't fully explain the *why*
6. Add footer lines: `BREAKING CHANGE:` if applicable, `AB#ID` if an ADO item is linked
7. Output the final commit message in a code block, ready to copy-paste into `git commit -m`

## Also flag (do not silently ignore)

- Unrelated changes that should be split into separate commits
- Unstaged changes that look like they belong with the staged ones
- A breaking change that wasn't mentioned by the user
