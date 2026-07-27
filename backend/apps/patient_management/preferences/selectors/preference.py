"""
Selectors for PatientPreference.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.preferences.models import (
    PatientPreference,
)


def get_patient_preferences() -> QuerySet[PatientPreference]:
    """
    Return all patient preferences.
    """
    return PatientPreference.objects.select_related(
        "organization",
        "patient",
    ).all()


def get_patient_preference(
    *,
    organization_id: int,
    patient_id: int,
) -> PatientPreference:
    """
    Return a patient's preferences.
    """
    return (
        PatientPreference.objects.by_organization(
            organization_id,
        )
        .by_patient(
            patient_id,
        )
        .select_related(
            "organization",
            "patient",
        )
        .get()
    )
