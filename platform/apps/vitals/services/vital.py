"""
Vital services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.vitals.models import Vital


def create_vital(
    *,
    validated_data: Mapping[str, Any],
) -> Vital:
    """
    Create a vital record.
    """

    return Vital.objects.create(
        **validated_data,
    )


def update_vital(
    *,
    instance: Vital,
    validated_data: Mapping[str, Any],
) -> Vital:
    """
    Update a vital record.
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


def delete_vital(
    *,
    instance: Vital,
) -> None:
    """
    Delete a vital record.
    """

    instance.delete()


__all__ = [
    "create_vital",
    "delete_vital",
    "update_vital",
]
