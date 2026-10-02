"""Patient communication-channel preference model."""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.preferences.constants import PreferenceChannel
from apps.patient_management.preferences.managers import (
    PatientCommunicationPreferenceManager,
)
from apps.patient_management.preferences.models.preference import PatientPreference


class PatientCommunicationPreference(BaseModel):
    """Store consent-like routing choices for one communication channel."""

    preference = models.ForeignKey(
        PatientPreference,
        on_delete=models.CASCADE,
        related_name="communication_preferences",
    )
    channel = models.CharField(
        max_length=20,
        choices=(
            (item.value, item.name.replace("_", " ").title())
            for item in PreferenceChannel
        ),
    )
    enabled = models.BooleanField(
        default=True,
    )
    appointment_reminders = models.BooleanField(
        default=True,
    )
    clinical_updates = models.BooleanField(
        default=True,
    )
    administrative_updates = models.BooleanField(
        default=True,
    )
    marketing_messages = models.BooleanField(
        default=False,
    )

    objects = PatientCommunicationPreferenceManager()

    class Meta:
        """Define database constraints."""

        db_table = "patient_management_communication_preference"
        constraints = (
            models.UniqueConstraint(
                fields=("preference", "channel"),
                name="patcomm_pref_channel_uniq",
            ),
        )
        indexes = (
            models.Index(
                fields=("preference", "channel"),
                name="patcomm_pref_channel_idx",
            ),
        )

    def __str__(self) -> str:
        """Return a stable human-readable identifier."""

        return f"{self.preference_id}:{self.channel}"


__all__ = ("PatientCommunicationPreference",)
