"""`lcg` CLI: reports and validation over operational logs.

Examples:
    uv run lcg report ai-usage
    uv run lcg report effort --format csv
    uv run lcg report issue --issue 123
    uv run lcg report monthly --month 2026-07
    uv run lcg report contributor --name "Masato Miyaichi"
    uv run lcg validate ai-usage reports/ai-usage
    uv run lcg validate work-log reports/effort
"""

from __future__ import annotations

import re
from collections.abc import Callable
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer

from learning_content_generator.application import reporting
from learning_content_generator.exporters.formats import Table, render
from learning_content_generator.infrastructure.log_store import LogRepository
from learning_content_generator.validators import logs as log_validators

app = typer.Typer(no_args_is_help=True, help="Learning content generator toolkit.")
report_app = typer.Typer(no_args_is_help=True, help="Aggregate effort and AI usage logs.")
validate_app = typer.Typer(no_args_is_help=True, help="Validate structured log files.")
app.add_typer(report_app, name="report")
app.add_typer(validate_app, name="validate")

MONTH_PATTERN = re.compile(r"^\d{4}-\d{2}$")


class OutputFormat(StrEnum):
    MARKDOWN = "markdown"
    JSON = "json"
    CSV = "csv"


DataDir = Annotated[
    Path,
    typer.Option("--data-dir", help="Directory containing ai-usage/ and effort/ logs."),
]
Format = Annotated[OutputFormat, typer.Option("--format", "-f", help="Output format.")]


def _emit(tables: list[Table], fmt: OutputFormat) -> None:
    typer.echo(render(tables, fmt.value), nl=False)


@report_app.command("ai-usage")
def report_ai_usage(
    data_dir: DataDir = Path("reports"), fmt: Format = OutputFormat.MARKDOWN
) -> None:
    """AI usage statistics (per issue, operator, tool, model, month, category)."""
    repo = LogRepository(data_dir)
    _emit(reporting.ai_usage_tables(repo.ai_usage()), fmt)


@report_app.command("effort")
def report_effort(data_dir: DataDir = Path("reports"), fmt: Format = OutputFormat.MARKDOWN) -> None:
    """Person-hour statistics (estimates, actuals, variance, breakdowns)."""
    repo = LogRepository(data_dir)
    _emit(reporting.effort_tables(repo.work_logs(), repo.estimates()), fmt)


@report_app.command("issue")
def report_issue(
    issue: Annotated[int, typer.Option("--issue", help="Issue number.")],
    data_dir: DataDir = Path("reports"),
    fmt: Format = OutputFormat.MARKDOWN,
) -> None:
    """Combined effort and AI usage report for one issue."""
    repo = LogRepository(data_dir)
    tables = reporting.issue_tables(issue, repo.work_logs(), repo.ai_usage(), repo.estimates())
    _emit(tables, fmt)


@report_app.command("monthly")
def report_monthly(
    month: Annotated[str, typer.Option("--month", help="Month as YYYY-MM.")],
    data_dir: DataDir = Path("reports"),
    fmt: Format = OutputFormat.MARKDOWN,
) -> None:
    """Monthly effort and AI usage report."""
    if not MONTH_PATTERN.match(month):
        typer.echo(f"error: --month must be YYYY-MM, got {month!r}", err=True)
        raise typer.Exit(code=2)
    repo = LogRepository(data_dir)
    tables = reporting.monthly_tables(month, repo.work_logs(), repo.ai_usage(), repo.estimates())
    _emit(tables, fmt)


@report_app.command("contributor")
def report_contributor(
    name: Annotated[str, typer.Option("--name", help="Contributor name.")],
    data_dir: DataDir = Path("reports"),
    fmt: Format = OutputFormat.MARKDOWN,
) -> None:
    """Per-contributor effort and AI usage report."""
    repo = LogRepository(data_dir)
    _emit(reporting.contributor_tables(name, repo.work_logs(), repo.ai_usage()), fmt)


def _run_validation(targets: list[Path], validate: Callable[[Path], list[str]]) -> None:
    errors: list[str] = []
    for target in targets:
        if not target.exists():
            errors.append(f"{target}: does not exist")
            continue
        errors.extend(validate(target))
    if errors:
        for error in errors:
            typer.echo(error, err=True)
        typer.echo(f"validation failed: {len(errors)} error(s)", err=True)
        raise typer.Exit(code=1)
    typer.echo("OK")


@validate_app.command("ai-usage")
def validate_ai_usage(
    targets: Annotated[list[Path] | None, typer.Argument(help="Log files or directories.")] = None,
) -> None:
    """Validate AI usage logs (default: reports/ai-usage)."""
    _run_validation(targets or [Path("reports/ai-usage")], log_validators.validate_ai_usage)


@validate_app.command("work-log")
def validate_work_log(
    targets: Annotated[list[Path] | None, typer.Argument(help="Log files or directories.")] = None,
) -> None:
    """Validate work logs and estimates (default: reports/effort)."""
    _run_validation(targets or [Path("reports/effort")], log_validators.validate_work_logs)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
