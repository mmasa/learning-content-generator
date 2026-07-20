"""Aggregation of work logs and AI usage logs into report tables.

All statistics are derived from the structured logs under ``reports/``
(single source of truth); nothing is scraped from issues or PRs.
Non-numeric token counts (``unknown`` / ``not-provided`` / ``estimated``)
are counted as 0 in sums and reported separately so that estimates are
never silently treated as measurements.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Iterable

from learning_content_generator.domain.effort import variance_hours, variance_rate
from learning_content_generator.domain.models import (
    AIUsageRecord,
    IssueEstimate,
    TokenCount,
    WorkLogEntry,
)
from learning_content_generator.exporters.formats import Cell, Table


def token_int(value: TokenCount) -> int:
    """Numeric token value for sums; markers such as not-provided count as 0."""
    return value if isinstance(value, int) else 0


def _cost_amount(record: AIUsageRecord) -> float:
    amount = record.cost.amount
    return float(amount) if isinstance(amount, int | float) else 0.0


class _AIBucket:
    def __init__(self) -> None:
        self.runs = 0
        self.input = 0
        self.cached_input = 0
        self.output = 0
        self.reasoning = 0
        self.total = 0
        self.cost = 0.0
        self.non_numeric = 0

    def add(self, record: AIUsageRecord) -> None:
        self.runs += 1
        tokens = record.tokens
        self.input += token_int(tokens.input)
        self.cached_input += token_int(tokens.cached_input)
        self.output += token_int(tokens.output)
        self.reasoning += token_int(tokens.reasoning)
        self.total += token_int(tokens.total)
        self.cost += _cost_amount(record)
        if any(not isinstance(v, int) for v in (tokens.input, tokens.output, tokens.total)):
            self.non_numeric += 1


def _ai_group_table(
    title: str,
    key_label: str,
    records: Iterable[AIUsageRecord],
    key: Callable[[AIUsageRecord], str],
) -> Table:
    buckets: dict[str, _AIBucket] = defaultdict(_AIBucket)
    for record in records:
        buckets[key(record)].add(record)
    rows: list[list[Cell]] = [
        [
            name,
            b.runs,
            b.input,
            b.cached_input,
            b.output,
            b.total,
            round(b.cost, 4),
            b.non_numeric,
        ]
        for name, b in sorted(buckets.items())
    ]
    columns = [
        key_label,
        "Runs",
        "Input Tokens",
        "Cached Input",
        "Output Tokens",
        "Total Tokens",
        "Cost",
        "Entries w/o Numeric Tokens",
    ]
    return Table(title=title, columns=columns, rows=rows)


def _review_status_table(records: list[AIUsageRecord]) -> Table:
    counts: dict[str, int] = defaultdict(int)
    for record in records:
        counts[record.human_review.status] += 1
    reviewed = counts["approved"] + counts["rejected"] + counts["revised"]
    approval_rate: Cell = round(counts["approved"] / reviewed * 100, 1) if reviewed else None
    rows: list[list[Cell]] = [
        ["pending", counts["pending"]],
        ["approved", counts["approved"]],
        ["revised", counts["revised"]],
        ["rejected (差戻し)", counts["rejected"]],
        ["approval rate (% of reviewed)", approval_rate],
    ]
    return Table(title="AI Output Review Status", columns=["Status", "Count"], rows=rows)


def ai_usage_tables(records: list[AIUsageRecord]) -> list[Table]:
    def issue_key(r: AIUsageRecord) -> str:
        return f"#{r.issue}" if r.issue is not None else "(none)"

    def category_key(r: AIUsageRecord) -> str:
        return r.category or "(none)"

    return [
        _ai_group_table("AI Usage by Issue", "Issue", records, issue_key),
        _ai_group_table("AI Usage by Operator", "Operator", records, lambda r: r.operator),
        _ai_group_table("AI Usage by Tool", "Tool", records, lambda r: f"{r.provider} {r.product}"),
        _ai_group_table("AI Usage by Model", "Model", records, lambda r: r.model),
        _ai_group_table("AI Usage by Month", "Month", records, lambda r: r.month),
        _ai_group_table("AI Usage by Category", "Category", records, category_key),
        _review_status_table(records),
    ]


def _effort_by_issue_table(logs: list[WorkLogEntry], estimates: list[IssueEstimate]) -> Table:
    actual: dict[int, float] = defaultdict(float)
    for entry in logs:
        actual[entry.issue] += entry.spent_person_hours
    estimate_map = {e.issue: e for e in estimates}
    rows: list[list[Cell]] = []
    for issue in sorted(set(actual) | set(estimate_map)):
        estimate = estimate_map.get(issue)
        estimated = estimate.estimated_person_hours if estimate else None
        act = round(actual.get(issue, 0.0), 2)
        variance: Cell = None
        rate: Cell = None
        if estimated is not None:
            variance = round(variance_hours(act, estimated), 2)
            rate_value = variance_rate(act, estimated)
            rate = round(rate_value, 1) if rate_value is not None else None
        rows.append(
            [
                f"#{issue}",
                estimate.title if estimate else "(no estimate)",
                estimated,
                act,
                variance,
                rate,
            ]
        )
    columns = [
        "Issue",
        "Title",
        "Estimated PH",
        "Actual PH",
        "Variance Hours",
        "Variance Rate (%)",
    ]
    return Table(title="Effort by Issue", columns=columns, rows=rows)


def _hours_group_table(
    title: str,
    key_label: str,
    logs: Iterable[WorkLogEntry],
    key: Callable[[WorkLogEntry], str],
) -> Table:
    hours: dict[str, float] = defaultdict(float)
    entries: dict[str, int] = defaultdict(int)
    for entry in logs:
        hours[key(entry)] += entry.spent_person_hours
        entries[key(entry)] += 1
    rows: list[list[Cell]] = [
        [name, entries[name], round(hours[name], 2)] for name in sorted(hours)
    ]
    return Table(title=title, columns=[key_label, "Entries", "Person-Hours"], rows=rows)


def _contributor_table(logs: list[WorkLogEntry]) -> Table:
    total: dict[str, float] = defaultdict(float)
    with_ai: dict[str, float] = defaultdict(float)
    for entry in logs:
        for participant in entry.participants:
            total[participant.name] += participant.hours
            if entry.ai_used:
                with_ai[participant.name] += participant.hours
    rows: list[list[Cell]] = [
        [
            name,
            round(total[name], 2),
            round(with_ai[name], 2),
            round(total[name] - with_ai[name], 2),
        ]
        for name in sorted(total)
    ]
    columns = ["Contributor", "Person-Hours", "AI-Assisted PH", "Non-AI PH"]
    return Table(title="Effort by Contributor", columns=columns, rows=rows)


def effort_tables(logs: list[WorkLogEntry], estimates: list[IssueEstimate]) -> list[Table]:
    return [
        _effort_by_issue_table(logs, estimates),
        _contributor_table(logs),
        _hours_group_table("Effort by Work Type", "Work Type", logs, lambda e: e.work_type),
        _hours_group_table("Effort by Month", "Month", logs, lambda e: e.month),
        _hours_group_table(
            "Effort by Category", "Category", logs, lambda e: e.category or "(none)"
        ),
        _hours_group_table(
            "AI vs Non-AI Work", "AI Used", logs, lambda e: "Yes" if e.ai_used else "No"
        ),
    ]


def issue_tables(
    issue: int,
    logs: list[WorkLogEntry],
    records: list[AIUsageRecord],
    estimates: list[IssueEstimate],
) -> list[Table]:
    issue_logs = [e for e in logs if e.issue == issue]
    issue_records = [r for r in records if r.issue == issue]
    issue_estimates = [e for e in estimates if e.issue == issue]
    work_rows: list[list[Cell]] = [
        [
            str(e.date),
            e.work_type,
            e.summary,
            ", ".join(f"{p.name} {p.hours}h" for p in e.participants),
            round(e.spent_person_hours, 2),
            "Yes" if e.ai_used else "No",
        ]
        for e in sorted(issue_logs, key=lambda e: e.date)
    ]
    work_table = Table(
        title=f"Work Log for Issue #{issue}",
        columns=["Date", "Work Type", "Summary", "Participants", "Person-Hours", "AI Used"],
        rows=work_rows,
    )
    return [
        _effort_by_issue_table(issue_logs, issue_estimates),
        work_table,
        _ai_group_table(
            f"AI Usage for Issue #{issue}",
            "Model",
            issue_records,
            lambda r: r.model,
        ),
        _review_status_table(issue_records),
    ]


def monthly_tables(
    month: str,
    logs: list[WorkLogEntry],
    records: list[AIUsageRecord],
    estimates: list[IssueEstimate],
) -> list[Table]:
    month_logs = [e for e in logs if e.month == month]
    month_records = [r for r in records if r.month == month]
    return [
        _effort_by_issue_table(month_logs, estimates),
        _contributor_table(month_logs),
        _hours_group_table(
            f"Effort by Work Type ({month})", "Work Type", month_logs, lambda e: e.work_type
        ),
        _ai_group_table(
            f"AI Usage by Issue ({month})",
            "Issue",
            month_records,
            lambda r: f"#{r.issue}" if r.issue is not None else "(none)",
        ),
        _ai_group_table(f"AI Usage by Model ({month})", "Model", month_records, lambda r: r.model),
    ]


def contributor_tables(
    name: str, logs: list[WorkLogEntry], records: list[AIUsageRecord]
) -> list[Table]:
    person_logs = [e for e in logs if any(p.name == name for p in e.participants)]
    person_records = [r for r in records if r.operator == name]
    hours_rows: list[list[Cell]] = [
        [
            str(e.date),
            f"#{e.issue}",
            e.work_type,
            next(p.hours for p in e.participants if p.name == name),
            "Yes" if e.ai_used else "No",
        ]
        for e in sorted(person_logs, key=lambda e: e.date)
    ]
    detail = Table(
        title=f"Work Entries for {name}",
        columns=["Date", "Issue", "Work Type", "Hours", "AI Used"],
        rows=hours_rows,
    )
    return [
        detail,
        _hours_group_table(f"Effort by Month ({name})", "Month", person_logs, lambda e: e.month),
        _ai_group_table(f"AI Usage by Model ({name})", "Model", person_records, lambda r: r.model),
    ]
