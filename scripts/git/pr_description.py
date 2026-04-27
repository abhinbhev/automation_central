"""Generate a structured PR description from a git diff."""

import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


def get_diff(base_branch: str = "main") -> str:
    result = subprocess.run(
        ["git", "diff", f"{base_branch}...HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def get_commit_messages(base_branch: str = "main") -> str:
    result = subprocess.run(
        ["git", "log", f"{base_branch}...HEAD", "--oneline"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


@app.command()
def main(
    base: str = typer.Option("main", help="Base branch to diff against"),
    diff: str = typer.Option(None, help="Raw diff text (if not reading from git)"),
    ado_item: str = typer.Option(None, help="ADO work item number to link"),
    output: Path = typer.Option(None, help="Write output to file instead of stdout"),
) -> None:
    diff_text = diff or get_diff(base)
    commits = get_commit_messages(base)

    if not diff_text.strip():
        console.print("[yellow]No diff found between HEAD and base branch.[/yellow]")
        sys.exit(0)

    ado_line = f"- [ ] ADO work item linked: #{ado_item}" if ado_item else "- [ ] ADO work item linked: #[number]"

    # Print a structured template for the AI to fill in, plus the raw diff
    template = f"""## What
[One sentence: what change does this PR make?]

## Why
[One sentence: what problem does it solve or what value does it add?]

## How
[Brief technical summary — approach, key decisions, anything non-obvious]

## How to test
1. [Step]
2. [Step]
3. Expected result: [...]

## Checklist
- [ ] Tests added or updated
- [ ] Docs updated if behaviour changed
- [ ] No secrets committed
{ado_line}

---
<!-- Context for the AI: commits and diff below -->
Commits:
{commits}

Diff:
{diff_text[:8000]}{'...[truncated]' if len(diff_text) > 8000 else ''}
"""

    if output:
        output.write_text(template, encoding="utf-8")
        console.print(f"[green]Written to {output}[/green]")
    else:
        print(template)


if __name__ == "__main__":
    app()
