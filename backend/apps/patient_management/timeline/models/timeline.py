"""
Timeline models.
"""

from __future__ import annotations

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.patient_management.timeline.constants import (
    TimelineEventType,
    TimelineEventVisibility,
)
from apps.platform.organizations.models import Organization
from django.db import models


class PatientTimelineEvent(BaseModel):
    """
    A chronological event on the patient timeline.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_timeline_events",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="timeline_events",
    )

    event_type = models.CharField(
        max_length=20,
        choices=TimelineEventType.choices,
        default=TimelineEventType.NOTE,
        db_index=True,
    )

    title = models.CharField(
        max_length=255,
        help_text="Short event title.",
    )

    description = models.TextField(
        blank=True,
        help_text="Event details.",
    )

    occurred_at = models.DateTimeField(
        help_text="When the event occurred.",
    )

    visibility = models.CharField(
        max_length=20,
        choices=TimelineEventVisibility.choices,
        default=TimelineEventVisibility.INTERNAL,
    )

    reference_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Related entity type (e.g. Appointment).",
    )

    reference_id = models.UUIDField(
        null=True,
        blank=True,
        help_text="Related entity identifier.",
    )

    created_by = models.CharField(
        max_length=150,
        blank=True,
        help_text="Actor who created the event.",
    )

    class Meta:
        db_table = "patient_timeline_events"

        verbose_name = "Patient Timeline Event"

        verbose_name_plural = "Patient Timeline Events"

        ordering = ("-occurred_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "event_type",
                ],
                name="timeline_org_pat_type_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.get_event_type_display()}: {self.title}"


__all__ = [
    "PatientTimelineEvent",
]
