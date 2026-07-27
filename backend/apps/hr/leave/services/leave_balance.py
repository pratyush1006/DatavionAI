"""
Business services for leave balances.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.hr.leave.models import LeaveBalance

type LeaveBalanceData = Mapping[str, object]


def _validate_leave_balance_data(
    *,
    validated_data: LeaveBalanceData,
    instance: LeaveBalance | None = None,
) -> None:
    """
    Validate leave balance business rules.
    """

    employee = validated_data.get(
        "employee",
        instance.employee if instance else None,
    )

    leave_type = validated_data.get(
        "leave_type",
        instance.leave_type if instance else None,
    )

    year = validated_data.get(
        "year",
        instance.year if instance else None,
    )

    if (
        employee
        and leave_type
        and employee.organization_id != leave_type.organization_id
    ):
        raise ValidationError(
            "Leave type does not belong to the employee's organization.",
        )

    queryset = LeaveBalance.objects.filter(
        employee=employee,
        leave_type=leave_type,
        year=year,
    )

    if instance:
        queryset = queryset.exclude(
            pk=instance.pk,
        )

    if queryset.exists():
        raise ValidationError(
            "A leave balance already exists for this employee, leave type and year.",
        )


@transaction.atomic
def create_leave_balance(
    *,
    validated_data: LeaveBalanceData,
) -> LeaveBalance:
    """
    Create a new leave balance.
    """

    _validate_leave_balance_data(
        validated_data=validated_data,
    )

    return LeaveBalance.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_leave_balance(
    *,
    instance: LeaveBalance,
    validated_data: LeaveBalanceData,
) -> LeaveBalance:
    """
    Update an existing leave balance.
    """

    if not validated_data:
        return instance

    _validate_leave_balance_data(
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
def delete_leave_balance(
    *,
    instance: LeaveBalance,
) -> None:
    """
    Delete a leave balance.
    """

    instance.delete()


__all__ = [
    "create_leave_balance",
    "update_leave_balance",
    "delete_leave_balance",
]
