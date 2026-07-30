"""
Billing account managers.

Provides reusable queryset operations
for DatavionOS SaaS BillingAccount objects.

Responsibilities:

- Tenant billing isolation
- Organization billing queries
- Billing lifecycle filtering
- Payment provider tracking
- Enterprise billing workflows
- Revenue operations support
"""

from __future__ import annotations

from django.db import models


class BillingAccountQuerySet(
    models.QuerySet,
):
    """
    Billing account queryset helpers.
    """

    # --------------------------------------------------------------
    # Lifecycle
    # --------------------------------------------------------------

    def active(
        self,
    ):
        """
        Return active billing accounts.
        """

        return self.filter(
            status="ACTIVE",
        )

    def suspended(
        self,
    ):
        """
        Return suspended billing accounts.
        """

        return self.filter(
            status="SUSPENDED",
        )

    def closed(
        self,
    ):
        """
        Return closed billing accounts.
        """

        return self.filter(
            status="CLOSED",
        )

    # --------------------------------------------------------------
    # Ownership
    # --------------------------------------------------------------

    def by_tenant(
        self,
        tenant,
    ):
        """
        Filter billing accounts by tenant.
        """

        return self.filter(
            tenant=tenant,
        )

    def by_organization(
        self,
        organization,
    ):
        """
        Filter billing account by organization.
        """

        return self.filter(
            organization=organization,
        )

    # --------------------------------------------------------------
    # Payment Provider
    # --------------------------------------------------------------

    def with_payment_provider(
        self,
        provider: str,
    ):
        """
        Filter accounts configured
        with a payment provider.
        """

        return self.filter(
            payment_provider=provider,
        )

    def without_payment_provider(
        self,
    ):
        """
        Return accounts without
        payment provider setup.
        """

        return self.filter(
            models.Q(
                payment_provider="",
            )
            | models.Q(
                payment_provider__isnull=True,
            )
        )

    def auto_charge_enabled(
        self,
    ):
        """
        Return accounts having
        automatic payment enabled.
        """

        return self.filter(
            auto_charge_enabled=True,
        )

    def auto_charge_disabled(
        self,
    ):
        """
        Return accounts where
        automatic payment is disabled.
        """

        return self.filter(
            auto_charge_enabled=False,
        )

    # --------------------------------------------------------------
    # Enterprise Billing
    # --------------------------------------------------------------

    def purchase_order_required(
        self,
    ):
        """
        Return enterprise accounts
        requiring purchase orders.
        """

        return self.filter(
            purchase_order_required=True,
        )

    def with_credit_limit(
        self,
    ):
        """
        Return accounts having
        configured credit limit.
        """

        return self.filter(
            credit_limit__gt=0,
        )

    # --------------------------------------------------------------
    # Tax
    # --------------------------------------------------------------

    def gst_registered(
        self,
    ):
        """
        Return GST registered accounts.
        """

        return self.exclude(
            gst_number="",
        )

    def vat_registered(
        self,
    ):
        """
        Return VAT registered accounts.
        """

        return self.exclude(
            vat_number="",
        )

    # --------------------------------------------------------------
    # Payment Customer Mapping
    # --------------------------------------------------------------

    def linked_payment_customer(
        self,
    ):
        """
        Return accounts mapped
        with external payment customer.
        """

        return self.exclude(
            payment_customer_id="",
        ).exclude(
            payment_customer_id__isnull=True,
        )

    def unlinked_payment_customer(
        self,
    ):
        """
        Return accounts without
        external payment customer.
        """

        return self.filter(
            models.Q(
                payment_customer_id="",
            )
            | models.Q(
                payment_customer_id__isnull=True,
            )
        )

    # --------------------------------------------------------------
    # Reporting
    # --------------------------------------------------------------

    def recent(
        self,
        limit: int = 10,
    ):
        """
        Return recently created accounts.
        """

        return self.order_by(
            "-created_at",
        )[:limit]


class BillingAccountManager(
    models.Manager,
):
    """
    Manager for BillingAccount model.
    """

    def get_queryset(
        self,
    ):
        return BillingAccountQuerySet(
            self.model,
            using=self._db,
        )

    def organization_account(
        self,
        organization,
    ):
        """
        Return organization billing account.
        """

        return (
            self.get_queryset()
            .by_organization(
                organization,
            )
            .first()
        )

    def tenant_accounts(
        self,
        tenant,
    ):
        """
        Return tenant billing accounts.
        """

        return self.get_queryset().by_tenant(
            tenant,
        )


__all__ = [
    "BillingAccountManager",
    "BillingAccountQuerySet",
]
