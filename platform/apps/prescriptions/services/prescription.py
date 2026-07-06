"""
Prescription services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.prescriptions.models import Prescription


def create_prescription(
    *,
    validated_data: Mapping[str, Any],
) -> Prescription:
    """
    Create a prescription.
    """

    return Prescription.objects.create(
        **validated_data,
    )


def update_prescription(
    *,
    instance: Prescription,
    validated_data: Mapping[str, Any],
) -> Prescription:
    """
    Update a prescription.
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


def delete_prescription(
    *,
    instance: Prescription,
) -> None:
    """
    Delete a prescription.
    """

    instance.delete()


__all__ = [
    "create_prescription",
    "delete_prescription",
    "update_prescription",
]
