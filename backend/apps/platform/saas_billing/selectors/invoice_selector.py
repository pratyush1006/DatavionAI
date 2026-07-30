"""
Invoice selectors.

Read-only query layer for DatavionOS
SaaS invoice management.

Responsibilities:

- Organization invoice lookup
- Subscription invoice lookup
- Payment status queries
- Outstanding invoices
- Overdue invoices
- Revenue reporting support

Architecture:

API
 |
Selectors
 |
Models
"""

from __future__ import annotations

from django.utils import timezone

from apps.platform.saas_billing.models import (
    Invoice,
)


class InvoiceSelector:
    """
    Invoice read operations.
    """

    @staticmethod
    def get_by_id(
        *,
        invoice_id,
    ) -> Invoice | None:
        """
        Retrieve invoice by ID.
        """

        return (
            Invoice.objects.filter(
                id=invoice_id,
            )
            .select_related(
                "organization",
                "subscription",
            )
            .first()
        )

    @staticmethod
    def get_by_number(
        *,
        invoice_number: str,
    ) -> Invoice | None:
        """
        Retrieve invoice by invoice number.
        """

        return Invoice.objects.filter(
            invoice_number=invoice_number,
        ).first()

    @staticmethod
    def by_organization(
        *,
        organization,
    ):
        """
        Return organization invoices.
        """

        return (
            Invoice.objects.by_organization(
                organization,
            )
            .select_related(
                "subscription",
                "organization",
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def by_subscription(
        *,
        subscription,
    ):
        """
        Return subscription invoices.
        """

        return Invoice.objects.by_subscription(
            subscription,
        ).select_related(
            "organization",
        )

    @staticmethod
    def draft_invoices():
        """
        Return draft invoices.
        """

        return Invoice.objects.drafts()

    @staticmethod
    def issued_invoices():
        """
        Return issued invoices.
        """

        return Invoice.objects.issued()

    @staticmethod
    def paid_invoices(
        *,
        organization=None,
    ):
        """
        Return paid invoices.
        """

        queryset = Invoice.objects.paid()

        if organization:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset

    @staticmethod
    def outstanding_invoices(
        *,
        organization=None,
    ):
        """
        Return unpaid invoices.
        """

        queryset = Invoice.objects.outstanding()

        if organization:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset

    @staticmethod
    def overdue_invoices(
        *,
        organization=None,
    ):
        """
        Return overdue invoices.
        """

        queryset = Invoice.objects.overdue(
            timezone.now(),
        )

        if organization:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset

    @staticmethod
    def recent_invoices(
        *,
        limit: int = 10,
    ):
        """
        Return recent invoices.
        """

        return Invoice.objects.recent(
            limit,
        )

    @staticmethod
    def total_revenue(
        *,
        organization=None,
    ):
        """
        Return paid invoice amount.
        """

        queryset = Invoice.objects.paid()

        if organization:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset


__all__ = [
    "InvoiceSelector",
]
