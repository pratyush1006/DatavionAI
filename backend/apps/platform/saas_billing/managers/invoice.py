"""
Invoice managers.

Provides reusable queryset operations
for DatavionOS SaaS invoice lifecycle.

Responsibilities:

- Organization invoice filtering
- Tenant invoice filtering
- Subscription billing queries
- Invoice lifecycle management
- Payment workflow support
- Revenue reporting queries
"""

from __future__ import annotations

from django.db import models


class InvoiceQuerySet(
    models.QuerySet,
):
    """
    Invoice queryset helpers.
    """

    # --------------------------------------------------------------
    # Status Filters
    # --------------------------------------------------------------

    def drafts(
        self,
    ):
        """
        Return draft invoices.
        """

        return self.filter(
            status="DRAFT",
        )

    def issued(
        self,
    ):
        """
        Return issued invoices.
        """

        return self.filter(
            status="ISSUED",
        )

    def sent(
        self,
    ):
        """
        Return sent invoices.
        """

        return self.filter(
            status="SENT",
        )

    def partially_paid(
        self,
    ):
        """
        Return partially paid invoices.
        """

        return self.filter(
            status="PARTIALLY_PAID",
        )

    def paid(
        self,
    ):
        """
        Return paid invoices.
        """

        return self.filter(
            status="PAID",
        )

    def failed(
        self,
    ):
        """
        Return failed invoices.
        """

        return self.filter(
            status="FAILED",
        )

    def cancelled(
        self,
    ):
        """
        Return cancelled invoices.
        """

        return self.filter(
            status="CANCELLED",
        )

    def refunded(
        self,
    ):
        """
        Return refunded invoices.
        """

        return self.filter(
            status="REFUNDED",
        )

    def overdue(
        self,
    ):
        """
        Return overdue invoices.
        """

        return self.filter(
            status="OVERDUE",
        )

    # --------------------------------------------------------------
    # Ownership
    # --------------------------------------------------------------

    def by_tenant(
        self,
        tenant,
    ):
        """
        Filter invoices by tenant.
        """

        return self.filter(
            tenant=tenant,
        )

    def by_organization(
        self,
        organization,
    ):
        """
        Filter invoices by organization.
        """

        return self.filter(
            organization=organization,
        )

    def by_subscription(
        self,
        subscription,
    ):
        """
        Filter invoices by subscription.
        """

        return self.filter(
            subscription=subscription,
        )

    # --------------------------------------------------------------
    # Billing
    # --------------------------------------------------------------

    def subscription_invoices(
        self,
    ):
        """
        Return subscription invoices.
        """

        return self.filter(
            invoice_type="SUBSCRIPTION",
        )

    def usage_invoices(
        self,
    ):
        """
        Return usage based invoices.
        """

        return self.filter(
            invoice_type="USAGE",
        )

    def addon_invoices(
        self,
    ):
        """
        Return addon invoices.
        """

        return self.filter(
            invoice_type="ADDON",
        )

    # --------------------------------------------------------------
    # Payment Workflow
    # --------------------------------------------------------------

    def outstanding(
        self,
    ):
        """
        Return unpaid invoices.
        """

        return self.exclude(
            status__in=[
                "PAID",
                "CANCELLED",
                "REFUNDED",
            ],
        )

    def payable(
        self,
    ):
        """
        Return invoices eligible for payment.
        """

        return self.filter(
            status__in=[
                "ISSUED",
                "SENT",
                "PARTIALLY_PAID",
                "OVERDUE",
            ],
        )

    def with_balance_due(
        self,
    ):
        """
        Return invoices having pending balance.
        """

        return self.filter(
            total_amount__gt=models.F(
                "paid_amount",
            ),
        )

    # --------------------------------------------------------------
    # Date Queries
    # --------------------------------------------------------------

    def due_before(
        self,
        date,
    ):
        """
        Return invoices due before date.
        """

        return self.filter(
            due_at__lte=date,
        )

    def issued_between(
        self,
        start,
        end,
    ):
        """
        Return invoices generated in period.
        """

        return self.filter(
            issued_at__range=(
                start,
                end,
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
        Return latest invoices.
        """

        return self.order_by(
            "-created_at",
        )[:limit]

    def revenue_ready(
        self,
    ):
        """
        Return invoices counted as revenue.
        """

        return self.filter(
            status__in=[
                "PAID",
                "PARTIALLY_PAID",
            ],
        )


class InvoiceManager(
    models.Manager,
):
    """
    Manager for Invoice model.
    """

    def get_queryset(
        self,
    ):
        return InvoiceQuerySet(
            self.model,
            using=self._db,
        )

    def latest_for_organization(
        self,
        organization,
    ):
        """
        Return latest organization invoice.
        """

        return (
            self.get_queryset()
            .by_organization(
                organization,
            )
            .first()
        )


__all__ = [
    "InvoiceManager",
    "InvoiceQuerySet",
]
