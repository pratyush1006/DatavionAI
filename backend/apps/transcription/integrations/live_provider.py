"""Fail-closed streaming speech provider contract."""

from dataclasses import dataclass
from importlib import import_module

from django.conf import settings


@dataclass(frozen=True, slots=True)
class StreamingTranscript:
    text: str
    kind: str
    sequence: int
    speaker_label: str = ""
    start_ms: int | None = None
    end_ms: int | None = None
    confidence: float | None = None
    provider_segment_id: str = ""


class StreamingSpeechProvider:
    def start(self, *, session_id, language, mime_type):
        raise NotImplementedError

    def push_audio(self, *, audio, sequence):
        raise NotImplementedError

    def finish(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


def get_streaming_provider():
    path = getattr(settings, "TRANSCRIPTION_STREAMING_PROVIDER", "").strip()
    if not path:
        raise RuntimeError("TRANSCRIPTION_STREAMING_PROVIDER is not configured.")
    module, name = path.rsplit(".", 1)
    return getattr(import_module(module), name)()
