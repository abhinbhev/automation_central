"""Create ADO work items (Epic / Feature / User Story / Task / Bug) from a JSON spec.

Usage:
    python create_work_items.py --spec work_items.json
    python create_work_items.py --spec work_items.json --dry-run

The spec JSON should be an array of work item objects. Example:
[
  {
    "type": "User Story",
    "title": "As a data engineer, I want automated schema validation",
    "description": "Schema mismatches should surface errors at ingestion time.",
    "acceptance_criteria": "1. Errors appear within 5s\\n2. Error includes field name and expected type",
    "priority": 2,
    "area_path": "MyProject\\\\TeamA",
    "iteration_path": "MyProject\\\\Sprint 42",
    "parent_id": 1001
  }
]
"""

import json
import sys
from pathlib import Path

import typer
from azure.devops.exceptions import AzureDevOpsServiceError
from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation
from rich.console import Console
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.shared.auth import get_ado_connection

app = typer.Typer()
console = Console()

FIELD_MAP = {
    "title": "System.Title",
    "description": "System.Description",
    "acceptance_criteria": "Microsoft.VSTS.Common.AcceptanceCriteria",
    "priority": "Microsoft.VSTS.Common.Priority",
    "area_path": "System.AreaPath",
    "iteration_path": "System.IterationPath",
}


def build_patch_document(item: dict) -> list[JsonPatchOperation]:
    ops = []
    for field_key, ado_field in FIELD_MAP.items():
        value = item.get(field_key)
        if value is not None:
            ops.append(
                JsonPatchOperation(
                    op="add",
                    path=f"/fields/{ado_field}",
                    value=str(value) if not isinstance(value, int) else value,
                )
            )
    if parent_id := item.get("parent_id"):
        ops.append(
            JsonPatchOperation(
                op="add",
                path="/relations/-",
                value={
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": f"{_get_org_url()}/_apis/wit/workItems/{parent_id}",
                },
            )
        )
    return ops


def _get_org_url() -> str:
    import os
    return os.environ["ADO_ORG_URL"].rstrip("/")


def create_item(client: "WorkItemTrackingClient", project: str, item: dict, dry_run: bool) -> dict | None:
    item_type = item.get("type", "Task")
    title = item.get("title", "Untitled")

    if dry_run:
        console.print(f"  [dim][DRY RUN][/dim] Would create {item_type}: {title}")
        return None

    try:
        patch_doc = build_patch_document(item)
        result = client.create_work_item(
            document=patch_doc,
            project=project,
            type=item_type,
        )
        return {"id": result.id, "type": item_type, "title": title, "url": result.url}
    except AzureDevOpsServiceError as exc:
        console.print(f"  [red]✗ Failed to create '{title}':[/red] {exc}")
        return None


@app.command()
def main(
    spec: Path = typer.Option(..., help="Path to JSON spec file"),
    project: str = typer.Option(..., envvar="ADO_PROJECT", help="ADO project name"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print what would be created without calling ADO"),
) -> None:
    """Create ADO work items from a JSON spec file."""
    if not spec.exists():
        console.print(f"[red]Spec file not found:[/red] {spec}")
        raise typer.Exit(1)

    items = json.loads(spec.read_text())
    if not isinstance(items, list):
        console.print("[red]Spec file must be a JSON array.[/red]")
        raise typer.Exit(1)

    connection = get_ado_connection()
    client = connection.clients.get_work_item_tracking_client()

    results = []
    console.print(f"\nCreating {len(items)} work item(s) in project '{project}'...\n")

    for item in items:
        result = create_item(client, project, item, dry_run)
        if result:
            results.append(result)

    if results:
        table = Table(title="Created Work Items")
        table.add_column("ID", style="cyan")
        table.add_column("Type")
        table.add_column("Title")
        for r in results:
            table.add_row(str(r["id"]), r["type"], r["title"])
        console.print(table)
        console.print(f"\n[green]✓ Created {len(results)} / {len(items)} items.[/green]")
    elif dry_run:
        console.print(f"\n[yellow]Dry run complete — {len(items)} items would be created.[/yellow]")


if __name__ == "__main__":
    app()
