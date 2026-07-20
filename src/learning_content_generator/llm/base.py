"""LLM provider abstraction.

Implementations MUST:

- read credentials from environment variables only (never from committed files),
- report token usage exactly as returned by the provider, using
  ``"not-provided"`` when the provider does not return a count
  (never fabricate or silently estimate),
- ensure every call ends up in the AI usage log
  (``reports/ai-usage/``, schema ``schemas/ai-usage-log.schema.json``).

Concrete providers will be added in future issues.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from learning_content_generator.domain.models import TokenCount


@dataclass
class LLMResult:
    text: str
    model: str
    input_tokens: TokenCount = "not-provided"
    cached_input_tokens: TokenCount = "not-provided"
    output_tokens: TokenCount = "not-provided"
    reasoning_tokens: TokenCount = "not-provided"


class LLMClient(Protocol):
    """Minimal text-generation interface."""

    def generate(self, prompt: str) -> LLMResult: ...
