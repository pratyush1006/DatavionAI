"""
Selectors for PatientCommunicationPreference.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
)


def get_communication_preferences(
    *,
    organization_id: int,
    patient_id: int,
) -> QuerySet[PatientCommunicationPreference]:
    """
    Return communication preferences for a patient.
    """
    return (
        PatientCommunicationPreference.objects.by_organization(
            organization_id,
        )
        .by_patient(
            patient_id,
        )
        .ordered()
    )


def get_enabled_communication_preferences(
    *,
    organization_id: int,
    patient_id: int,
) -> QuerySet[PatientCommunicationPreference]:
    """
    Return enabled communication preferences.
    """
    return get_communication_preferences(
        organization_id=organization_id,
        patient_id=patient_id,
    ).enabled()


def get_communication_preference(
    *,
    organization_id: int,
    patient_id: int,
    channel: str,
) -> PatientCommunicationPreference:
    """
    Return a communication preference by channel.
    """
    return get_communication_preferences(
        organization_id=organization_id,
        patient_id=patient_id,
    ).get(
        channel=channel,
    )
