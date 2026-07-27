"""
Business services for the Attendance app.
"""

from __future__ import annotations

import datetime
from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.hr.attendance.models import AttendanceRecord

type AttendanceData = Mapping[str, object]


def _compute_hours_worked(
    *,
    check_in: datetime.time | None,
    check_out: datetime.time | None,
) -> float | None:
    """
    Compute hours worked from check-in and check-out times.
    """

    if not check_in or not check_out:
        return None

    today = datetime.date.today()

    delta = datetime.datetime.combine(
        today,
        check_out,
    ) - datetime.datetime.combine(
        today,
        check_in,
    )

    if delta.total_seconds() < 0:
        raise ValidationError(
            "Check-out time must be after check-in time.",
        )

    return round(
        delta.total_seconds() / 3600,
        2,
    )


def _validate_attendance_data(
    *,
    validated_data: AttendanceData,
    instance: AttendanceRecord | None = None,
) -> None:
    """
    Validate attendance business rules.
    """

    employee = validated_data.get(
        "employee",
        instance.employee if instance else None,
    )

    organization = validated_data.get(
        "organization",
        instance.organization if instance else None,
    )

    work_date = validated_data.get(
        "work_date",
        instance.work_date if instance else None,
    )

    if employee and organization and employee.organization_id != organization.id:
        raise ValidationError(
            "Employee must belong to the selected organization.",
        )

    queryset = AttendanceRecord.objects.filter(
        employee=employee,
        work_date=work_date,
    )

    if instance:
        queryset = queryset.exclude(
            pk=instance.pk,
        )

    if queryset.exists():
        raise ValidationError(
            "An attendance record already exists for this employee on this date.",
        )


@transaction.atomic
def create_attendance_record(
    *,
    validated_data: AttendanceData,
) -> AttendanceRecord:
    """
    Create a new attendance record.
    """

    _validate_attendance_data(
        validated_data=validated_data,
    )

    data = dict(validated_data)

    data["hours_worked"] = _compute_hours_worked(
        check_in=data.get("check_in"),
        check_out=data.get("check_out"),
    )

    return AttendanceRecord.objects.create(
        **data,
    )


@transaction.atomic
def update_attendance_record(
    *,
    instance: AttendanceRecord,
    validated_data: AttendanceData,
) -> AttendanceRecord:
    """
    Update an existing attendance record.
    """

    if not validated_data:
        return instance

    _validate_attendance_data(
        validated_data=validated_data,
        instance=instance,
    )

    data = dict(validated_data)

    check_in = data.get(
        "check_in",
        instance.check_in,
    )

    check_out = data.get(
        "check_out",
        instance.check_out,
    )

    data["hours_worked"] = _compute_hours_worked(
        check_in=check_in,
        check_out=check_out,
    )

    for field, value in data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save(
        update_fields=tuple(data.keys()),
    )

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_attendance_record(
    *,
    instance: AttendanceRecord,
) -> None:
    """
    Delete an attendance record.
    """

    instance.delete()


__all__ = [
    "create_attendance_record",
    "update_attendance_record",
    "delete_attendance_record",
]
