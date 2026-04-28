"""Generate release notes from closed ADO work items in a sprint or date range.

Usage:
    python release_notes.py --iteration "MyProject\\Sprint 42"
    python release_notes.py --iteration "MyProject\\Sprint 42" --audience stakeholder
    python release_notes.py --since 2025-05-01 --until 2025-05-23 --version v2.4.0

Outputs Markdown release notes in either stakeholder or internal (engineering) format.
"""

import sys
from datetime import date
from pathlib import Path

import typer
from azure.devops.exceptions import AzureDevOpsServiceError
from azure.devops.v7_1.work_item_tracking.models import Wiql
from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.shared.auth import get_ado_connection

app = typer.Typer()
console = Console()

CLOSED_STATES = {"Closed", "Done", "Resolved", "Completed"}
STORY_TYPES = {"User Story", "Feature"}
BUG_TYPES = {"Bug"}
TASK_TYPES = {"Task"}


def fetch_closed_items(client: "WorkItemTrackingClient", project: str, iteration: str | None, since: str | None, until: str | None) -> list[dict]:
    conditions = [
        f"[System.TeamProject] = '{project}'",
        f"[System.State] IN ('Closed', 'Done', 'Resolved', 'Completed')",
        "[System.WorkItemType] IN ('Epic', 'Feature', 'User Story', 'Task', 'Bug')",
    ]
    if iteration:
        conditions.append(f"[System.IterationPath] = '{iteration}'")
    if since:
        conditions.append(f"[Microsoft.VSTS.Common.ClosedDate] >= '{since}'")
    if until:
        conditions.append(f"[Microsoft.VSTS.Common.ClosedDate] <= '{until}'")

    wiql = f"""
    SELECT [System.Id], [System.Title], [System.WorkItemType], [System.State],
           [Microsoft.VSTS.Scheduling.StoryPoints], [Microsoft.VSTS.Common.ClosedDate]
    FROM WorkItems
    WHERE {' AND '.join(conditions)}
    ORDER BY [System.WorkItemType], [System.Id]
    """
    result = client.query_by_wiql(Wiql(query=wiql), project=project)
    if not result.work_items:
        return []

    ids = [wi.id for wi in result.work_items]
    fields = [
        "System.Id", "System.Title", "System.WorkItemType", "System.State",
        "Microsoft.VSTS.Scheduling.StoryPoints",
        "Microsoft.VSTS.Common.ClosedDate",
    ]
    work_items = client.get_work_items(ids=ids, fields=fields)
    return [
        {
            "id": wi.id,
            "title": wi.fields.get("System.Title", ""),
            "type": wi.fields.get("System.WorkItemType", ""),
            "state": wi.fields.get("System.State", ""),
            "points": wi.fields.get("Microsoft.VSTS.Scheduling.StoryPoints") or 0,
            "closed_date": (wi.fields.get("Microsoft.VSTS.Common.ClosedDate") or "")[:10],
        }
        for wi in work_items
    ]


def render_stakeholder(items: list[dict], title: str, version: str | None) -> str:
    features = [i for i in items if i["type"] in STORY_TYPES]
    bugs = [i for i in items if i["type"] in BUG_TYPES]
    ver_line = f" / {version}" if version else ""
    lines = [f"# Release Notes — {title}{ver_line}", f"**Released:** {date.today()}", ""]

    if features:
        lines += ["## What's New", ""]
        for item in features:
            lines.append(f"- **{item['title']}**")
        lines.append("")

    if bugs:
        lines += ["## Bug Fixes", ""]
        for item in bugs:
            lines.append(f"- {item['title']}")
        lines.append("")

    return "\n".join(lines)


def render_internal(items: list[dict], title: str, version: str | None) -> str:
    features = [i for i in items if i["type"] in STORY_TYPES]
    bugs = [i for i in items if i["type"] in BUG_TYPES]
    tasks = [i for i in items if i["type"] in TASK_TYPES]
    total_points = sum(i["points"] for i in items)
    ver_line = f" / {version}" if version else ""

    lines = [
        f"# Release Notes — {title}{ver_line}",
        f"**Items closed:** {len(items)}  |  **Story points delivered:** {total_points}",
        "",
    ]

    def item_table(section_title: str, section_items: list[dict]) -> list[str]:
        if not section_items:
            return []
        rows = [f"## {section_title}", "", "| ID | Title | Points |", "|----|-------|--------|"]
        for i in section_items:
            rows.append(f"| #{i['id']} | {i['title']} | {i['points']} |")
        rows.append("")
        return rows

    lines += item_table("Features & Stories", features)
    lines += item_table("Bugs Fixed", bugs)
    lines += item_table("Technical Tasks", tasks)
    return "\n".join(lines)


@app.command()
def main(
    project: str = typer.Option(..., envvar="ADO_PROJECT", help="ADO project name"),
    iteration: str = typer.Option(None, help="ADO iteration path"),
    since: str = typer.Option(None, help="Closed date from (YYYY-MM-DD)"),
    until: str = typer.Option(None, help="Closed date to (YYYY-MM-DD)"),
    version: str = typer.Option(None, help="Release version label, e.g. v2.4.0"),
    audience: str = typer.Option("internal", help="Output format: internal or stakeholder"),
    output: Path = typer.Option(None, help="Write output to this file"),
) -> None:
    """Generate release notes from closed ADO work items."""
    if not iteration and not (since or until):
        console.print("[red]Provide either --iteration or --since / --until.[/red]")
        raise typer.Exit(1)

    connection = get_ado_connection()
    client = connection.clients.get_work_item_tracking_client()

    title = iteration or f"{since} to {until}"
    console.print(f"Fetching closed items for '{title}'...")
    try:
        items = fetch_closed_items(client, project, iteration, since, until)
    except AzureDevOpsServiceError as exc:
        console.print(f"[red]ADO API error:[/red] {exc}")
        raise typer.Exit(1)

    if not items:
        console.print("[yellow]No closed items found.[/yellow]")
        raise typer.Exit(0)

    if audience == "stakeholder":
        notes = render_stakeholder(items, title, version)
    else:
        notes = render_internal(items, title, version)

    if output:
        output.write_text(notes)
        console.print(f"[green]✓ Release notes written to {output}[/green]")
    else:
        console.print(notes)


if __name__ == "__main__":
    app()
