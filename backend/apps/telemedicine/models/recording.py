"""
Telemedicine recording model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel


class Recording(BaseModel):
    """
    Represents a recording of a telemedicine session.
    """

    objects = BaseManager()

    session = models.ForeignKey(
        "telemedicine.TelemedicineSession",
        on_delete=models.CASCADE,
        related_name="recordings",
        help_text="Session that was recorded.",
    )

    recording_url = models.URLField(
        help_text="URL where the recording is stored.",
    )

    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Recording duration in seconds.",
    )

    file_size_bytes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Recording file size in bytes.",
    )

    transcript_url = models.URLField(
        blank=True,
        help_text="URL of the transcript file.",
    )

    transcript_text = models.TextField(
        blank=True,
        help_text="Transcript text content.",
    )

    is_processed = models.BooleanField(
        default=False,
        help_text="Whether the recording has been processed.",
    )

    class Meta:
        db_table = "telemedicine_recordings"

        verbose_name = "Telemedicine Recording"

        verbose_name_plural = "Telemedicine Recordings"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "session",
                    "created_at",
                ],
                name="tele_record_sess_crt_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"Recording - {self.session.session_id} ({self.duration_seconds}s)"


__all__ = [
    "Recording",
]
