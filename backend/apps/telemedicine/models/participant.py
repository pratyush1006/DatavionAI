from __future__ import annotations

from django.db import models
from django.utils import timezone

from apps.core.models import BaseManager, BaseModel
from apps.telemedicine.constants import (
    ConnectionQuality,
    MediaPermission,
    ParticipantStatus,
    ParticipantType,
)


class Participant(BaseModel):
    objects = BaseManager()
    session = models.ForeignKey(
        "telemedicine.TelemedicineSession",
        on_delete=models.CASCADE,
        related_name="participants",
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="telemedicine_participations",
    )
    participant_type = models.CharField(max_length=20, choices=ParticipantType.choices)
    status = models.CharField(
        max_length=20,
        choices=ParticipantStatus.choices,
        default=ParticipantStatus.INVITED,
        db_index=True,
    )
    invited_at = models.DateTimeField(null=True, blank=True)
    admitted_at = models.DateTimeField(null=True, blank=True)
    joined_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)
    connection_quality = models.CharField(
        max_length=20, choices=ConnectionQuality.choices, blank=True
    )
    microphone_enabled = models.BooleanField(default=True)
    camera_enabled = models.BooleanField(default=True)
    audio_connected = models.BooleanField(default=False)
    video_connected = models.BooleanField(default=False)
    microphone_permission = models.CharField(
        max_length=20, choices=MediaPermission.choices, default=MediaPermission.PROMPT
    )
    camera_permission = models.CharField(
        max_length=20, choices=MediaPermission.choices, default=MediaPermission.PROMPT
    )
    media_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "telemedicine_participants"
        ordering = ("session", "user")
        constraints = [
            models.UniqueConstraint(
                fields=["session", "user"], name="unique_tele_participant_session_user"
            )
        ]
        indexes = [
            models.Index(
                fields=["session", "status"], name="tele_part_sess_status_idx"
            ),
            models.Index(
                fields=["session", "joined_at"], name="tele_part_sess_join_idx"
            ),
        ]

    @property
    def is_present(self):
        return self.status == ParticipantStatus.JOINED

    def mark_media_state(self, **data):
        for field in (
            "microphone_enabled",
            "camera_enabled",
            "audio_connected",
            "video_connected",
            "microphone_permission",
            "camera_permission",
        ):
            if field in data:
                setattr(self, field, data[field])
        self.media_updated_at = timezone.now()

    def __str__(self):
        return f"{self.user_id} | {self.participant_type} | {self.session.session_id}"
