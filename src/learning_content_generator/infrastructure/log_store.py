"""Loading of operational logs from the reports/ directory tree.

Layout (relative to a data directory, by default ``reports/``):

- ``ai-usage/*.yaml`` or ``*.jsonl``  — AI usage records
- ``effort/*.yaml``                   — work log entries
- ``effort/estimates.yaml``           — per-issue estimates
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from learning_content_generator.domain.models import (
    AIUsageRecord,
    IssueEstimate,
    WorkLogEntry,
)

LOG_SUFFIXES = {".yaml", ".yml", ".jsonl"}
ESTIMATES_FILENAME = "estimates.yaml"


def load_raw_entries(path: Path) -> list[dict[str, Any]]:
    """Load a log file (YAML list or JSONL) as a list of dicts."""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        data: Any = [json.loads(line) for line in text.splitlines() if line.strip()]
    else:
        data = yaml.safe_load(text)
    if data is None:
        return []
    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a list of entries, got {type(data).__name__}")
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise ValueError(f"{path}: entry {i} is not a mapping")
    return data


def iter_log_files(directory: Path, *, exclude: frozenset[str] = frozenset()) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(
        p
        for p in directory.iterdir()
        if p.is_file() and p.suffix in LOG_SUFFIXES and p.name not in exclude
    )


def load_ai_usage(directory: Path) -> list[AIUsageRecord]:
    records: list[AIUsageRecord] = []
    for path in iter_log_files(directory):
        records.extend(AIUsageRecord.model_validate(e) for e in load_raw_entries(path))
    return records


def load_work_logs(directory: Path) -> list[WorkLogEntry]:
    entries: list[WorkLogEntry] = []
    for path in iter_log_files(directory, exclude=frozenset({ESTIMATES_FILENAME})):
        entries.extend(WorkLogEntry.model_validate(e) for e in load_raw_entries(path))
    return entries


def load_estimates(path: Path) -> list[IssueEstimate]:
    if not path.is_file():
        return []
    return [IssueEstimate.model_validate(e) for e in load_raw_entries(path)]


class LogRepository:
    """Convenience access to all logs under one data directory."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir

    @property
    def ai_usage_dir(self) -> Path:
        return self.data_dir / "ai-usage"

    @property
    def effort_dir(self) -> Path:
        return self.data_dir / "effort"

    @property
    def estimates_path(self) -> Path:
        return self.effort_dir / ESTIMATES_FILENAME

    def ai_usage(self) -> list[AIUsageRecord]:
        return load_ai_usage(self.ai_usage_dir)

    def work_logs(self) -> list[WorkLogEntry]:
        return load_work_logs(self.effort_dir)

    def estimates(self) -> list[IssueEstimate]:
        return load_estimates(self.estimates_path)
