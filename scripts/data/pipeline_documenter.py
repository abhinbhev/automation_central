"""Parse a data pipeline configuration and generate Markdown documentation.

Supports:
  - Airflow DAG Python files (extract task IDs, dependencies, schedule)
  - Azure Data Factory pipeline JSON exports
  - dbt project YAML (dbt_project.yml + model YAML)
  - Generic JSON/YAML pipeline spec (custom format)

Usage:
    python pipeline_documenter.py --source dag_file.py --type airflow --output pipeline_docs.md
    python pipeline_documenter.py --source pipeline.json --type adf --output pipeline_docs.md
    python pipeline_documenter.py --source dbt_project.yml --type dbt --output pipeline_docs.md
    python pipeline_documenter.py --source spec.json --type generic --output pipeline_docs.md
"""

import json
import re
from datetime import date
from pathlib import Path

import typer
import yaml
from rich.console import Console

app = typer.Typer()
console = Console()


def parse_airflow_dag(source_path: Path) -> dict:
    """Extract DAG metadata and task graph from an Airflow Python file."""
    source = source_path.read_text()
    schedule_match = re.search(r"schedule(?:_interval)?\s*=\s*['\"]([^'\"]+)['\"]", source)
    dag_id_match = re.search(r"dag_id\s*=\s*['\"]([^'\"]+)['\"]", source)
    task_ids = re.findall(r"task_id\s*=\s*['\"]([^'\"]+)['\"]", source)
    dependencies = re.findall(r"(\w+)\s*>>\s*(\w+)", source)

    return {
        "name": dag_id_match.group(1) if dag_id_match else source_path.stem,
        "schedule": schedule_match.group(1) if schedule_match else "[TBD]",
        "tasks": [{"id": t} for t in task_ids],
        "dependencies": [{"from": d[0], "to": d[1]} for d in dependencies],
        "source_type": "airflow",
    }


def parse_adf_pipeline(source_path: Path) -> dict:
    """Extract pipeline metadata from an Azure Data Factory pipeline JSON export."""
    data = json.loads(source_path.read_text())
    name = data.get("name", source_path.stem)
    properties = data.get("properties", {})
    activities = properties.get("activities", [])

    tasks = []
    for act in activities:
        tasks.append({
            "id": act.get("name", "unknown"),
            "type": act.get("type", ""),
            "linked_service": (act.get("linkedServiceName") or {}).get("referenceName", ""),
        })

    dependencies = []
    for act in activities:
        for dep in act.get("dependsOn", []):
            dependencies.append({"from": dep.get("activity"), "to": act.get("name")})

    return {
        "name": name,
        "schedule": properties.get("folder", {}).get("name", "[see ADF triggers]"),
        "tasks": tasks,
        "dependencies": dependencies,
        "source_type": "adf",
    }


def parse_dbt_project(source_path: Path) -> dict:
    """Extract model list and dependencies from a dbt project YAML."""
    data = yaml.safe_load(source_path.read_text())
    name = data.get("name", source_path.stem)
    models = data.get("models", {})
    model_names = list(models.keys()) if isinstance(models, dict) else []

    return {
        "name": name,
        "schedule": "[see Airflow/ADF orchestrator]",
        "tasks": [{"id": m} for m in model_names],
        "dependencies": [],
        "source_type": "dbt",
    }


def parse_generic(source_path: Path) -> dict:
    """Parse a generic JSON or YAML pipeline spec."""
    text = source_path.read_text()
    if source_path.suffix in (".yaml", ".yml"):
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)

    return {
        "name": data.get("name", source_path.stem),
        "schedule": data.get("schedule", "[TBD]"),
        "tasks": data.get("tasks", []),
        "dependencies": data.get("dependencies", []),
        "inputs": data.get("inputs", []),
        "outputs": data.get("outputs", []),
        "source_type": "generic",
    }


def render_mermaid_flow(tasks: list[dict], dependencies: list[dict]) -> str:
    lines = ["```mermaid", "flowchart LR"]
    for task in tasks:
        label = task.get("type", task["id"])
        lines.append(f'  {task["id"]}["{label}"]')
    for dep in dependencies:
        if dep.get("from") and dep.get("to"):
            lines.append(f'  {dep["from"]} --> {dep["to"]}')
    lines.append("```")
    return "\n".join(lines)


def render_markdown(pipeline: dict) -> str:
    lines = [
        f"# Pipeline: {pipeline['name']}",
        f"**Owner:** [TBD]",
        f"**Last updated:** {date.today()}",
        f"**Schedule:** {pipeline.get('schedule', '[TBD]')}",
        f"**Source type:** {pipeline.get('source_type', 'unknown')}",
        "",
        "---",
        "",
        "## Overview",
        "[Add a 2-3 sentence description of what this pipeline does and who depends on it.]",
        "",
        "## Data Flow",
        "",
        render_mermaid_flow(pipeline.get("tasks", []), pipeline.get("dependencies", [])),
        "",
    ]

    inputs = pipeline.get("inputs", [])
    if inputs:
        lines += ["## Inputs", "", "| Source | Type | Description |", "|--------|------|-------------|"]
        for inp in inputs:
            if isinstance(inp, dict):
                lines.append(f"| {inp.get('name','')} | {inp.get('type','')} | {inp.get('description','')} |")
            else:
                lines.append(f"| {inp} | | |")
        lines.append("")

    outputs = pipeline.get("outputs", [])
    if outputs:
        lines += ["## Outputs", "", "| Destination | Description |", "|-------------|-------------|"]
        for out in outputs:
            if isinstance(out, dict):
                lines.append(f"| {out.get('name','')} | {out.get('description','')} |")
            else:
                lines.append(f"| {out} | |")
        lines.append("")

    tasks = pipeline.get("tasks", [])
    if tasks:
        lines += ["## Tasks / Activities", "", "| Task | Type | Notes |", "|------|------|-------|"]
        for task in tasks:
            lines.append(
                f"| {task.get('id','')} | {task.get('type','')} | {task.get('linked_service','')} |"
            )
        lines.append("")

    lines += [
        "## Failure Handling",
        "[Document retry behaviour, alerting, and on-failure actions here.]",
        "",
        "## Post-Incident",
        "On failure → use `/incident-runbook` skill to generate a runbook.",
    ]

    return "\n".join(lines)


@app.command()
def main(
    source: Path = typer.Argument(..., help="Path to pipeline config file"),
    type: str = typer.Option("generic", help="Pipeline type: airflow, adf, dbt, generic"),
    output: Path = typer.Option(..., help="Output Markdown file path"),
) -> None:
    """Document a data pipeline from its config file."""
    if not source.exists():
        console.print(f"[red]Source file not found:[/red] {source}")
        raise typer.Exit(1)

    parsers = {
        "airflow": parse_airflow_dag,
        "adf": parse_adf_pipeline,
        "dbt": parse_dbt_project,
        "generic": parse_generic,
    }
    parser = parsers.get(type, parse_generic)
    console.print(f"Parsing {type} pipeline from {source.name}...")
    pipeline = parser(source)

    docs = render_markdown(pipeline)
    output.write_text(docs)
    console.print(f"[green]✓ Pipeline docs written to {output}[/green]")


if __name__ == "__main__":
    app()
