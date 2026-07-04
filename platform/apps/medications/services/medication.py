"""
Medication services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.medications.models import Medication


def create_medication(
    *,
    validated_data: Mapping[str, Any],
) -> Medication:
    """
    Create a medication.
    """

    return Medication.objects.create(
        **validated_data,
    )


def update_medication(
    *,
    instance: Medication,
    validated_data: Mapping[str, Any],
) -> Medication:
    """
    Update a medication.
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


def delete_medication(
    *,
    instance: Medication,
) -> None:
    """
    Delete a medication.
    """

    instance.delete()


__all__ = [
    "create_medication",
    "delete_medication",
    "update_medication",
]
