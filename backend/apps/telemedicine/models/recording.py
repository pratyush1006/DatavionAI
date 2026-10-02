from __future__ import annotations

import uuid

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.telemedicine.constants import RecordingStatus


class Recording(BaseModel):
    objects = BaseManager()
    session = models.ForeignKey(
        "telemedicine.TelemedicineSession",
        on_delete=models.CASCADE,
        related_name="recordings",
    )
    recording_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(
        max_length=20,
        choices=RecordingStatus.choices,
        default=RecordingStatus.REQUESTED,
        db_index=True,
    )
    recording_url = models.URLField(blank=True)
    transcript_url = models.URLField(blank=True)
    transcript_text = models.TextField(blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    file_size_bytes = models.PositiveBigIntegerField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finalized_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        db_table = "telemedicine_recordings"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["session", "status"], name="tele_rec_sess_status_idx")
        ]

    def __str__(self):
        return f"{self.recording_id} | {self.status}"
