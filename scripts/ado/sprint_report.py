"""Generate a sprint status report from ADO work items.

Usage:
    python sprint_report.py --iteration "MyProject\\Sprint 42"
    python sprint_report.py --iteration "MyProject\\Sprint 42" --format markdown
    python sprint_report.py --iteration "MyProject\\Sprint 42" --format json --output report.json

Outputs a sprint summary with: total items, completed, in-progress, blocked, and
per-type and per-assignee breakdowns.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import typer
from azure.devops.exceptions import AzureDevOpsServiceError
from rich.console import Console
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.shared.auth import get_ado_connection

app = typer.Typer()
console = Console()

DONE_STATES = {"Closed", "Done", "Resolved", "Completed"}
BLOCKED_STATES = {"Blocked", "Impediment"}
ACTIVE_STATES = {"Active", "In Progress", "In Review", "Committed"}


def fetch_sprint_items(client: "WorkItemTrackingClient", project: str, iteration_path: str) -> list[dict]:
    wiql = f"""
    SELECT [System.Id], [System.Title], [System.WorkItemType],
           [System.State], [System.AssignedTo], [Microsoft.VSTS.Scheduling.StoryPoints]
    FROM WorkItems
    WHERE [System.TeamProject] = '{project}'
      AND [System.IterationPath] = '{iteration_path}'
      AND [System.WorkItemType] IN ('Epic', 'Feature', 'User Story', 'Task', 'Bug')
    ORDER BY [System.WorkItemType], [System.Id]
    """
    from azure.devops.v7_1.work_item_tracking.models import Wiql
    result = client.query_by_wiql(Wiql(query=wiql), project=project)
    if not result.work_items:
        return []

    ids = [wi.id for wi in result.work_items]
    fields = [
        "System.Id", "System.Title", "System.WorkItemType",
        "System.State", "System.AssignedTo",
        "Microsoft.VSTS.Scheduling.StoryPoints",
    ]
    work_items = client.get_work_items(ids=ids, fields=fields)
    return [
        {
            "id": wi.id,
            "title": wi.fields.get("System.Title", ""),
            "type": wi.fields.get("System.WorkItemType", ""),
            "state": wi.fields.get("System.State", ""),
            "assignee": (wi.fields.get("System.AssignedTo") or {}).get("displayName", "Unassigned"),
            "points": wi.fields.get("Microsoft.VSTS.Scheduling.StoryPoints") or 0,
        }
        for wi in work_items
    ]


def categorise(state: str) -> str:
    if state in DONE_STATES:
        return "done"
    if state in BLOCKED_STATES:
        return "blocked"
    if state in ACTIVE_STATES:
        return "active"
    return "not_started"


def build_summary(items: list[dict]) -> dict:
    summary: dict = {
        "total": len(items),
        "done": 0, "active": 0, "blocked": 0, "not_started": 0,
        "total_points": 0, "done_points": 0,
        "by_type": defaultdict(lambda: {"total": 0, "done": 0}),
        "by_assignee": defaultdict(lambda: {"total": 0, "done": 0, "points": 0}),
        "items": items,
    }
    for item in items:
        cat = categorise(item["state"])
        summary[cat] += 1
        summary["total_points"] += item["points"]
        if cat == "done":
            summary["done_points"] += item["points"]
        summary["by_type"][item["type"]]["total"] += 1
        if cat == "done":
            summary["by_type"][item["type"]]["done"] += 1
        summary["by_assignee"][item["assignee"]]["total"] += 1
        summary["by_assignee"][item["assignee"]]["points"] += item["points"]
        if cat == "done":
            summary["by_assignee"][item["assignee"]]["done"] += 1
    return summary


def render_markdown(summary: dict, iteration: str) -> str:
    s = summary
    pct = round(s["done"] / s["total"] * 100) if s["total"] else 0
    lines = [
        f"# Sprint Report — {iteration}",
        "",
        "## Summary",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total items | {s['total']} |",
        f"| Done | {s['done']} ({pct}%) |",
        f"| Active | {s['active']} |",
        f"| Blocked | {s['blocked']} |",
        f"| Not started | {s['not_started']} |",
        f"| Story points delivered | {s['done_points']} / {s['total_points']} |",
        "",
        "## By Type",
        "| Type | Done | Total |",
        "|------|------|-------|",
    ]
    for item_type, counts in sorted(s["by_type"].items()):
        lines.append(f"| {item_type} | {counts['done']} | {counts['total']} |")
    lines += [
        "",
        "## By Assignee",
        "| Assignee | Done | Total | Points |",
        "|----------|------|-------|--------|",
    ]
    for assignee, counts in sorted(s["by_assignee"].items()):
        lines.append(f"| {assignee} | {counts['done']} | {counts['total']} | {counts['points']} |")
    if s.get("blocked"):
        blocked_items = [i for i in s["items"] if categorise(i["state"]) == "blocked"]
        lines += ["", "## Blocked Items", "| ID | Title | Assignee |", "|----|-------|----------|"]
        for item in blocked_items:
            lines.append(f"| #{item['id']} | {item['title']} | {item['assignee']} |")
    return "\n".join(lines)


@app.command()
def main(
    iteration: str = typer.Option(..., help="ADO iteration path, e.g. 'MyProject\\Sprint 42'"),
    project: str = typer.Option(..., envvar="ADO_PROJECT", help="ADO project name"),
    format: str = typer.Option("markdown", help="Output format: markdown or json"),
    output: Path = typer.Option(None, help="Write output to this file instead of stdout"),
) -> None:
    """Generate a sprint status report from ADO."""
    connection = get_ado_connection()
    client = connection.clients.get_work_item_tracking_client()

    console.print(f"Fetching sprint items for '{iteration}'...")
    try:
        items = fetch_sprint_items(client, project, iteration)
    except AzureDevOpsServiceError as exc:
        console.print(f"[red]ADO API error:[/red] {exc}")
        raise typer.Exit(1)

    if not items:
        console.print("[yellow]No work items found for this iteration.[/yellow]")
        raise typer.Exit(0)

    summary = build_summary(items)

    if format == "json":
        out = json.dumps({k: v for k, v in summary.items() if k != "items"}, indent=2, default=dict)
    else:
        out = render_markdown(summary, iteration)

    if output:
        output.write_text(out)
        console.print(f"[green]✓ Report written to {output}[/green]")
    else:
        console.print(out)


if __name__ == "__main__":
    app()
