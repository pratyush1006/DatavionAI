"""
Billing Core Invoice service.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from django.db import transaction

from apps.billing.exceptions import (
    BillingFinancialInvariantError,
    BillingLifecycleError,
)
from apps.billing.models import Invoice, InvoiceItem


class InvoiceService:
    """Mutate the invoice aggregate transactionally."""

    @staticmethod
    @transaction.atomic
    def create(
        *,
        organization,
        patient,
        data: dict[str, Any],
        items: list[dict[str, Any]],
        performed_by,
    ) -> Invoice:
        """Create an invoice and all line items atomically."""
        if patient.organization_id != organization.pk:
            raise BillingFinancialInvariantError(
                "Patient and organization must match.",
            )

        total = Decimal(
            str(data["total_amount"]),
        )
        calculated = sum(
            (
                Decimal(str(item["quantity"])) * Decimal(str(item["unit_price"]))
                for item in items
            ),
            Decimal("0.00"),
        )

        if items and calculated != total:
            raise BillingFinancialInvariantError(
                "Invoice total must equal line item totals.",
            )

        invoice = Invoice(
            organization=organization,
            patient=patient,
            invoice_number=data["invoice_number"],
            invoice_date=data["invoice_date"],
            due_date=data["due_date"],
            total_amount=total,
            paid_amount=Decimal("0.00"),
            balance_amount=total,
            status=data.get("status", "DRAFT"),
            notes=data.get("notes", ""),
        )
        invoice.full_clean()
        invoice.save()

        for item in items:
            InvoiceItem.objects.create(
                invoice=invoice,
                description=item["description"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                service_code=item.get("service_code", ""),
            )

        return invoice

    @staticmethod
    @transaction.atomic
    def update(
        *,
        invoice: Invoice,
        data: dict[str, Any],
        performed_by,
    ) -> Invoice:
        """Update mutable invoice fields under a row lock."""
        locked = Invoice.objects.select_for_update().get(pk=invoice.pk)

        if locked.status == "VOID":
            raise BillingLifecycleError(
                "A void invoice cannot be updated.",
            )

        for field_name in (
            "invoice_date",
            "due_date",
            "notes",
        ):
            if field_name in data:
                setattr(
                    locked,
                    field_name,
                    data[field_name],
                )

        if "total_amount" in data:
            total = Decimal(
                str(data["total_amount"]),
            )
            if total < locked.paid_amount:
                raise BillingFinancialInvariantError(
                    "Invoice total cannot be lower than paid amount.",
                )
            locked.total_amount = total

        locked.balance_amount = locked.total_amount - locked.paid_amount
        locked.recalculate_status()
        locked.full_clean()
        locked.save()

        return locked

    @staticmethod
    @transaction.atomic
    def void(
        *,
        invoice: Invoice,
        performed_by,
    ) -> Invoice:
        """Void an unpaid invoice."""
        locked = Invoice.objects.select_for_update().get(pk=invoice.pk)

        if locked.paid_amount > Decimal("0.00"):
            raise BillingLifecycleError(
                "An invoice with payments cannot be voided.",
            )

        locked.status = "VOID"
        locked.is_active = False
        locked.full_clean()
        locked.save(
            update_fields=(
                "status",
                "is_active",
                "updated_at",
            ),
        )

        return locked

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        invoice: Invoice,
        performed_by,
    ) -> Invoice:
        """Soft-delete an invoice with no payments."""
        locked = Invoice.objects.select_for_update().get(pk=invoice.pk)

        if locked.paid_amount > Decimal("0.00"):
            raise BillingLifecycleError(
                "An invoice with payments cannot be deleted.",
            )

        locked.delete(
            user_id=performed_by.pk,
        )
        return locked


__all__ = ("InvoiceService",)
