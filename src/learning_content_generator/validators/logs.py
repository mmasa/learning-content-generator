"""Validation of log files against the canonical Pydantic models.

Checks include schema conformance and cross-field rules such as
``spent_person_hours`` matching the sum of participant hours
(see docs/specifications/log-formats.md).
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ValidationError

from learning_content_generator.domain.models import (
    AIUsageRecord,
    IssueEstimate,
    WorkLogEntry,
)
from learning_content_generator.infrastructure.log_store import (
    ESTIMATES_FILENAME,
    iter_log_files,
    load_raw_entries,
)


def _validate_file(path: Path, model: type[BaseModel]) -> list[str]:
    try:
        entries = load_raw_entries(path)
    except (ValueError, yaml.YAMLError, OSError) as exc:
        return [f"{path}: {exc}"]
    errors: list[str] = []
    for index, entry in enumerate(entries):
        try:
            model.model_validate(entry)
        except ValidationError as exc:
            for err in exc.errors():
                location = ".".join(str(part) for part in err["loc"]) or "(entry)"
                errors.append(f"{path} entry {index}: {location}: {err['msg']}")
    return errors


def _collect(target: Path, *, exclude: frozenset[str] = frozenset()) -> list[Path]:
    if target.is_dir():
        return iter_log_files(target, exclude=exclude)
    return [target]


def validate_work_logs(target: Path) -> list[str]:
    """Validate a work log file, or every log file in a directory."""
    errors: list[str] = []
    for path in _collect(target, exclude=frozenset({ESTIMATES_FILENAME})):
        errors.extend(_validate_file(path, WorkLogEntry))
    estimates = target / ESTIMATES_FILENAME if target.is_dir() else None
    if estimates is not None and estimates.is_file():
        errors.extend(_validate_file(estimates, IssueEstimate))
    return errors


def validate_ai_usage(target: Path) -> list[str]:
    """Validate an AI usage log file, or every log file in a directory."""
    errors: list[str] = []
    for path in _collect(target):
        errors.extend(_validate_file(path, AIUsageRecord))
    return errors


def validate_estimates(path: Path) -> list[str]:
    return _validate_file(path, IssueEstimate)
