"""
Business services for holidays.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.hr.holidays.models import Holiday

type HolidayData = Mapping[str, object]


def _validate_holiday_data(
    *,
    validated_data: HolidayData,
    instance: Holiday | None = None,
) -> None:
    """
    Validate holiday business rules.
    """

    organization = validated_data.get(
        "organization",
        instance.organization if instance else None,
    )

    date = validated_data.get(
        "date",
        instance.date if instance else None,
    )

    name = validated_data.get(
        "name",
        instance.name if instance else None,
    )

    queryset = Holiday.objects.filter(
        organization=organization,
        date=date,
        name=name,
    )

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    if queryset.exists():
        raise ValidationError(
            "This holiday already exists on this date for this organization.",
        )


@transaction.atomic
def create_holiday(*, validated_data: HolidayData) -> Holiday:
    """
    Create a new holiday.
    """

    _validate_holiday_data(validated_data=validated_data)

    return Holiday.objects.create(**validated_data)


@transaction.atomic
def update_holiday(
    *,
    instance: Holiday,
    validated_data: HolidayData,
) -> Holiday:
    """
    Update an existing holiday.
    """

    if not validated_data:
        return instance

    _validate_holiday_data(
        validated_data=validated_data,
        instance=instance,
    )

    for field, value in validated_data.items():
        setattr(instance, field, value)

    instance.save(update_fields=tuple(validated_data.keys()))

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_holiday(*, instance: Holiday) -> None:
    """
    Delete a holiday.
    """

    instance.delete()


@transaction.atomic
def apply_holiday_to_attendance(
    *,
    instance: Holiday,
) -> int:
    """
    Mark every active employee in the holiday's organization as
    on holiday in the attendance records for this holiday's
    date, creating a record where one does not already exist.

    Returns the number of attendance records created or updated.
    """

    from apps.hr.attendance.constants import AttendanceStatus
    from apps.hr.attendance.models import AttendanceRecord
    from apps.organization.employees.models import Employee

    employees = Employee.objects.filter(
        organization=instance.organization,
        is_active=True,
    )

    affected = 0

    for employee in employees:
        _, created = AttendanceRecord.objects.update_or_create(
            employee=employee,
            work_date=instance.date,
            defaults={
                "organization": instance.organization,
                "status": AttendanceStatus.HOLIDAY,
            },
        )

        affected += 1

    return affected


__all__ = [
    "create_holiday",
    "update_holiday",
    "delete_holiday",
    "apply_holiday_to_attendance",
]
