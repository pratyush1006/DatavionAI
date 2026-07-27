"""
Transcription services.

Encapsulates speech-to-text and transcript-to-structured-note
generation. Uses the DatavionOS AI runtime for note generation.
"""

from __future__ import annotations

import os
from typing import Any

from apps.datavionos.ai.chat import (
    ChatMessage,
    ChatRequest,
    ChatRole,
)
from apps.datavionos.ai.implementation.chat import OpenAIChatModel
from apps.transcription.constants import TranscriptionStatus
from apps.transcription.models import GeneratedNote, TranscriptionJob

NOTE_PROMPT = (
    "Convert the following clinician-patient conversation transcript into a "
    "structured SOAP note. Return only valid JSON with keys: subjective, "
    "objective, assessment, plan. Do not invent facts not present.\n\n"
    "Transcript:\n{{ transcript }}"
)


class TranscriptionService:
    """
    Service for transcription and structured note generation.
    """

    @staticmethod
    def transcribe(
        *,
        job: TranscriptionJob,
    ) -> TranscriptionJob:
        """
        Run speech-to-text for a job and store the transcript.
        """

        job.status = TranscriptionStatus.PROCESSING
        job.save(update_fields=["status", "updated_at"])

        try:
            transcript = _run_speech_to_text(job)
        except Exception as exc:  # noqa: BLE001
            job.status = TranscriptionStatus.FAILED
            job.error = str(exc)
            job.save(update_fields=["status", "error", "updated_at"])
            return job

        job.transcript = transcript
        job.status = TranscriptionStatus.COMPLETED
        job.save(
            update_fields=[
                "transcript",
                "status",
                "updated_at",
            ]
        )

        return job

    @staticmethod
    def generate_note(
        *,
        job: TranscriptionJob,
        organization_id: Any | None = None,
    ) -> GeneratedNote:
        """
        Generate a structured clinical note draft from the transcript.
        """

        chat = OpenAIChatModel()

        response = _run_until_complete(
            chat.complete(
                ChatRequest(
                    messages=(
                        ChatMessage(
                            role=ChatRole.SYSTEM,
                            content=("You are a clinical documentation assistant."),
                        ),
                        ChatMessage(
                            role=ChatRole.USER,
                            content=NOTE_PROMPT.replace(
                                "{{ transcript }}",
                                job.transcript,
                            ),
                        ),
                    ),
                )
            )
        )

        note, _created = GeneratedNote.objects.update_or_create(
            job=job,
            defaults={"draft_text": response.message.content},
        )

        return note


def _run_speech_to_text(
    job: TranscriptionJob,
) -> str:
    """
    Dispatch to the configured speech-to-text provider.
    """

    if job.provider == TranscriptionProvider.LOCAL or not os.environ.get(
        "OPENAI_API_KEY"
    ):
        return f"[offline transcript] Audio for job {job.pk} would be transcribed here."

    from openai import OpenAI

    client = OpenAI()
    with open(job.audio_path, "rb") as audio_file:
        segment = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )

    return segment.text


def _run_until_complete(coroutine):
    """Run an async coroutine to completion without an event loop leak."""

    import asyncio

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        raise RuntimeError("Cannot run coroutine in a running loop")

    return asyncio.run(coroutine)


__all__ = [
    "TranscriptionService",
]
