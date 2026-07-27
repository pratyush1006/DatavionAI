"""
Business services for shift assignments.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.hr.shifts.models import ShiftAssignment

type ShiftAssignmentData = Mapping[str, object]


def _validate_shift_assignment_data(
    *,
    validated_data: ShiftAssignmentData,
    instance: ShiftAssignment | None = None,
) -> None:
    """
    Validate shift assignment business rules.
    """

    employee = validated_data.get(
        "employee",
        instance.employee if instance else None,
    )

    organization = validated_data.get(
        "organization",
        instance.organization if instance else None,
    )

    shift = validated_data.get(
        "shift",
        instance.shift if instance else None,
    )

    work_date = validated_data.get(
        "work_date",
        instance.work_date if instance else None,
    )

    if employee and organization and employee.organization_id != organization.id:
        raise ValidationError(
            "Employee must belong to the selected organization.",
        )

    if shift and organization and shift.organization_id != organization.id:
        raise ValidationError(
            "Shift must belong to the selected organization.",
        )

    queryset = ShiftAssignment.objects.filter(
        employee=employee,
        work_date=work_date,
    )

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    if queryset.exists():
        raise ValidationError(
            "A shift assignment already exists for this employee on this date.",
        )


@transaction.atomic
def create_shift_assignment(
    *,
    validated_data: ShiftAssignmentData,
) -> ShiftAssignment:
    """
    Create a new shift assignment.
    """

    _validate_shift_assignment_data(validated_data=validated_data)

    return ShiftAssignment.objects.create(**validated_data)


@transaction.atomic
def update_shift_assignment(
    *,
    instance: ShiftAssignment,
    validated_data: ShiftAssignmentData,
) -> ShiftAssignment:
    """
    Update an existing shift assignment.
    """

    if not validated_data:
        return instance

    _validate_shift_assignment_data(
        validated_data=validated_data,
        instance=instance,
    )

    for field, value in validated_data.items():
        setattr(instance, field, value)

    instance.save(update_fields=tuple(validated_data.keys()))

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_shift_assignment(*, instance: ShiftAssignment) -> None:
    """
    Delete a shift assignment.
    """

    instance.delete()


__all__ = [
    "create_shift_assignment",
    "update_shift_assignment",
    "delete_shift_assignment",
]
