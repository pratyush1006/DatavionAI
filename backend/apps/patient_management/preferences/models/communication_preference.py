"""
Patient communication preference model.
"""

from __future__ import annotations

from django.db import models

from apps.common.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.notifications.constants import (
    NotificationChannelType,
)
from apps.platform.organizations.models import Organization


class PatientCommunicationPreference(BaseModel):
    """
    Stores notification channel preferences for a patient.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_communication_preferences",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="communication_preferences",
    )

    channel = models.CharField(
        max_length=32,
        choices=NotificationChannelType.choices,
    )

    priority = models.PositiveSmallIntegerField(
        default=1,
    )

    enabled = models.BooleanField(
        default=True,
    )

    appointment_notifications = models.BooleanField(
        default=True,
    )

    clinical_notifications = models.BooleanField(
        default=True,
    )

    laboratory_notifications = models.BooleanField(
        default=True,
    )

    radiology_notifications = models.BooleanField(
        default=True,
    )

    pharmacy_notifications = models.BooleanField(
        default=True,
    )

    billing_notifications = models.BooleanField(
        default=True,
    )

    insurance_notifications = models.BooleanField(
        default=True,
    )

    marketing_notifications = models.BooleanField(
        default=False,
    )

    emergency_notifications = models.BooleanField(
        default=True,
    )

    ai_assistant_notifications = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Patient Communication Preference"

        verbose_name_plural = "Patient Communication Preferences"

        ordering = ("priority",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "patient",
                    "channel",
                ],
                name="uq_patient_channel",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                ],
            ),
            models.Index(
                fields=[
                    "channel",
                ],
            ),
            models.Index(
                fields=[
                    "enabled",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.patient} - {self.get_channel_display()}"
