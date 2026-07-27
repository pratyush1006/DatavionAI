"""
Business services for leave types.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.hr.leave.models import LeaveType

type LeaveTypeData = Mapping[str, object]


def _validate_leave_type_data(
    *,
    validated_data: LeaveTypeData,
    instance: LeaveType | None = None,
) -> None:
    """
    Validate leave type business rules.
    """

    organization = validated_data.get(
        "organization",
        instance.organization if instance else None,
    )

    code = validated_data.get(
        "code",
        instance.code if instance else None,
    )

    queryset = LeaveType.objects.filter(
        organization=organization,
        code=code,
    )

    if instance:
        queryset = queryset.exclude(
            pk=instance.pk,
        )

    if queryset.exists():
        raise ValidationError(
            "Leave type code already exists in this organization.",
        )


@transaction.atomic
def create_leave_type(
    *,
    validated_data: LeaveTypeData,
) -> LeaveType:
    """
    Create a new leave type.
    """

    _validate_leave_type_data(
        validated_data=validated_data,
    )

    return LeaveType.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_leave_type(
    *,
    instance: LeaveType,
    validated_data: LeaveTypeData,
) -> LeaveType:
    """
    Update an existing leave type.
    """

    if not validated_data:
        return instance

    _validate_leave_type_data(
        validated_data=validated_data,
        instance=instance,
    )

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save(
        update_fields=tuple(validated_data.keys()),
    )

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_leave_type(
    *,
    instance: LeaveType,
) -> None:
    """
    Delete a leave type.
    """

    instance.delete()


__all__ = [
    "create_leave_type",
    "update_leave_type",
    "delete_leave_type",
]
