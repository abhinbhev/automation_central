"""Validate a skill folder against repo standards."""

import re
import sys
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

REQUIRED_FRONTMATTER = {"name", "description", "domain", "requires_script"}
VALID_DOMAINS = {"ado", "office", "devops", "data-ml", "infra", "comms", "coding", "meta"}
REQUIRED_SECTIONS = {"## Usage", "## Output", "## Steps"}
SECRET_PATTERNS = [
    r"(?i)(password|passwd|secret|token|pat|api.?key)\s*=\s*['\"][^'\"]{6,}",
]

Finding = tuple[str, str]  # (level, message)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.index("---", 3)
    fm_raw = text[3:end].strip()
    body = text[end + 3:].strip()
    return yaml.safe_load(fm_raw) or {}, body


def check_skill(skill_path: Path) -> list[Finding]:
    findings: list[Finding] = []

    if not skill_path.is_dir():
        return [("ERROR", f"Path is not a directory: {skill_path}")]

    folder_name = skill_path.name
    if folder_name != folder_name.lower() or "_" in folder_name:
        findings.append(("ERROR", f"Folder name must be kebab-case, got: {folder_name}"))

    domain = skill_path.parent.name
    if domain not in VALID_DOMAINS:
        findings.append(("ERROR", f"Parent domain '{domain}' is not a valid domain: {VALID_DOMAINS}"))

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        findings.append(("ERROR", "SKILL.md not found"))
        return findings

    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    missing_fields = REQUIRED_FRONTMATTER - set(fm.keys())
    for field in sorted(missing_fields):
        findings.append(("ERROR", f"Frontmatter missing required field: '{field}'"))

    if "name" in fm and fm["name"] != folder_name:
        findings.append(("ERROR", f"Frontmatter 'name' ({fm['name']}) does not match folder name ({folder_name})"))

    if "domain" in fm and fm["domain"] not in VALID_DOMAINS:
        findings.append(("ERROR", f"Frontmatter 'domain' '{fm['domain']}' is not a valid domain"))

    for section in REQUIRED_SECTIONS:
        if section not in text:
            findings.append(("ERROR", f"Missing required section: {section}"))

    if fm.get("requires_script") is True:
        script_path = fm.get("script", "")
        if script_path and not Path(script_path).exists():
            findings.append(("WARN", f"Script listed in frontmatter not found: {script_path}"))

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            findings.append(("ERROR", "Possible secret/credential detected in SKILL.md"))

    return findings


@app.command()
def main(skill_path: Path = typer.Argument(..., help="Path to the skill folder")) -> None:
    findings = check_skill(skill_path)

    table = Table(title=f"Validation: {skill_path}", show_header=True)
    table.add_column("Level", style="bold")
    table.add_column("Finding")

    errors = 0
    for level, msg in findings:
        style = "red" if level == "ERROR" else "yellow"
        table.add_row(f"[{style}]{level}[/{style}]", msg)
        if level == "ERROR":
            errors += 1

    if not findings:
        console.print(f"[green]✓ {skill_path.name} — all checks passed[/green]")
    else:
        console.print(table)
        console.print(f"\n[{'red' if errors else 'yellow'}]Result: {'FAIL' if errors else 'WARN'} ({errors} error(s))[/]")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    app()
