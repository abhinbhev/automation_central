---
name: code-review
description: Review a git diff or code snippet against the team's SCM checklist, output findings by severity
domain: coding
requires_script: false
---

## Usage

Invoke with `/code-review` then provide:
- A git diff (paste output of `git diff` or `git diff main...HEAD`)
- Or a code snippet to review
- Optionally: language/domain context (Python / Terraform / SQL / YAML)

## Output

A prioritised findings list:

```
## Code Review

### Critical (must fix)
- [file:line] [Issue description] → [Suggested fix]

### Major (should fix)
- ...

### Minor (fix or explain)
- ...

### Suggestions
- ...

---
Recommendation: Approve / Approve with minor changes / Request changes
```

## Review Checklist

**Critical:** secrets in code, injection vulnerabilities, logic errors causing incorrect prod behaviour, unhandled breaking changes

**Major:** missing error handling at system boundaries, functions >100 lines, missing tests for new logic, hardcoded values that should be config, missing type annotations

**Minor:** naming convention violations, magic numbers, commented-out code, TODO without ADO item

**Suggestions:** readability, alternative approaches, additional test cases

## Steps

1. Read the diff or code
2. Apply each checklist item systematically
3. For each finding: note file + line range, describe the problem, suggest a fix
4. Group by severity
5. Give overall recommendation
