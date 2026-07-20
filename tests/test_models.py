import datetime
from typing import Any

import pytest
from pydantic import ValidationError

from learning_content_generator.domain.models import AIUsageRecord, WorkLogEntry


def work_log_data(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "date": "2026-07-20",
        "issue": 123,
        "work_type": "Implementation",
        "summary": "Test entry",
        "participants": [
            {"name": "A", "hours": 0.5},
            {"name": "B", "hours": 0.5},
        ],
        "elapsed_hours": 0.5,
        "spent_person_hours": 1.0,
        "ai_used": False,
    }
    data.update(overrides)
    return data


class TestWorkLogEntry:
    def test_valid_entry(self) -> None:
        entry = WorkLogEntry.model_validate(work_log_data())
        assert entry.spent_person_hours == 1.0
        assert entry.month == "2026-07"
        assert entry.date == datetime.date(2026, 7, 20)

    def test_rejects_mismatched_spent_hours(self) -> None:
        with pytest.raises(ValidationError, match="does not match"):
            WorkLogEntry.model_validate(work_log_data(spent_person_hours=2.0))

    def test_rejects_ai_used_without_tool(self) -> None:
        with pytest.raises(ValidationError, match="ai_tool is required"):
            WorkLogEntry.model_validate(work_log_data(ai_used=True))

    def test_accepts_ai_used_with_tool(self) -> None:
        entry = WorkLogEntry.model_validate(work_log_data(ai_used=True, ai_tool="Claude Code"))
        assert entry.ai_tool == "Claude Code"

    def test_rejects_unknown_work_type(self) -> None:
        with pytest.raises(ValidationError):
            WorkLogEntry.model_validate(work_log_data(work_type="Sleeping"))


def ai_usage_data(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "date": "2026-07-20T14:30:00+09:00",
        "issue": 123,
        "operator": "A",
        "provider": "Anthropic",
        "product": "Claude Code",
        "model": "claude-fable-5",
        "purpose": "testing",
        "tokens": {"input": 100, "output": 50, "total": 150},
        "measurement": {"type": "actual"},
        "cost": {"amount": 0.0, "currency": "USD", "type": "unknown"},
        "human_review": {"status": "pending"},
    }
    data.update(overrides)
    return data


class TestAIUsageRecord:
    def test_valid_record(self) -> None:
        record = AIUsageRecord.model_validate(ai_usage_data())
        assert record.tokens.input == 100
        assert record.tokens.reasoning == "not-provided"
        assert record.month == "2026-07"

    def test_accepts_token_markers(self) -> None:
        record = AIUsageRecord.model_validate(
            ai_usage_data(
                tokens={"input": "not-provided", "output": "unknown", "total": "estimated"}
            )
        )
        assert record.tokens.input == "not-provided"

    def test_rejects_invalid_token_marker(self) -> None:
        with pytest.raises(ValidationError):
            AIUsageRecord.model_validate(
                ai_usage_data(tokens={"input": "roughly-a-lot", "output": 1, "total": 1})
            )

    def test_rejects_invalid_review_status(self) -> None:
        with pytest.raises(ValidationError):
            AIUsageRecord.model_validate(ai_usage_data(human_review={"status": "maybe"}))

    def test_cost_amount_unknown(self) -> None:
        record = AIUsageRecord.model_validate(
            ai_usage_data(cost={"amount": "unknown", "currency": "USD", "type": "unknown"})
        )
        assert record.cost.amount == "unknown"
