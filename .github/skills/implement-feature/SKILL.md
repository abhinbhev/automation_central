---
name: implement-feature
description: "Implement a feature or script following team standards (Python 3.11+, typed, tested)"
mode: agent
---

Implement the following feature or script using team standards.

Before writing any code:
1. Search the codebase for existing utilities, helpers, or patterns that should be reused
2. Identify integration points (config files, shared modules, entry points)
3. Ask only if inputs/outputs are genuinely ambiguous

Implementation checklist:
- Python 3.11+ with full type annotations on all function signatures
- `typer` for CLI entry points, `rich` for console output
- `httpx` for HTTP calls, `pathlib.Path` for file paths
- `python-dotenv` for secrets — never hardcode credentials
- Functions under 40 lines; extract helpers rather than nesting logic
- `main()` function + `if __name__ == "__main__": main()` (or `app()` with typer)
- snake_case names, descriptive variable names, no commented-out code

After implementation:
- Write pytest tests covering happy paths, edge cases, and error conditions
- Name tests `test_<what>_when_<condition>_then_<expected>`
- Mock external dependencies (network, filesystem, DB) with `pytest-mock`

Summarise:
- Files created/modified with paths
- How to run the script or invoke the CLI
- What the `code-reviewer` agent should focus on
