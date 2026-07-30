"""
Payment services.

Business logic layer for DatavionOS SaaS payments.

Responsibilities:

- Create payments
- Process gateway transactions
- Update lifecycle
- Refund payments
- Reconcile invoices
- Maintain accounting records

Architecture:

Invoice
    |
PaymentService
    |
Payment Workflow
    |
Gateway
    |
Reconciliation
"""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.platform.saas_billing.models import (
    Invoice,
    Payment,
)


class PaymentService:
    """
    Enterprise SaaS payment service.
    """

    @staticmethod
    @transaction.atomic
    def create_payment(
        *,
        invoice: Invoice,
        amount: Decimal,
        provider: str = "",
        payment_method: str = "",
        transaction_id: str = "",
        gateway_order_id: str = "",
        gateway_payment_id: str = "",
    ) -> Payment:
        """
        Create payment transaction.
        """

        if amount <= 0:
            raise ValueError(
                "Payment amount must be greater than zero.",
            )

        existing = None

        if transaction_id:
            existing = Payment.objects.filter(
                transaction_id=transaction_id,
            ).first()

        if existing:
            return existing

        return Payment.objects.create(
            tenant=(invoice.tenant),
            organization=(invoice.organization),
            invoice=invoice,
            amount=amount,
            currency=(invoice.currency),
            provider=provider,
            payment_method=payment_method,
            transaction_id=transaction_id,
            gateway_order_id=gateway_order_id,
            gateway_payment_id=gateway_payment_id,
            status=(Payment.Status.PENDING),
        )

    @staticmethod
    @transaction.atomic
    def mark_processing(
        *,
        payment: Payment,
    ) -> Payment:
        """
        Mark payment processing.
        """

        payment.status = Payment.Status.PROCESSING

        payment.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return payment

    @staticmethod
    @transaction.atomic
    def mark_success(
        *,
        payment: Payment,
        gateway_response: dict | None = None,
    ) -> Payment:
        """
        Mark payment successful.
        """

        payment.status = Payment.Status.SUCCESS

        payment.paid_at = timezone.now()

        if gateway_response:
            payment.gateway_response = gateway_response

        payment.save(
            update_fields=[
                "status",
                "paid_at",
                "gateway_response",
                "updated_at",
            ],
        )

        PaymentService._sync_invoice(
            payment=payment,
        )

        return payment

    @staticmethod
    @transaction.atomic
    def mark_failed(
        *,
        payment: Payment,
        reason: str = "",
        gateway_response: dict | None = None,
    ) -> Payment:
        """
        Mark payment failed.
        """

        payment.status = Payment.Status.FAILED

        payment.failed_at = timezone.now()

        payment.failure_reason = reason

        if gateway_response:
            payment.gateway_response = gateway_response

        payment.save(
            update_fields=[
                "status",
                "failed_at",
                "failure_reason",
                "gateway_response",
                "updated_at",
            ],
        )

        return payment

    @staticmethod
    @transaction.atomic
    def refund(
        *,
        payment: Payment,
        amount: Decimal | None = None,
    ) -> Payment:
        """
        Refund payment.

        Supports:

        - Full refund
        - Partial refund
        """

        refund_amount = amount or payment.amount

        if refund_amount <= 0:
            raise ValueError(
                "Refund amount must be positive.",
            )

        if payment.refunded_amount + refund_amount > payment.amount:
            raise ValueError(
                "Refund exceeds payment amount.",
            )

        payment.refunded_amount += refund_amount

        payment.refunded_at = timezone.now()

        if payment.refunded_amount >= payment.amount:
            payment.status = Payment.Status.REFUNDED

        else:
            payment.status = Payment.Status.PARTIALLY_REFUNDED

        payment.save(
            update_fields=[
                "refunded_amount",
                "refunded_at",
                "status",
                "updated_at",
            ],
        )

        return payment

    @staticmethod
    @transaction.atomic
    def reconcile_gateway(
        *,
        payment: Payment,
        response: dict,
    ) -> Payment:
        """
        Store gateway reconciliation.
        """

        payment.gateway_response = response

        payment.reconciliation_data = {
            **payment.reconciliation_data,
            "synced_at": (timezone.now().isoformat()),
            "gateway_status": (
                response.get(
                    "status",
                )
            ),
        }

        payment.save(
            update_fields=[
                "gateway_response",
                "reconciliation_data",
                "updated_at",
            ],
        )

        return payment

    @staticmethod
    @transaction.atomic
    def _sync_invoice(
        *,
        payment: Payment,
    ) -> Invoice:
        """
        Synchronize invoice payment state.
        """

        invoice = payment.invoice

        paid_amount = sum(
            invoice.payments.filter(
                status=Payment.Status.SUCCESS,
            ).values_list(
                "amount",
                flat=True,
            ),
            Decimal("0"),
        )

        invoice.paid_amount = paid_amount

        if paid_amount >= invoice.total_amount:
            invoice.status = Invoice.Status.PAID

            invoice.paid_at = timezone.now()

        elif paid_amount > 0:
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
    def successful_amount(
        *,
        organization,
    ) -> Decimal:
        """
        Calculate successful revenue.
        """

        return sum(
            Payment.objects.filter(
                organization=organization,
                status=Payment.Status.SUCCESS,
            ).values_list(
                "amount",
                flat=True,
            ),
            Decimal("0"),
        )


__all__ = [
    "PaymentService",
]
