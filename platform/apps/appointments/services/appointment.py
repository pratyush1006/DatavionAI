"""
Appointment services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.appointments.models import Appointment


def create_appointment(
    *,
    validated_data: Mapping[str, Any],
) -> Appointment:
    """
    Create a new appointment.
    """

    return Appointment.objects.create(
        **validated_data,
    )


def update_appointment(
    *,
    instance: Appointment,
    validated_data: Mapping[str, Any],
) -> Appointment:
    """
    Update an existing appointment.
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


def delete_appointment(
    *,
    instance: Appointment,
) -> None:
    """
    Delete an appointment.
    """

    instance.delete()


__all__ = [
    "create_appointment",
    "update_appointment",
    "delete_appointment",
]
