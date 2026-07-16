"""
Patient services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.clinical.patients.models import Patient


def create_patient(
    *,
    validated_data: Mapping[str, Any],
) -> Patient:
    """
    Create a new patient.
    """

    return Patient.objects.create(
        **validated_data,
    )


def update_patient(
    *,
    instance: Patient,
    validated_data: Mapping[str, Any],
) -> Patient:
    """
    Update an existing patient.
    """

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save(
        update_fields=list(validated_data.keys()),
    )

    return instance


def delete_patient(
    *,
    instance: Patient,
) -> None:
    """
    Delete a patient.
    """

    instance.delete()


__all__ = [
    "create_patient",
    "delete_patient",
    "update_patient",
]
