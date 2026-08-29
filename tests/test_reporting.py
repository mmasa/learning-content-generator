import datetime
from pathlib import Path

import pytest

from learning_content_generator.application import reporting
from learning_content_generator.domain.models import (
    AIUsageRecord,
    Cost,
    HumanReview,
    Measurement,
    Tokens,
)
from learning_content_generator.exporters.formats import Table, to_csv, to_json, to_markdown
from learning_content_generator.infrastructure.log_store import LogRepository


@pytest.fixture(scope="module")
def repo(examples_dir: Path) -> LogRepository:
    return LogRepository(examples_dir)


def find_table(tables: list[Table], title: str) -> Table:
    matches = [t for t in tables if t.title == title]
    assert matches, f"table {title!r} not found in {[t.title for t in tables]}"
    return matches[0]


class TestEffortReport:
    def test_effort_by_issue(self, repo: LogRepository) -> None:
        tables = reporting.effort_tables(repo.work_logs(), repo.estimates())
        by_issue = find_table(tables, "Effort by Issue")
        rows = {row[0]: row for row in by_issue.rows}
        # issue 123: 1.0 + 0.75 actual vs 2.0 estimated
        assert rows["#123"][2] == 2.0
        assert rows["#123"][3] == pytest.approx(1.75)
        assert rows["#123"][4] == pytest.approx(-0.25)
        assert rows["#123"][5] == pytest.approx(-12.5)
        # issue 130: overrun 1.5 vs 1.0 -> +50%
        assert rows["#130"][5] == pytest.approx(50.0)

    def test_contributor_hours_sum_individual_times(self, repo: LogRepository) -> None:
        tables = reporting.effort_tables(repo.work_logs(), repo.estimates())
        contributors = find_table(tables, "Effort by Contributor")
        rows = {row[0]: row for row in contributors.rows}
        assert rows["Masato Miyaichi"][1] == pytest.approx(2.5)
        assert rows["Masato Miyaichi"][2] == pytest.approx(2.0)  # AI-assisted
        assert rows["Member C"][1] == pytest.approx(0.5)

    def test_contributor_month_hours_exclude_other_participants(self, repo: LogRepository) -> None:
        # Two of the four July entries have other participants alongside
        # "Masato Miyaichi" (spent_person_hours 1.0 and 1.5), so a bucket that
        # summed the whole entry instead of this contributor's own hours
        # would report 4.0 instead of the correct 0.5 + 1.5 + 0.5 = 2.5.
        tables = reporting.contributor_tables("Masato Miyaichi", repo.work_logs(), repo.ai_usage())
        by_month = find_table(tables, "Effort by Month (Masato Miyaichi)")
        rows = {row[0]: row for row in by_month.rows}
        assert rows["2026-07"][2] == pytest.approx(2.5)

    def test_ai_vs_non_ai_split(self, repo: LogRepository) -> None:
        tables = reporting.effort_tables(repo.work_logs(), repo.estimates())
        split = find_table(tables, "AI vs Non-AI Work")
        rows = {row[0]: row for row in split.rows}
        assert rows["Yes"][2] == pytest.approx(2.5)
        assert rows["No"][2] == pytest.approx(2.25)


class TestAIUsageReport:
    def test_by_issue_token_sums(self, repo: LogRepository) -> None:
        tables = reporting.ai_usage_tables(repo.ai_usage())
        by_issue = find_table(tables, "AI Usage by Issue")
        rows = {row[0]: row for row in by_issue.rows}
        assert rows["#123"][2] == 12000  # input tokens
        assert rows["#123"][5] == 16200  # total tokens
        # issue 131 has only non-numeric token counts
        assert rows["#131"][5] == 0
        assert rows["#131"][7] == 1  # entries without numeric tokens

    def test_review_status(self, repo: LogRepository) -> None:
        tables = reporting.ai_usage_tables(repo.ai_usage())
        status = find_table(tables, "AI Output Review Status")
        rows = {row[0]: row[1] for row in status.rows}
        assert rows["approved"] == 2
        assert rows["pending"] == 1
        assert rows["approval rate (% of reviewed)"] == pytest.approx(100.0)

    def test_cost_kept_separate_by_currency(self) -> None:
        def make_record(amount: float, currency: str) -> AIUsageRecord:
            return AIUsageRecord(
                date=datetime.datetime(2026, 7, 1),
                operator="Masato Miyaichi",
                provider="Anthropic",
                product="Claude Code",
                model="m1",
                purpose="test",
                tokens=Tokens(),
                measurement=Measurement(type="unknown"),
                cost=Cost(amount=amount, currency=currency, type="actual"),
                human_review=HumanReview(status="pending"),
            )

        records = [make_record(1.0, "USD"), make_record(100.0, "JPY")]
        tables = reporting.ai_usage_tables(records)
        by_model = find_table(tables, "AI Usage by Model")
        cost_cell = by_model.rows[0][-2]
        assert isinstance(cost_cell, str)
        assert "1.0 USD" in cost_cell
        assert "100.0 JPY" in cost_cell

    def test_monthly_filter(self, repo: LogRepository) -> None:
        tables = reporting.monthly_tables(
            "2026-07", repo.work_logs(), repo.ai_usage(), repo.estimates()
        )
        assert any(t.rows for t in tables)
        empty = reporting.monthly_tables(
            "2030-01", repo.work_logs(), repo.ai_usage(), repo.estimates()
        )
        by_contributor = find_table(empty, "Effort by Contributor")
        assert by_contributor.rows == []


class TestFormats:
    def test_renderers_produce_output(self) -> None:
        tables = [Table(title="T", columns=["A", "B"], rows=[["x", 1.234]])]
        assert "| x | 1.23 |" in to_markdown(tables)
        assert '"title": "T"' in to_json(tables)
        assert "# T" in to_csv(tables)

    def test_markdown_empty_table(self) -> None:
        tables = [Table(title="Empty", columns=["A"], rows=[])]
        assert "(no data)" in to_markdown(tables)
