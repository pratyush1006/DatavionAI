"""
Business services for shifts.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.hr.shifts.models import Shift

type ShiftData = Mapping[str, object]


def _validate_shift_data(
    *,
    validated_data: ShiftData,
    instance: Shift | None = None,
) -> None:
    """
    Validate shift business rules.
    """

    organization = validated_data.get(
        "organization",
        instance.organization if instance else None,
    )

    code = validated_data.get(
        "code",
        instance.code if instance else None,
    )

    start_time = validated_data.get(
        "start_time",
        instance.start_time if instance else None,
    )

    end_time = validated_data.get(
        "end_time",
        instance.end_time if instance else None,
    )

    if start_time and end_time and start_time == end_time:
        raise ValidationError(
            "Shift start time and end time cannot be the same.",
        )

    queryset = Shift.objects.filter(organization=organization, code=code)

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    if queryset.exists():
        raise ValidationError(
            "Shift code already exists in this organization.",
        )


@transaction.atomic
def create_shift(*, validated_data: ShiftData) -> Shift:
    """
    Create a new shift.
    """

    _validate_shift_data(validated_data=validated_data)

    return Shift.objects.create(**validated_data)


@transaction.atomic
def update_shift(*, instance: Shift, validated_data: ShiftData) -> Shift:
    """
    Update an existing shift.
    """

    if not validated_data:
        return instance

    _validate_shift_data(validated_data=validated_data, instance=instance)

    for field, value in validated_data.items():
        setattr(instance, field, value)

    instance.save(update_fields=tuple(validated_data.keys()))

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_shift(*, instance: Shift) -> None:
    """
    Delete a shift.
    """

    instance.delete()


__all__ = [
    "create_shift",
    "update_shift",
    "delete_shift",
]
