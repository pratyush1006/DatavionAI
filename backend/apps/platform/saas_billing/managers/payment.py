"""
Payment managers.

Provides reusable queryset operations
for DatavionOS SaaS payment lifecycle.

Responsibilities:

- Payment lifecycle management
- Provider tracking
- Invoice payment queries
- Refund workflows
- Gateway reconciliation
- Revenue reporting
"""

from __future__ import annotations

from django.db import models


class PaymentQuerySet(
    models.QuerySet,
):
    """
    Payment queryset helpers.
    """

    # --------------------------------------------------------------
    # Status
    # --------------------------------------------------------------

    def pending(
        self,
    ):
        """
        Return pending payments.
        """

        return self.filter(
            status="PENDING",
        )

    def processing(
        self,
    ):
        """
        Return processing payments.
        """

        return self.filter(
            status="PROCESSING",
        )

    def successful(
        self,
    ):
        """
        Return successful payments.
        """

        return self.filter(
            status="SUCCESS",
        )

    def failed(
        self,
    ):
        """
        Return failed payments.
        """

        return self.filter(
            status="FAILED",
        )

    def cancelled(
        self,
    ):
        """
        Return cancelled payments.
        """

        return self.filter(
            status="CANCELLED",
        )

    def refunded(
        self,
    ):
        """
        Return refunded payments.
        """

        return self.filter(
            status="REFUNDED",
        )

    def partially_refunded(
        self,
    ):
        """
        Return partially refunded payments.
        """

        return self.filter(
            status="PARTIALLY_REFUNDED",
        )

    # --------------------------------------------------------------
    # Ownership
    # --------------------------------------------------------------

    def by_tenant(
        self,
        tenant,
    ):
        """
        Filter tenant payments.
        """

        return self.filter(
            tenant=tenant,
        )

    def by_organization(
        self,
        organization,
    ):
        """
        Filter organization payments.
        """

        return self.filter(
            organization=organization,
        )

    def by_invoice(
        self,
        invoice,
    ):
        """
        Filter invoice payments.
        """

        return self.filter(
            invoice=invoice,
        )

    # --------------------------------------------------------------
    # Provider
    # --------------------------------------------------------------

    def by_provider(
        self,
        provider: str,
    ):
        """
        Filter payment provider.
        """

        return self.filter(
            provider=provider,
        )

    def gateway_payments(
        self,
    ):
        """
        Return payments processed
        through gateways.
        """

        return self.exclude(
            gateway_payment_id="",
        ).exclude(
            gateway_payment_id__isnull=True,
        )

    def bank_payments(
        self,
    ):
        """
        Return bank transfer payments.
        """

        return self.filter(
            provider="BANK",
        )

    # --------------------------------------------------------------
    # Transaction
    # --------------------------------------------------------------

    def by_transaction(
        self,
        transaction_id: str,
    ):
        """
        Find transaction.
        """

        return self.filter(
            transaction_id=transaction_id,
        )

    def by_gateway_payment_id(
        self,
        gateway_payment_id: str,
    ):
        """
        Find gateway payment.
        """

        return self.filter(
            gateway_payment_id=gateway_payment_id,
        )

    # --------------------------------------------------------------
    # Payment Processing
    # --------------------------------------------------------------

    def completed(
        self,
    ):
        """
        Completed successful payments.
        """

        return self.filter(
            status="SUCCESS",
            paid_at__isnull=False,
        )

    def failed_retry_candidates(
        self,
    ):
        """
        Payments eligible for retry.
        """

        return self.filter(
            status="FAILED",
        )

    # --------------------------------------------------------------
    # Revenue
    # --------------------------------------------------------------

    def revenue(
        self,
    ):
        """
        Payments counted as revenue.
        """

        return self.filter(
            status__in=[
                "SUCCESS",
                "PARTIALLY_REFUNDED",
            ],
        )

    def refundable(
        self,
    ):
        """
        Payments having refundable amount.
        """

        return self.filter(
            status="SUCCESS",
        ).filter(
            amount__gt=models.F(
                "refunded_amount",
            ),
        )

    # --------------------------------------------------------------
    # Reporting
    # --------------------------------------------------------------

    def recent(
        self,
        limit: int = 10,
    ):
        """
        Return latest payments.
        """

        return self.order_by(
            "-created_at",
        )[:limit]


class PaymentManager(
    models.Manager,
):
    """
    Manager for Payment model.
    """

    def get_queryset(
        self,
    ):
        return PaymentQuerySet(
            self.model,
            using=self._db,
        )

    def latest_for_invoice(
        self,
        invoice,
    ):
        """
        Return latest invoice payment.
        """

        return (
            self.get_queryset()
            .by_invoice(
                invoice,
            )
            .order_by(
                "-created_at",
            )
            .first()
        )


__all__ = [
    "PaymentManager",
    "PaymentQuerySet",
]
