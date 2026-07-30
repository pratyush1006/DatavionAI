"""
Payment selectors.

Read-only query layer for DatavionOS
SaaS payment management.

Responsibilities:

- Organization payment lookup
- Invoice payment lookup
- Successful payments
- Failed payments
- Refund tracking
- Gateway transaction queries
- Revenue reporting support

Architecture:

API
 |
Selectors
 |
Models
"""

from __future__ import annotations

from apps.platform.saas_billing.models import (
    Payment,
)


class PaymentSelector:
    """
    Payment read operations.
    """

    @staticmethod
    def get_by_id(
        *,
        payment_id,
    ) -> Payment | None:
        """
        Retrieve payment by ID.
        """

        return (
            Payment.objects.filter(
                id=payment_id,
            )
            .select_related(
                "organization",
                "invoice",
            )
            .first()
        )

    @staticmethod
    def by_organization(
        *,
        organization,
    ):
        """
        Return organization payments.
        """

        return (
            Payment.objects.by_organization(
                organization,
            )
            .select_related(
                "invoice",
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def by_invoice(
        *,
        invoice,
    ):
        """
        Return invoice payments.
        """

        return Payment.objects.by_invoice(
            invoice,
        ).select_related(
            "organization",
        )

    @staticmethod
    def successful(
        *,
        organization=None,
    ):
        """
        Return successful payments.
        """

        queryset = Payment.objects.successful()

        if organization:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset

    @staticmethod
    def failed(
        *,
        organization=None,
    ):
        """
        Return failed payments.
        """

        queryset = Payment.objects.failed()

        if organization:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset

    @staticmethod
    def refunded(
        *,
        organization=None,
    ):
        """
        Return refunded payments.
        """

        queryset = Payment.objects.refunded()

        if organization:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset

    @staticmethod
    def pending():
        """
        Return pending payments.
        """

        return Payment.objects.pending()

    @staticmethod
    def by_provider(
        *,
        provider: str,
    ):
        """
        Return gateway specific payments.

        Example:

        STRIPE
        RAZORPAY
        PAYPAL
        BANK
        """

        return Payment.objects.by_provider(
            provider,
        )

    @staticmethod
    def get_by_transaction_id(
        *,
        transaction_id: str,
    ) -> Payment | None:
        """
        Retrieve payment by external transaction.
        """

        return Payment.objects.filter(
            transaction_id=transaction_id,
        ).first()

    @staticmethod
    def get_by_gateway_payment_id(
        *,
        gateway_payment_id: str,
    ) -> Payment | None:
        """
        Retrieve payment by gateway ID.
        """

        return Payment.objects.filter(
            gateway_payment_id=(gateway_payment_id),
        ).first()

    @staticmethod
    def revenue_queryset(
        *,
        organization=None,
    ):
        """
        Return successful payments
        for revenue analytics.
        """

        queryset = Payment.objects.revenue()

        if organization:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset


__all__ = [
    "PaymentSelector",
]
