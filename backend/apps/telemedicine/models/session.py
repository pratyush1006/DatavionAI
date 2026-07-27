"""
Telemedicine session model.
"""

from __future__ import annotations

import uuid

from django.db import models

from apps.clinical.patients.models import Patient
from apps.clinical.providers.models import Provider
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization
from apps.telemedicine.constants import (
    DEFAULT_SESSION_STATUS,
    SessionStatus,
    SessionType,
)


class TelemedicineSession(BaseModel):
    """
    Represents a virtual consultation session.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="telemedicine_sessions",
        help_text="Organization that owns the session.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="telemedicine_sessions",
        help_text="Patient participating in the session.",
    )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="telemedicine_sessions",
        help_text="Provider conducting the session.",
    )

    appointment = models.OneToOneField(
        "appointments.Appointment",
        on_delete=models.SET_NULL,
        related_name="telemedicine_session",
        null=True,
        blank=True,
        help_text="Associated appointment, if any.",
    )

    session_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique session identifier.",
    )

    scheduled_start = models.DateTimeField(
        help_text="Scheduled session start time.",
    )

    scheduled_end = models.DateTimeField(
        help_text="Scheduled session end time.",
    )

    actual_start = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Actual session start time.",
    )

    actual_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Actual session end time.",
    )

    status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=DEFAULT_SESSION_STATUS,
        db_index=True,
        help_text="Session lifecycle status.",
    )

    session_type = models.CharField(
        max_length=20,
        choices=SessionType.choices,
        default=SessionType.VIDEO,
        help_text="Type of telemedicine session.",
    )

    connection_url = models.URLField(
        help_text="URL for joining the session.",
    )

    connection_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Connection identifier from the telephony provider.",
    )

    recording_url = models.URLField(
        blank=True,
        help_text="URL of the session recording.",
    )

    recording_consent = models.BooleanField(
        default=False,
        help_text="Whether the patient consented to recording.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Session notes.",
    )

    class Meta:
        db_table = "telemedicine_sessions"

        verbose_name = "Telemedicine Session"

        verbose_name_plural = "Telemedicine Sessions"

        ordering = ("-scheduled_start",)

        indexes = [
            models.Index(
                fields=[
                    "patient",
                    "scheduled_start",
                ],
                name="tele_session_patient_start_idx",
            ),
            models.Index(
                fields=[
                    "provider",
                    "scheduled_start",
                ],
                name="tele_sess_prov_start_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="tele_session_org_status_idx",
            ),
            models.Index(
                fields=[
                    "appointment",
                ],
                name="tele_session_appointment_idx",
            ),
        ]

    def save(self, *args, **kwargs) -> None:
        """
        Generate session_id if not set and validate before saving.
        """

        if not self.session_id:
            self.session_id = str(uuid.uuid4())

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.session_id} | {self.patient.full_name} | {self.status}"


__all__ = [
    "TelemedicineSession",
]
