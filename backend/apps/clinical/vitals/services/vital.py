"""
Vital services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.clinical.vitals.models import Vital


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


def delete_vital(
    instance,
    *,
    organization,
    actor=None,
    request_user=None,
    performed_by=None,
    user=None,
    **kwargs,
):
    if getattr(instance, "organization_id", None) != getattr(organization, "id", None):
        raise ValueError("Vital does not belong to the organization.")
    resolved_actor = actor or request_user or performed_by or user
    user_id = (
        getattr(resolved_actor, "id", None) if resolved_actor is not None else None
    )
    delete_method = getattr(instance, "delete", None)
    if not callable(delete_method):
        raise RuntimeError("Vital model does not expose a delete operation.")
    try:
        delete_method(user_id=user_id)
    except TypeError:
        delete_method()
    return instance
