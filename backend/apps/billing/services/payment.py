"""
Billing Core Payment service.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction

from apps.billing.exceptions import BillingFinancialInvariantError
from apps.billing.models import Invoice, Payment


class PaymentService:
    """Record payments with invoice row-level concurrency control."""

    @staticmethod
    @transaction.atomic
    def create(
        *,
        organization,
        patient,
        data,
        performed_by,
    ) -> Payment:
        """Create a payment and update the invoice atomically."""
        invoice = (
            Invoice.objects.select_for_update()
            .select_related("patient", "organization")
            .get(
                pk=data["invoice_id"],
                organization_id=organization.pk,
            )
        )

        if invoice.patient_id != patient.pk:
            raise BillingFinancialInvariantError(
                "Payment patient must match invoice patient.",
            )

        amount = Decimal(
            str(data["amount"]),
        )

        if amount <= Decimal("0.00"):
            raise BillingFinancialInvariantError(
                "Payment amount must be greater than zero.",
            )

        if amount > invoice.balance_amount:
            raise BillingFinancialInvariantError(
                "Payment cannot exceed invoice balance.",
            )

        payment = Payment(
            organization=organization,
            invoice=invoice,
            patient=patient,
            payment_method=data["payment_method"],
            amount=amount,
            payment_date=data["payment_date"],
            reference_number=data.get("reference_number", ""),
            notes=data.get("notes", ""),
            received_by=performed_by,
        )
        payment.full_clean()
        payment.save()

        invoice.paid_amount += amount
        invoice.balance_amount = invoice.total_amount - invoice.paid_amount
        invoice.recalculate_status()
        invoice.full_clean()
        invoice.save(
            update_fields=(
                "paid_amount",
                "balance_amount",
                "status",
                "updated_at",
            ),
        )

        return payment


__all__ = ("PaymentService",)
