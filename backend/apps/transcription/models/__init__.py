"""
Transcription models.

Captures audio transcription jobs and the structured clinical note that
is generated from the transcript.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.encounters.models import Encounter
from apps.core.models import BaseManager, BaseModel
from apps.notes.models import ClinicalNote
from apps.platform.organizations.models import Organization
from apps.transcription.constants import (
    TranscriptionProvider,
    TranscriptionStatus,
)


class TranscriptionJob(BaseModel):
    """
    A speech-to-text job for an audio recording.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="transcription_jobs",
        help_text="Owning organization.",
    )

    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.SET_NULL,
        related_name="transcription_jobs",
        null=True,
        blank=True,
        help_text="Encounter the audio relates to.",
    )

    provider = models.CharField(
        max_length=30,
        choices=TranscriptionProvider.CHOICES,
        default=TranscriptionProvider.OPENAI_WHISPER,
    )

    status = models.CharField(
        max_length=20,
        choices=TranscriptionStatus.CHOICES,
        default=TranscriptionStatus.PENDING,
        db_index=True,
    )

    audio_path = models.CharField(
        max_length=512,
        help_text="Storage path or URL of the source audio.",
    )

    transcript = models.TextField(
        blank=True,
        help_text="Verbatim transcript produced by the provider.",
    )

    language = models.CharField(
        max_length=10,
        blank=True,
        default="en",
    )

    error = models.TextField(
        blank=True,
        help_text="Error detail if the job failed.",
    )

    class Meta:
        db_table = "transcription_jobs"

        verbose_name = "Transcription Job"

        verbose_name_plural = "Transcription Jobs"

        ordering = ("-created_at",)

    def __str__(self) -> str:
        """Return a readable label."""

        return f"Transcription {self.pk} ({self.status})"


class GeneratedNote(BaseModel):
    """
    A clinical note produced from a transcription.
    """

    objects = BaseManager()

    job = models.OneToOneField(
        TranscriptionJob,
        on_delete=models.CASCADE,
        related_name="generated_note",
        help_text="Source transcription job.",
    )

    note = models.OneToOneField(
        ClinicalNote,
        on_delete=models.SET_NULL,
        related_name="generated_from_transcription",
        null=True,
        blank=True,
        help_text="Persisted clinical note, once reviewed.",
    )

    draft_text = models.TextField(
        blank=True,
        help_text="AI-generated structured draft before human review.",
    )

    review_required = models.BooleanField(
        default=True,
        help_text="Whether a clinician must review before signing.",
    )

    class Meta:
        db_table = "transcription_generated_notes"

        verbose_name = "Generated Note"

        verbose_name_plural = "Generated Notes"

        ordering = ("-created_at",)

    def __str__(self) -> str:
        """Return a readable label."""

        return f"Generated note for {self.job_id}"


__all__ = [
    "GeneratedNote",
    "TranscriptionJob",
]
