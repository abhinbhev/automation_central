---
applyTo: "**/*.py"
---

# Python Standards

- Python 3.11+
- Use `typer` for CLI entry points, not `argparse`
- Use `rich` for console output (progress bars, tables, colored text)
- Use `python-dotenv` to load `.env` files — never hardcode secrets
- Type-annotate all function signatures
- Use `pathlib.Path` not `os.path`
- Prefer `httpx` over `requests` for HTTP calls
- Structure scripts with a `main()` function and `if __name__ == "__main__": main()` — or `app()` when using `typer`
- Keep functions under 40 lines; extract helpers rather than nesting logic
- Use `pyyaml` for YAML, `openpyxl` for Excel, `jinja2` for HTML presentations, `python-docx` for Word
