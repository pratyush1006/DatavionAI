"""
Provider abstractions for speech-to-text and clinical-note generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any, Protocol

from django.conf import settings


@dataclass(frozen=True, slots=True)
class TranscriptionResult:
    text: str
    segments: list[dict[str, Any]]
    language: str
    duration_seconds: int | None
    speaker_count: int | None
    provider: str


class SpeechToTextProvider(Protocol):
    def transcribe(
        self,
        *,
        audio_uri: str,
        language: str,
        mime_type: str,
    ) -> TranscriptionResult: ...


class ClinicalNoteGenerator(Protocol):
    def generate(
        self,
        *,
        transcript: str,
        patient_id: str,
        encounter_id: str | None,
        note_type: str,
    ) -> dict[str, Any]: ...


def _load_provider(setting_name: str, protocol_name: str):
    path = getattr(settings, setting_name, "").strip()
    if not path:
        raise RuntimeError(
            f"{setting_name} is not configured. Configure a concrete {protocol_name} adapter."
        )
    module_name, class_name = path.rsplit(".", 1)
    return getattr(import_module(module_name), class_name)()


def get_speech_provider() -> SpeechToTextProvider:
    return _load_provider(
        "TRANSCRIPTION_SPEECH_PROVIDER",
        "SpeechToTextProvider",
    )


def get_note_generator() -> ClinicalNoteGenerator:
    return _load_provider(
        "TRANSCRIPTION_NOTE_PROVIDER",
        "ClinicalNoteGenerator",
    )
