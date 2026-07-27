"""
Services for PatientCommunicationPreference.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
)


@transaction.atomic
def create_communication_preference(
    **validated_data,
) -> PatientCommunicationPreference:
    """
    Create communication preference.
    """
    return PatientCommunicationPreference.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_communication_preference(
    *,
    preference: PatientCommunicationPreference,
    **validated_data,
) -> PatientCommunicationPreference:
    """
    Update communication preference.
    """
    for field, value in validated_data.items():
        setattr(
            preference,
            field,
            value,
        )

    preference.save()

    return preference


@transaction.atomic
def delete_communication_preference(
    *,
    preference: PatientCommunicationPreference,
) -> None:
    """
    Delete communication preference.
    """
    preference.delete()
