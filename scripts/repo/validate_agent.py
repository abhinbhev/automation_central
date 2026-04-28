"""Validate an .agent.md file against repo standards."""

import re
import sys
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

# Claude agents require both; Copilot agents only need description
CLAUDE_REQUIRED_FRONTMATTER = {"name", "description"}
COPILOT_REQUIRED_FRONTMATTER = {"description"}
SECRET_PATTERNS = [
    r"(?i)(password|passwd|secret|token|pat|api.?key)\s*=\s*['\"][^'\"]{6,}",
]


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.index("---", 3)
    fm_raw = text[3:end].strip()
    body = text[end + 3:].strip()
    return yaml.safe_load(fm_raw) or {}, body


def check_agent(agent_path: Path) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []

    if not agent_path.is_file():
        return [("ERROR", f"File not found: {agent_path}")]

    if not agent_path.name.endswith(".agent.md"):
        findings.append(("ERROR", "File must have .agent.md extension"))

    stem = agent_path.stem.replace(".agent", "")
    if stem != stem.lower() or "_" in stem:
        findings.append(("ERROR", f"Agent filename stem must be kebab-case, got: {stem}"))

    text = agent_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    # Determine if this is a Copilot (.github/) or Claude (.claude/) agent
    is_copilot = ".github" in agent_path.parts
    required = COPILOT_REQUIRED_FRONTMATTER if is_copilot else CLAUDE_REQUIRED_FRONTMATTER

    missing_fields = required - set(fm.keys())
    for field in sorted(missing_fields):
        findings.append(("ERROR", f"Frontmatter missing required field: '{field}'"))

    if "name" in fm:
        expected_name = stem
        if fm["name"] != expected_name:
            findings.append(("WARN", f"Frontmatter 'name' ({fm['name']}) doesn't match filename stem ({expected_name})"))

    if len(body.strip()) < 50:
        findings.append(("WARN", "Agent body is very short — consider adding capabilities and boundaries"))

    if not is_copilot and "skills" in fm:
        skills = fm["skills"]
        if not isinstance(skills, list):
            findings.append(("ERROR", "Frontmatter 'skills' must be a list of domain/skill-name strings"))
        else:
            repo_root = agent_path
            for _ in range(10):  # walk up to find repo root (.claude dir)
                repo_root = repo_root.parent
                if (repo_root / ".claude" / "skills").is_dir():
                    break
            for entry in skills:
                if not isinstance(entry, str) or "/" not in entry:
                    findings.append(("WARN", f"Skill entry '{entry}' should be in 'domain/skill-name' format"))
                    continue
                skill_path = repo_root / ".claude" / "skills" / entry.replace("/", "/") / "SKILL.md"
                # normalise for OS
                skill_path = repo_root / ".claude" / "skills" / Path(entry) / "SKILL.md"
                if not skill_path.is_file():
                    findings.append(("ERROR", f"Skill '{entry}' has no SKILL.md at {skill_path.relative_to(repo_root)}"))
    elif not is_copilot and "skills" not in fm:
        findings.append(("WARN", "Claude agent has no 'skills:' frontmatter — add relevant skills or set skills: [] if none apply"))

    if not is_copilot and "## Relevant Skills" not in body:
        findings.append(("WARN", "Claude agent body is missing '## Relevant Skills' section"))

    if is_copilot and "## Relevant Skills" not in body:
        findings.append(("WARN", "Copilot agent body is missing '## Relevant Skills' section"))

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            findings.append(("ERROR", "Possible secret/credential detected in agent file"))

    return findings


@app.command()
def main(agent_path: Path = typer.Argument(..., help="Path to the .agent.md file")) -> None:
    findings = check_agent(agent_path)

    errors = sum(1 for level, _ in findings if level == "ERROR")

    if not findings:
        console.print(f"[green]✓ {agent_path.name} — all checks passed[/green]")
    else:
        table = Table(title=f"Validation: {agent_path.name}", show_header=True)
        table.add_column("Level", style="bold")
        table.add_column("Finding")
        for level, msg in findings:
            style = "red" if level == "ERROR" else "yellow"
            table.add_row(f"[{style}]{level}[/{style}]", msg)
        console.print(table)
        console.print(f"\n[{'red' if errors else 'yellow'}]Result: {'FAIL' if errors else 'WARN'} ({errors} error(s))[/]")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    app()
