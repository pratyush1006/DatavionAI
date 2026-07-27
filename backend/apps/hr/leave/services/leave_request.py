"""
Business services for leave requests.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.hr.leave.constants import LeaveRequestStatus
from apps.hr.leave.models import LeaveBalance, LeaveRequest

type LeaveRequestData = Mapping[str, object]


def _validate_leave_request_data(
    *,
    validated_data: LeaveRequestData,
    instance: LeaveRequest | None = None,
) -> None:
    """
    Validate leave request business rules.
    """

    employee = validated_data.get(
        "employee",
        instance.employee if instance else None,
    )

    organization = validated_data.get(
        "organization",
        instance.organization if instance else None,
    )

    leave_type = validated_data.get(
        "leave_type",
        instance.leave_type if instance else None,
    )

    start_date = validated_data.get(
        "start_date",
        instance.start_date if instance else None,
    )

    end_date = validated_data.get(
        "end_date",
        instance.end_date if instance else None,
    )

    if employee and organization and employee.organization_id != organization.id:
        raise ValidationError(
            "Employee must belong to the selected organization.",
        )

    if leave_type and organization and leave_type.organization_id != organization.id:
        raise ValidationError(
            "Leave type must belong to the selected organization.",
        )

    if start_date and end_date and end_date < start_date:
        raise ValidationError(
            "End date must be on or after the start date.",
        )


@transaction.atomic
def create_leave_request(
    *,
    validated_data: LeaveRequestData,
) -> LeaveRequest:
    """
    Create a new leave request.
    """

    _validate_leave_request_data(
        validated_data=validated_data,
    )

    return LeaveRequest.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_leave_request(
    *,
    instance: LeaveRequest,
    validated_data: LeaveRequestData,
) -> LeaveRequest:
    """
    Update an existing leave request.
    """

    if not validated_data:
        return instance

    if instance.status != LeaveRequestStatus.PENDING:
        raise ValidationError(
            "Only pending leave requests can be updated.",
        )

    _validate_leave_request_data(
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
def decide_leave_request(
    *,
    instance: LeaveRequest,
    approver,
    approve: bool,
    decision_notes: str = "",
) -> LeaveRequest:
    """
    Approve or reject a pending leave request.

    Approving a request debits the matching leave balance for
    the year of the request's start date, creating one with a
    zero allocation if it does not yet exist.
    """

    if instance.status != LeaveRequestStatus.PENDING:
        raise ValidationError(
            "Only pending leave requests can be approved or rejected.",
        )

    if approve:
        balance, _ = LeaveBalance.objects.get_or_create(
            employee=instance.employee,
            leave_type=instance.leave_type,
            year=instance.start_date.year,
        )

        balance.used_days = balance.used_days + instance.number_of_days
        balance.save(
            update_fields=[
                "used_days",
            ],
        )

        instance.status = LeaveRequestStatus.APPROVED

    else:
        instance.status = LeaveRequestStatus.REJECTED

    instance.approver = approver
    instance.decision_notes = decision_notes
    instance.decided_at = timezone.now()

    instance.save(
        update_fields=[
            "status",
            "approver",
            "decision_notes",
            "decided_at",
        ],
    )

    instance.refresh_from_db()

    return instance


@transaction.atomic
def cancel_leave_request(
    *,
    instance: LeaveRequest,
) -> LeaveRequest:
    """
    Cancel a leave request, reversing any balance debit if it
    had already been approved.
    """

    if instance.status == LeaveRequestStatus.CANCELLED:
        return instance

    if instance.status == LeaveRequestStatus.APPROVED:
        balance = LeaveBalance.objects.filter(
            employee=instance.employee,
            leave_type=instance.leave_type,
            year=instance.start_date.year,
        ).first()

        if balance is not None:
            balance.used_days = max(
                balance.used_days - instance.number_of_days,
                0,
            )
            balance.save(
                update_fields=[
                    "used_days",
                ],
            )

    instance.status = LeaveRequestStatus.CANCELLED

    instance.save(
        update_fields=[
            "status",
        ],
    )

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_leave_request(
    *,
    instance: LeaveRequest,
) -> None:
    """
    Delete a leave request.
    """

    instance.delete()


__all__ = [
    "create_leave_request",
    "update_leave_request",
    "decide_leave_request",
    "cancel_leave_request",
    "delete_leave_request",
]
