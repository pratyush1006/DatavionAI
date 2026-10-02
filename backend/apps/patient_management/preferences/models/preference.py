"""Patient-level general preference model."""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.patient_management.preferences.constants import (
    DEFAULT_DATE_FORMAT,
    DEFAULT_LANGUAGE,
    DEFAULT_TIME_FORMAT,
    DEFAULT_TIMEZONE,
)
from apps.patient_management.preferences.managers import PatientPreferenceManager
from apps.platform.organizations.models import Organization


class PatientPreference(BaseModel):
    """Store display, accessibility, and notification preferences."""

    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="preferences",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="patient_preferences",
    )
    language = models.CharField(
        max_length=20,
        default=DEFAULT_LANGUAGE.value,
    )
    timezone = models.CharField(
        max_length=100,
        default=DEFAULT_TIMEZONE,
    )
    date_format = models.CharField(
        max_length=20,
        default=DEFAULT_DATE_FORMAT.value,
    )
    time_format = models.CharField(
        max_length=10,
        default=DEFAULT_TIME_FORMAT.value,
    )
    accessibility = models.JSONField(
        default=dict,
        blank=True,
    )
    notification_preferences = models.JSONField(
        default=dict,
        blank=True,
    )

    objects = PatientPreferenceManager()

    class Meta:
        """Define database constraints and indexes."""

        db_table = "patient_management_patient_preference"
        indexes = (
            models.Index(
                fields=("organization", "patient"),
                name="patpref_org_patient_idx",
            ),
            models.Index(
                fields=("organization", "language"),
                name="patpref_org_lang_idx",
            ),
        )

    def __str__(self) -> str:
        """Return a stable human-readable identifier."""

        return f"Preferences for patient {self.patient_id}"


__all__ = ("PatientPreference",)
