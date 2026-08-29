"""TTS provider abstraction.

Implementations MUST:

- read service credentials from environment variables only,
- never write audio files into git-tracked locations
  (``contents/*/audio/`` is git-ignored; only metadata conforming to
  ``contents/<name>/schemas/audio-metadata.schema.json`` is committed).

Concrete providers will be added in future issues.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class SynthesisResult:
    audio: bytes
    audio_format: str
    provider: str
    voice: str


class TTSProvider(Protocol):
    """Synthesizes a reading script into audio."""

    def synthesize(self, text: str, *, voice: str) -> SynthesisResult: ...
