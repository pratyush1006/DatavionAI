"""
Patient Timeline domain model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.patient_management.timeline.constants import (
    TimelineEventType,
    TimelineStatus,
)
from apps.patient_management.timeline.managers import TimelineEntryManager
from apps.patient_management.timeline.validators import validate_timeline_title
from apps.platform.organizations.models import Organization


class TimelineEntry(BaseModel):
    """Represent a chronological event in a patient's record."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="timeline_entries",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="timeline_entries",
    )
    event_type = models.CharField(
        max_length=32,
        choices=TimelineEventType.choices,
        default=TimelineEventType.SYSTEM,
    )
    title = models.CharField(
        max_length=255,
        validators=(validate_timeline_title,),
    )
    description = models.TextField(
        blank=True,
        default="",
    )
    occurred_at = models.DateTimeField()
    status = models.CharField(
        max_length=32,
        choices=TimelineStatus.choices,
        default=TimelineStatus.ACTIVE,
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_timeline_entries",
    )

    objects = TimelineEntryManager()

    class Meta:
        """Configure TimelineEntry persistence behavior."""

        ordering = (
            "-occurred_at",
            "-created_at",
        )
        indexes = (
            models.Index(
                fields=(
                    "organization",
                    "patient",
                    "occurred_at",
                ),
            ),
            models.Index(
                fields=(
                    "organization",
                    "status",
                    "is_deleted",
                ),
            ),
            models.Index(
                fields=(
                    "organization",
                    "is_active",
                    "occurred_at",
                ),
            ),
        )

    def __str__(self) -> str:
        """Return a readable Timeline entry label."""

        return f"{self.title} ({self.patient_id})"


__all__ = ("TimelineEntry",)
