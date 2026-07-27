"""
Transcription constants.
"""

from __future__ import annotations


class TranscriptionStatus:
    """
    Lifecycle states for a transcription job.
    """

    PENDING = "pending"

    PROCESSING = "processing"

    COMPLETED = "completed"

    FAILED = "failed"

    CHOICES = (
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
    )


class TranscriptionProvider:
    """
    Supported speech-to-text providers.
    """

    OPENAI_WHISPER = "openai_whisper"

    LOCAL = "local"

    CHOICES = (
        (OPENAI_WHISPER, "OpenAI Whisper"),
        (LOCAL, "Local"),
    )


__all__ = [
    "TranscriptionProvider",
    "TranscriptionStatus",
]
