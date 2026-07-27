"""
Services for PatientPreference.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.preferences.models import (
    PatientPreference,
)


@transaction.atomic
def create_patient_preference(
    **validated_data,
) -> PatientPreference:
    """
    Create patient preferences.
    """
    return PatientPreference.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_patient_preference(
    *,
    preference: PatientPreference,
    **validated_data,
) -> PatientPreference:
    """
    Update patient preferences.
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
def delete_patient_preference(
    *,
    preference: PatientPreference,
) -> None:
    """
    Delete patient preferences.
    """
    preference.delete()
