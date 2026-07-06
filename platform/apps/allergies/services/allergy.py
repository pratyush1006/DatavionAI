"""
Allergy services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.allergies.models import Allergy


def create_allergy(
    *,
    validated_data: Mapping[str, Any],
) -> Allergy:
    """
    Create an allergy.
    """

    return Allergy.objects.create(
        **validated_data,
    )


def update_allergy(
    *,
    instance: Allergy,
    validated_data: Mapping[str, Any],
) -> Allergy:
    """
    Update an allergy.
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


def delete_allergy(
    *,
    instance: Allergy,
) -> None:
    """
    Delete an allergy.
    """

    instance.delete()


__all__ = [
    "create_allergy",
    "delete_allergy",
    "update_allergy",
]
