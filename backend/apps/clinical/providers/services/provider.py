"""
Provider services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.clinical.providers.models import Provider


def create_provider(
    *,
    validated_data: Mapping[str, Any],
) -> Provider:
    """
    Create a new provider.
    """

    return Provider.objects.create(
        **validated_data,
    )


def update_provider(
    *,
    instance: Provider,
    validated_data: Mapping[str, Any],
) -> Provider:
    """
    Update an existing provider.
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


def delete_provider(
    *,
    instance: Provider,
) -> None:
    """
    Delete a provider.
    """

    instance.delete()


__all__ = [
    "create_provider",
    "delete_provider",
    "update_provider",
]
