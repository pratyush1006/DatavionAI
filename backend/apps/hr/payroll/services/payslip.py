"""
Business services for payslips.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.hr.payroll.constants import PayslipStatus
from apps.hr.payroll.models import (
    Payslip,
    PayslipLineItem,
    PayslipLineItemType,
)

type PayslipData = Mapping[str, object]


def _compute_totals(
    *,
    basic_salary,
    line_items: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    """
    Compute payslip totals from its basic salary and line items.
    """

    total_earnings = basic_salary or 0
    total_deductions = 0

    for item in line_items:
        amount = item["amount"]

        if item["component_type"] == PayslipLineItemType.EARNING:
            total_earnings += amount
        else:
            total_deductions += amount

    return {
        "total_earnings": total_earnings,
        "total_deductions": total_deductions,
        "net_pay": total_earnings - total_deductions,
    }


@transaction.atomic
def create_payslip(
    *,
    validated_data: PayslipData,
) -> Payslip:
    """
    Create a payslip along with its earning and deduction line
    items, computing the payslip's totals.
    """

    data = dict(validated_data)

    line_items = data.pop("line_items", [])

    employee = data.get("employee")
    organization = data.get("organization")

    if employee and organization and employee.organization_id != organization.id:
        raise ValidationError(
            "Employee must belong to the selected organization.",
        )

    pay_period_start = data.get("pay_period_start")
    pay_period_end = data.get("pay_period_end")

    if pay_period_start and pay_period_end and pay_period_end < pay_period_start:
        raise ValidationError(
            "Pay period end date must be on or after the start date.",
        )

    totals = _compute_totals(
        basic_salary=data.get("basic_salary", 0),
        line_items=line_items,
    )

    payslip = Payslip.objects.create(
        **data,
        **totals,
    )

    PayslipLineItem.objects.bulk_create(
        [
            PayslipLineItem(
                payslip=payslip,
                **item,
            )
            for item in line_items
        ],
    )

    return payslip


@transaction.atomic
def update_payslip(
    *,
    instance: Payslip,
    validated_data: PayslipData,
) -> Payslip:
    """
    Update a payslip's editable fields. Once processed or paid,
    a payslip can no longer be edited.
    """

    if not validated_data:
        return instance

    if instance.status in (
        PayslipStatus.PROCESSED,
        PayslipStatus.PAID,
    ):
        raise ValidationError(
            "Processed or paid payslips can no longer be edited.",
        )

    data = dict(validated_data)

    line_items = data.pop(
        "line_items",
        None,
    )

    for field, value in data.items():
        setattr(instance, field, value)

    if line_items is not None:
        instance.line_items.all().delete()

        PayslipLineItem.objects.bulk_create(
            [
                PayslipLineItem(
                    payslip=instance,
                    **item,
                )
                for item in line_items
            ],
        )

        totals = _compute_totals(
            basic_salary=data.get(
                "basic_salary",
                instance.basic_salary,
            ),
            line_items=line_items,
        )

        for field, value in totals.items():
            setattr(instance, field, value)

    instance.save()

    instance.refresh_from_db()

    return instance


@transaction.atomic
def mark_payslip_processed(
    *,
    instance: Payslip,
) -> Payslip:
    """
    Mark a draft payslip as processed.
    """

    if instance.status != PayslipStatus.DRAFT:
        raise ValidationError(
            "Only draft payslips can be marked as processed.",
        )

    instance.status = PayslipStatus.PROCESSED

    instance.save(update_fields=["status"])

    return instance


@transaction.atomic
def mark_payslip_paid(
    *,
    instance: Payslip,
) -> Payslip:
    """
    Mark a processed payslip as paid.
    """

    if instance.status != PayslipStatus.PROCESSED:
        raise ValidationError(
            "Only processed payslips can be marked as paid.",
        )

    instance.status = PayslipStatus.PAID
    instance.paid_on = timezone.now().date()

    instance.save(update_fields=["status", "paid_on"])

    return instance


@transaction.atomic
def delete_payslip(*, instance: Payslip) -> None:
    """
    Delete a payslip.
    """

    instance.delete()


__all__ = [
    "create_payslip",
    "update_payslip",
    "mark_payslip_processed",
    "mark_payslip_paid",
    "delete_payslip",
]
