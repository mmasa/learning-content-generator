"""Importer interfaces: bring raw source data into a content pipeline.

Raw materials with unverified copyright must stay outside git
(contents/<name>/raw/ is git-ignored); importers read from there and write
schema-conformant files into contents/<name>/normalized/.
Concrete importers will be added per content category in future issues.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class Importer(Protocol):
    """Reads raw source files and produces normalized input records."""

    def import_source(self, source: Path, destination: Path) -> list[Path]:
        """Import raw data from ``source``; return the files written."""
        ...
