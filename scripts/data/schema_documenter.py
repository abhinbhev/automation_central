"""Introspect a database or parse SQL DDL to generate schema documentation in Markdown.

Usage:
    # From DDL file
    python schema_documenter.py --ddl schema.sql --output schema_docs.md

    # From a live database (SQLAlchemy connection string)
    python schema_documenter.py --connection "mssql+pyodbc://user:pass@server/db?driver=ODBC+Driver+18+for+SQL+Server" --output schema_docs.md

    # Filter to specific tables
    python schema_documenter.py --ddl schema.sql --tables orders,customers --output schema_docs.md

Outputs a Markdown document with table definitions, column descriptions, and a Mermaid ER diagram.
Connection strings should be passed via environment variable SCHEMA_DB_URL, not on the command line.
"""

import re
import sys
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


def parse_ddl(ddl_text: str) -> list[dict]:
    """Parse CREATE TABLE statements from DDL into a list of table dicts."""
    tables = []
    create_pattern = re.compile(
        r"CREATE\s+TABLE\s+(?:\[?(\w+)\]?\.)?\[?(\w+)\]?\s*\((.+?)\);",
        re.IGNORECASE | re.DOTALL,
    )
    col_pattern = re.compile(
        r"^\s*\[?(\w+)\]?\s+([\w\(\), ]+?)(\s+NOT NULL|\s+NULL)?(\s+PRIMARY KEY)?(\s+IDENTITY[^,]*)?(?:\s*,|$)",
        re.IGNORECASE | re.MULTILINE,
    )

    for match in create_pattern.finditer(ddl_text):
        schema_name = match.group(1) or "dbo"
        table_name = match.group(2)
        columns_block = match.group(3)
        columns = []
        for col_match in col_pattern.finditer(columns_block):
            col_name = col_match.group(1)
            col_type = col_match.group(2).strip().rstrip(",")
            nullable = "No" if col_match.group(3) and "NOT NULL" in col_match.group(3).upper() else "Yes"
            is_pk = bool(col_match.group(4))
            if col_name.upper() in ("PRIMARY", "UNIQUE", "FOREIGN", "INDEX", "KEY", "CONSTRAINT"):
                continue
            columns.append({
                "name": col_name,
                "type": col_type,
                "nullable": nullable,
                "primary_key": is_pk,
            })
        if columns:
            tables.append({"schema": schema_name, "name": table_name, "columns": columns})
    return tables


def introspect_db(connection_url: str, table_filter: list[str] | None) -> list[dict]:
    """Introspect a live database using SQLAlchemy reflection."""
    try:
        from sqlalchemy import create_engine, inspect, text
    except ImportError:
        console.print("[red]sqlalchemy is not installed. Run: pip install sqlalchemy[/red]")
        raise typer.Exit(1)

    engine = create_engine(connection_url)
    inspector = inspect(engine)
    tables = []
    all_tables = inspector.get_table_names()
    selected = [t for t in all_tables if not table_filter or t in table_filter]

    for table_name in selected:
        columns = []
        pk_cols = set(inspector.get_pk_constraint(table_name).get("constrained_columns", []))
        for col in inspector.get_columns(table_name):
            columns.append({
                "name": col["name"],
                "type": str(col["type"]),
                "nullable": "Yes" if col.get("nullable", True) else "No",
                "primary_key": col["name"] in pk_cols,
            })
        tables.append({"schema": "dbo", "name": table_name, "columns": columns})

    return tables


def render_mermaid_er(tables: list[dict]) -> str:
    lines = ["```mermaid", "erDiagram"]
    for table in tables:
        lines.append(f"  {table['name'].upper()} {{")
        for col in table["columns"]:
            pk_marker = " PK" if col["primary_key"] else ""
            col_type = col["type"].split("(")[0].upper()
            lines.append(f"    {col_type} {col['name']}{pk_marker}")
        lines.append("  }")
    lines.append("```")
    return "\n".join(lines)


def render_markdown(tables: list[dict]) -> str:
    from datetime import date
    lines = [
        "# Schema Documentation",
        f"**Generated:** {date.today()}",
        "",
        "## Tables",
        "",
    ]
    for table in tables:
        lines += [
            f"### `{table['name']}`",
            "",
            "| Column | Type | Nullable | Notes |",
            "|--------|------|----------|-------|",
        ]
        for col in table["columns"]:
            pk_note = "Primary key" if col["primary_key"] else ""
            lines.append(f"| `{col['name']}` | `{col['type']}` | {col['nullable']} | {pk_note} |")
        lines.append("")

    lines += ["## Entity Relationship Diagram", "", render_mermaid_er(tables)]
    return "\n".join(lines)


@app.command()
def main(
    ddl: Path = typer.Option(None, help="Path to SQL DDL file"),
    connection: str = typer.Option(None, envvar="SCHEMA_DB_URL", help="SQLAlchemy connection string (prefer env var SCHEMA_DB_URL)"),
    tables: str = typer.Option(None, help="Comma-separated list of table names to document"),
    output: Path = typer.Option(..., help="Output Markdown file path"),
) -> None:
    """Generate schema documentation from DDL or a live database."""
    if not ddl and not connection:
        console.print("[red]Provide either --ddl or --connection (or set SCHEMA_DB_URL).[/red]")
        raise typer.Exit(1)

    table_filter = [t.strip() for t in tables.split(",")] if tables else None

    if ddl:
        console.print(f"Parsing DDL from {ddl}...")
        table_list = parse_ddl(ddl.read_text())
        if table_filter:
            table_list = [t for t in table_list if t["name"] in table_filter]
    else:
        console.print("Introspecting live database...")
        table_list = introspect_db(connection, table_filter)

    if not table_list:
        console.print("[yellow]No tables found.[/yellow]")
        raise typer.Exit(0)

    console.print(f"Documenting {len(table_list)} table(s)...")
    docs = render_markdown(table_list)
    output.write_text(docs)
    console.print(f"[green]✓ Schema docs written to {output}[/green]")


if __name__ == "__main__":
    app()
