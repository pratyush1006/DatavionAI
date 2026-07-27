"""
Signals for the Patient Preferences module.
"""

from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.patient_management.patients.models import Patient
from apps.patient_management.preferences.models import (
    PatientPreference,
)


@receiver(
    post_save,
    sender=Patient,
)
def create_patient_preferences(
    sender,
    instance: Patient,
    created: bool,
    **kwargs,
) -> None:
    """
    Automatically create default preferences
    when a patient is created.
    """
    if not created:
        return

    PatientPreference.objects.get_or_create(
        organization=instance.organization,
        patient=instance,
    )
