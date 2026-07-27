"""
Patient preference model.
"""

from __future__ import annotations

from django.db import models

from apps.common.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.patient_management.preferences.constants import (
    Language,
    PreferenceStatus,
    ReminderPreference,
    ThemePreference,
)
from apps.patient_management.preferences.managers import (
    PatientPreferenceManager,
)
from apps.patient_management.preferences.validators import (
    validate_language,
    validate_preferred_name,
    validate_timezone,
)
from apps.platform.organizations.models import Organization


class PatientPreference(BaseModel):
    """
    Stores global patient preferences.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_preferences",
    )

    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="preferences",
    )

    language = models.CharField(
        max_length=10,
        choices=Language.choices,
        default=Language.ENGLISH,
        validators=[
            validate_language,
        ],
    )

    timezone = models.CharField(
        max_length=100,
        default="Asia/Kolkata",
        validators=[
            validate_timezone,
        ],
    )

    preferred_name = models.CharField(
        max_length=100,
        blank=True,
        validators=[
            validate_preferred_name,
        ],
    )

    portal_theme = models.CharField(
        max_length=20,
        choices=ThemePreference.choices,
        default=ThemePreference.SYSTEM,
    )

    appointment_reminder = models.CharField(
        max_length=10,
        choices=ReminderPreference.choices,
        default=ReminderPreference.ONE_DAY,
    )

    accessibility_mode = models.BooleanField(
        default=False,
    )

    ai_personalization = models.BooleanField(
        default=True,
    )

    data_sharing_consent = models.BooleanField(
        default=False,
    )

    status = models.CharField(
        max_length=20,
        choices=PreferenceStatus.choices,
        default=PreferenceStatus.ACTIVE,
    )

    objects = PatientPreferenceManager()

    class Meta:
        verbose_name = "Patient Preference"
        verbose_name_plural = "Patient Preferences"

        ordering = ("patient",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "patient",
                ],
                name="uq_patient_preference",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return self.preferred_name or str(self.patient)
