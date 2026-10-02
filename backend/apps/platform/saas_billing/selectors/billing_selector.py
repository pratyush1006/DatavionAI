"""
Billing selectors.

Read-only query layer for DatavionOS
SaaS billing accounts.

Responsibilities:

- Retrieve billing accounts
- Organization billing lookup
- Tenant billing lookup
- Payment provider queries
- Billing status queries

Architecture:

API
 |
Selectors
 |
Models
"""

from __future__ import annotations

from apps.platform.saas_billing.models import (
    BillingAccount,
)


class BillingSelector:
    """
    Billing account read operations.
    """

    @staticmethod
    def get_by_organization(
        *,
        organization,
    ) -> BillingAccount | None:
        """
        Get billing account by organization.
        """

        return BillingAccount.objects.filter(
            organization=organization,
        ).first()

    @staticmethod
    def get_by_tenant(
        *,
        tenant,
    ):
        """
        Return tenant billing accounts.
        """

        return BillingAccount.objects.filter(
            tenant=tenant,
        )

    @staticmethod
    def get_active_accounts():
        """
        Return active billing accounts.
        """

        return BillingAccount.objects.active()

    @staticmethod
    def get_by_payment_provider(
        *,
        provider: str,
    ):
        """
        Return accounts using payment provider.
        """

        return BillingAccount.objects.with_payment_provider(
            provider,
        )

    @staticmethod
    def get_auto_charge_accounts():
        """
        Return accounts with auto charge enabled.
        """

        return BillingAccount.objects.auto_charge_enabled()

    @staticmethod
    def exists_for_organization(
        *,
        organization,
    ) -> bool:
        """
        Check billing account existence.
        """

        return BillingAccount.objects.filter(
            organization=organization,
        ).exists()


__all__ = [
    "BillingSelector",
]
