"""
Diagnosis services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.diagnoses.models import Diagnosis


def create_diagnosis(
    *,
    validated_data: Mapping[str, Any],
) -> Diagnosis:
    """
    Create a new diagnosis.
    """

    return Diagnosis.objects.create(
        **validated_data,
    )


def update_diagnosis(
    *,
    instance: Diagnosis,
    validated_data: Mapping[str, Any],
) -> Diagnosis:
    """
    Update an existing diagnosis.
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


def delete_diagnosis(
    *,
    instance: Diagnosis,
) -> None:
    """
    Delete a diagnosis.
    """

    instance.delete()


__all__ = [
    "create_diagnosis",
    "update_diagnosis",
    "delete_diagnosis",
]
