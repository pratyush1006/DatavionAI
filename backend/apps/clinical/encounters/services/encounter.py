"""
Encounter services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.clinical.encounters.models import Encounter


def create_encounter(
    *,
    validated_data: Mapping[str, Any],
) -> Encounter:
    """
    Create a new encounter.
    """

    return Encounter.objects.create(
        **validated_data,
    )


def update_encounter(
    *,
    instance: Encounter,
    validated_data: Mapping[str, Any],
) -> Encounter:
    """
    Update an existing encounter.
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


def delete_encounter(
    *,
    instance: Encounter,
) -> None:
    """
    Delete an encounter.
    """

    instance.delete()


__all__ = [
    "create_encounter",
    "delete_encounter",
    "update_encounter",
]
