"""
Invoice services.

Business logic layer for DatavionOS SaaS invoices.

Responsibilities:

- Generate invoices
- Calculate totals
- Apply taxes
- Manage invoice lifecycle
- Handle payment readiness
- Support subscription and usage billing

Architecture:

Subscription
      |
InvoiceService
      |
Invoice Workflow
      |
Invoice Model
      |
Payment
      |
Accounting
"""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.platform.saas_billing.models import (
    Invoice,
    Subscription,
)


class InvoiceService:
    """
    Enterprise SaaS invoice service.
    """

    @staticmethod
    def generate_invoice_number() -> str:
        """
        Generate unique invoice number.
        """

        timestamp = timezone.now()

        return f"DATAVION-{timestamp.strftime('%Y%m%d%H%M%S%f')}"

    @staticmethod
    def calculate_tax(
        *,
        amount: Decimal,
        tax_rate: Decimal = Decimal("0"),
    ) -> Decimal:
        """
        Calculate GST/VAT amount.
        """

        return amount * tax_rate / Decimal("100")

    @staticmethod
    @transaction.atomic
    def create_subscription_invoice(
        *,
        subscription: Subscription,
    ) -> Invoice:
        """
        Create subscription invoice.

        Used during:

        - Activation
        - Renewal
        - Billing cycle execution
        """

        existing = Invoice.objects.filter(
            subscription=subscription,
            status__in=[
                Invoice.Status.DRAFT,
                Invoice.Status.ISSUED,
            ],
            billing_period_start=(subscription.current_period_start),
        ).first()

        if existing:
            return existing

        plan = subscription.plan

        subtotal = plan.price

        tax_amount = Decimal(
            "0",
        )

        total_amount = subtotal + tax_amount

        return Invoice.objects.create(
            tenant=(subscription.tenant),
            organization=(subscription.organization),
            subscription=subscription,
            invoice_number=(InvoiceService.generate_invoice_number()),
            invoice_type=(Invoice.InvoiceType.SUBSCRIPTION),
            status=(Invoice.Status.DRAFT),
            billing_period_start=(subscription.current_period_start),
            billing_period_end=(subscription.current_period_end),
            subtotal=subtotal,
            tax_amount=tax_amount,
            discount_amount=Decimal(
                "0",
            ),
            total_amount=total_amount,
            currency=(plan.currency),
            invoice_data={
                "type": "subscription",
                "plan": {
                    "id": str(
                        plan.id,
                    ),
                    "name": plan.name,
                    "code": plan.code,
                    "price": str(
                        plan.price,
                    ),
                },
                "subscription": {
                    "id": str(
                        subscription.id,
                    ),
                },
            },
        )

    @staticmethod
    @transaction.atomic
    def issue_invoice(
        *,
        invoice: Invoice,
    ) -> Invoice:
        """
        Issue invoice.
        """

        if invoice.status != Invoice.Status.DRAFT:
            return invoice

        invoice.status = Invoice.Status.ISSUED

        invoice.issued_at = timezone.now()

        invoice.save(
            update_fields=[
                "status",
                "issued_at",
                "updated_at",
            ],
        )

        return invoice

    @staticmethod
    @transaction.atomic
    def mark_sent(
        *,
        invoice: Invoice,
    ) -> Invoice:
        """
        Mark invoice sent.
        """

        invoice.status = Invoice.Status.SENT

        invoice.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return invoice

    @staticmethod
    @transaction.atomic
    def mark_paid(
        *,
        invoice: Invoice,
        payment_reference: str = "",
    ) -> Invoice:
        """
        Mark invoice fully paid.
        """

        invoice.status = Invoice.Status.PAID

        invoice.paid_amount = invoice.total_amount

        invoice.paid_at = timezone.now()

        if payment_reference:
            invoice.payment_reference = payment_reference

        invoice.save(
            update_fields=[
                "status",
                "paid_amount",
                "paid_at",
                "payment_reference",
                "updated_at",
            ],
        )

        return invoice

    @staticmethod
    @transaction.atomic
    def add_payment(
        *,
        invoice: Invoice,
        amount: Decimal,
    ) -> Invoice:
        """
        Add partial payment.
        """

        invoice.paid_amount += amount

        if invoice.paid_amount >= invoice.total_amount:
            invoice.status = Invoice.Status.PAID

            invoice.paid_at = timezone.now()

        else:
            invoice.status = Invoice.Status.PARTIALLY_PAID

        invoice.save(
            update_fields=[
                "paid_amount",
                "status",
                "paid_at",
                "updated_at",
            ],
        )

        return invoice

    @staticmethod
    @transaction.atomic
    def cancel_invoice(
        *,
        invoice: Invoice,
    ) -> Invoice:
        """
        Cancel invoice.
        """

        invoice.status = Invoice.Status.CANCELLED

        invoice.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return invoice

    @staticmethod
    @transaction.atomic
    def refund_invoice(
        *,
        invoice: Invoice,
    ) -> Invoice:
        """
        Refund invoice.
        """

        invoice.status = Invoice.Status.REFUNDED

        invoice.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return invoice

    @staticmethod
    def is_paid(
        *,
        invoice: Invoice,
    ) -> bool:
        """
        Check payment completion.
        """

        return invoice.status == Invoice.Status.PAID

    @staticmethod
    def outstanding_amount(
        *,
        invoice: Invoice,
    ) -> Decimal:
        """
        Calculate outstanding balance.
        """

        return invoice.total_amount - invoice.paid_amount


__all__ = [
    "InvoiceService",
]
