"""Generator interfaces: produce learning content from normalized data.

Generators that call an LLM must go through the abstraction in
``learning_content_generator.llm`` so that every call is captured in the
AI usage log. Concrete generators (quiz, explanation, reading script)
will be added in future issues.
"""

from __future__ import annotations

from typing import Protocol


class Generator(Protocol):
    """Produces a generated artifact (quiz, explanation, reading script)."""

    def generate(self, source: str) -> str: ...
