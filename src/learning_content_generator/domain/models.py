"""Pydantic models for work logs, AI usage logs, and issue estimates.

These models are the canonical definition of the log formats. The JSON
Schemas under ``schemas/`` express the same structure for external tooling;
if they diverge, file an issue (see docs/specifications/log-formats.md).
"""

from __future__ import annotations

import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

TokenCount = int | Literal["unknown", "not-provided", "estimated"]
MeasurementType = Literal["actual", "estimated", "unknown"]
WorkType = Literal[
    "Implementation",
    "Review",
    "Fix",
    "Meeting",
    "Research",
    "Data Creation",
    "Documentation",
    "Testing",
    "Incident Response",
    "Other",
]

HOURS_TOLERANCE = 0.01


class Participant(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    hours: float = Field(ge=0)


class WorkLogEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date: datetime.date
    issue: int = Field(ge=0)
    work_type: WorkType
    summary: str = Field(min_length=1)
    participants: list[Participant] = Field(min_length=1)
    elapsed_hours: float = Field(ge=0)
    # Must equal the sum of participant hours; each participant's time is
    # recorded individually because not everyone works the same duration.
    spent_person_hours: float = Field(ge=0)
    ai_used: bool
    ai_tool: str | None = None
    category: str | None = None
    result: str | None = None
    remaining_work: str | None = None

    @model_validator(mode="after")
    def _check_consistency(self) -> WorkLogEntry:
        total = sum(p.hours for p in self.participants)
        if abs(total - self.spent_person_hours) > HOURS_TOLERANCE:
            raise ValueError(
                f"spent_person_hours ({self.spent_person_hours}) does not match "
                f"the sum of participant hours ({total})"
            )
        if self.ai_used and not self.ai_tool:
            raise ValueError("ai_tool is required when ai_used is true")
        return self

    @property
    def month(self) -> str:
        return self.date.strftime("%Y-%m")


class Tokens(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input: TokenCount = "not-provided"
    cached_input: TokenCount = "not-provided"
    output: TokenCount = "not-provided"
    reasoning: TokenCount = "not-provided"
    total: TokenCount = "not-provided"


class Measurement(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: MeasurementType


class Cost(BaseModel):
    model_config = ConfigDict(extra="forbid")

    amount: float | Literal["unknown", "not-provided"]
    currency: str = Field(min_length=3, max_length=3)
    type: MeasurementType


class HumanReview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["pending", "approved", "rejected", "revised"]
    reviewer: str | None = None
    result: str | None = None


class AIUsageRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    date: datetime.datetime
    issue: int | None = Field(default=None, ge=0)
    pull_request: int | None = Field(default=None, ge=0)
    operator: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    product: str = Field(min_length=1)
    model: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    category: str | None = None
    tokens: Tokens
    measurement: Measurement
    cost: Cost
    prompt_reference: str | None = None
    generated_files: list[str] = Field(default_factory=list)
    human_review: HumanReview
    notes: str | None = None

    @property
    def month(self) -> str:
        return self.date.strftime("%Y-%m")


class IssueEstimate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    issue: int = Field(ge=0)
    title: str = Field(min_length=1)
    estimated_person_hours: float = Field(ge=0)
    category: str | None = None
    assignee: str | None = None
