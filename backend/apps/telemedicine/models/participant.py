"""
Telemedicine participant model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.telemedicine.constants import (
    ConnectionQuality,
    ParticipantType,
)


class Participant(BaseModel):
    """
    Represents a participant in a telemedicine session.
    """

    objects = BaseManager()

    session = models.ForeignKey(
        "telemedicine.TelemedicineSession",
        on_delete=models.CASCADE,
        related_name="participants",
        help_text="Session this participant belongs to.",
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="telemedicine_participations",
        help_text="User participating in the session.",
    )

    participant_type = models.CharField(
        max_length=20,
        choices=ParticipantType.choices,
        help_text="Role of the participant.",
    )

    joined_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Time the participant joined the session.",
    )

    left_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Time the participant left the session.",
    )

    is_present = models.BooleanField(
        default=False,
        help_text="Whether the participant is currently present.",
    )

    connection_quality = models.CharField(
        max_length=20,
        choices=ConnectionQuality.choices,
        blank=True,
        help_text="Connection quality rating.",
    )

    class Meta:
        db_table = "telemedicine_participants"

        verbose_name = "Telemedicine Participant"

        verbose_name_plural = "Telemedicine Participants"

        ordering = (
            "session",
            "user",
        )

        indexes = [
            models.Index(
                fields=[
                    "session",
                    "user",
                ],
                name="tele_part_sess_user_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "session",
                    "user",
                ],
                name="unique_participant_per_session",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.user.full_name} ({self.participant_type}) "
            f"- {self.session.session_id}"
        )


__all__ = [
    "Participant",
]
