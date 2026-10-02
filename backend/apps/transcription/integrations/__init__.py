"""
External transcription/AI provider integrations.
"""

from __future__ import annotations

from .providers import (
    ClinicalNoteGenerator,
    SpeechToTextProvider,
    TranscriptionResult,
    get_note_generator,
    get_speech_provider,
)

__all__ = (
    "ClinicalNoteGenerator",
    "SpeechToTextProvider",
    "TranscriptionResult",
    "get_note_generator",
    "get_speech_provider",
)
