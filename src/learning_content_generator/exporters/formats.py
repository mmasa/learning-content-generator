"""Render report tables as Markdown, JSON, or CSV."""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass

Cell = str | int | float | None


@dataclass
class Table:
    title: str
    columns: list[str]
    rows: list[list[Cell]]


def _cell_text(value: Cell) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def to_markdown(tables: list[Table]) -> str:
    parts: list[str] = []
    for table in tables:
        lines = [f"## {table.title}", ""]
        lines.append("| " + " | ".join(table.columns) + " |")
        lines.append("| " + " | ".join("---" for _ in table.columns) + " |")
        if table.rows:
            lines.extend("| " + " | ".join(_cell_text(c) for c in row) + " |" for row in table.rows)
        else:
            lines.append("| " + " | ".join("(no data)" for _ in table.columns) + " |")
        parts.append("\n".join(lines))
    return "\n\n".join(parts) + "\n"


def to_json(tables: list[Table]) -> str:
    payload = [{"title": t.title, "columns": t.columns, "rows": t.rows} for t in tables]
    return json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n"


def to_csv(tables: list[Table]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    for table in tables:
        writer.writerow([f"# {table.title}"])
        writer.writerow(table.columns)
        for row in table.rows:
            writer.writerow(["" if c is None else c for c in row])
        writer.writerow([])
    return buffer.getvalue()


def render(tables: list[Table], fmt: str) -> str:
    if fmt in {"markdown", "md"}:
        return to_markdown(tables)
    if fmt == "json":
        return to_json(tables)
    if fmt == "csv":
        return to_csv(tables)
    raise ValueError(f"unsupported format: {fmt}")
