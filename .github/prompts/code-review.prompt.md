---
mode: ask
description: Review code or a diff against the team's SCM checklist
---

Review the following code or diff against the team's engineering standards.

Check for:

**Correctness**
- Logic errors, off-by-one issues, unhandled edge cases

**Security**
- Secrets or credentials in code
- SQL injection, command injection, XSS (if web-facing)
- Insecure deserialization or file handling

**Code Quality**
- Function length (>40 lines is a smell)
- Naming (descriptive, consistent with codebase conventions)
- Duplication — is there an existing utility that should be reused?
- Missing type annotations (Python)

**Testing**
- Are there tests for the new code?
- Are edge cases covered?

**Documentation**
- Is the README updated if behavior changed?
- Are non-obvious decisions explained with a comment?

**ADO / SCM**
- Is there a linked ADO work item?
- Does the branch name follow `<type>/<description>` convention?
- Is the commit message descriptive?

Output: a prioritized list of findings (Critical / Major / Minor / Suggestion).
