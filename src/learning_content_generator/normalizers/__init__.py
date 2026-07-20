"""Normalizer interfaces: clean and structure imported text.

Concrete normalizers (e.g. Takken text normalization) will be added in
future issues.
"""

from __future__ import annotations

from typing import Protocol


class Normalizer(Protocol):
    """Transforms raw text into normalized text suitable for generation."""

    def normalize(self, text: str) -> str: ...
