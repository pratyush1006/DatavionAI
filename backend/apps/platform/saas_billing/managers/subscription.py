"""
Subscription managers.

Provides reusable queryset operations
for DatavionOS SaaS subscription lifecycle.

Responsibilities:

- Subscription status filtering
- Organization subscriptions
- Tenant subscriptions
- Plan subscriptions
- Renewal workflows
- Expiry monitoring
- Billing provider synchronization
- Entitlement resolution
"""

from __future__ import annotations

from django.db import models


class SubscriptionQuerySet(
    models.QuerySet,
):
    """
    Subscription queryset helpers.
    """

    def active(
        self,
    ):
        """
        Return active subscriptions.
        """

        return self.filter(
            status="ACTIVE",
        )

    def trial(
        self,
    ):
        """
        Return trial subscriptions.
        """

        return self.filter(
            status="TRIAL",
        )

    def accessible(
        self,
    ):
        """
        Return subscriptions currently
        allowed platform access.
        """

        return self.filter(
            status__in=[
                "TRIAL",
                "ACTIVE",
            ],
        )

    def past_due(
        self,
    ):
        """
        Return payment overdue subscriptions.
        """

        return self.filter(
            status="PAST_DUE",
        )

    def suspended(
        self,
    ):
        """
        Return suspended subscriptions.
        """

        return self.filter(
            status="SUSPENDED",
        )

    def cancelled(
        self,
    ):
        """
        Return cancelled subscriptions.
        """

        return self.filter(
            status="CANCELLED",
        )

    def expired(
        self,
    ):
        """
        Return expired subscriptions.
        """

        return self.filter(
            status="EXPIRED",
        )

    # --------------------------------------------------------------
    # Ownership
    # --------------------------------------------------------------

    def by_tenant(
        self,
        tenant,
    ):
        """
        Filter tenant subscriptions.
        """

        return self.filter(
            tenant=tenant,
        )

    def by_organization(
        self,
        organization,
    ):
        """
        Filter organization subscriptions.
        """

        return self.filter(
            organization=organization,
        )

    # --------------------------------------------------------------
    # Plan
    # --------------------------------------------------------------

    def by_plan(
        self,
        plan,
    ):
        """
        Filter subscriptions by plan.
        """

        return self.filter(
            plan=plan,
        )

    def enterprise(
        self,
    ):
        """
        Return enterprise subscriptions.
        """

        return self.filter(
            plan__plan_type="ENTERPRISE",
        )

    # --------------------------------------------------------------
    # Renewal
    # --------------------------------------------------------------

    def auto_renewing(
        self,
    ):
        """
        Return subscriptions enabled
        for automatic renewal.
        """

        return self.filter(
            auto_renew=True,
            status__in=[
                "ACTIVE",
                "TRIAL",
            ],
        )

    def renewal_due_before(
        self,
        date,
    ):
        """
        Return subscriptions requiring renewal.
        """

        return self.filter(
            current_period_end__lte=date,
            auto_renew=True,
        )

    # --------------------------------------------------------------
    # Expiry
    # --------------------------------------------------------------

    def expiring_before(
        self,
        date,
    ):
        """
        Return subscriptions expiring
        before given date.
        """

        return self.filter(
            expires_at__lte=date,
        )

    def in_grace_period(
        self,
        date,
    ):
        """
        Return subscriptions inside grace period.
        """

        return self.filter(
            grace_period_end__gte=date,
        )

    # --------------------------------------------------------------
    # Payment Provider
    # --------------------------------------------------------------

    def with_external_subscription(
        self,
    ):
        """
        Return subscriptions linked
        with payment providers.
        """

        return self.exclude(
            external_subscription_id="",
        ).exclude(
            external_subscription_id__isnull=True,
        )

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

    # --------------------------------------------------------------
    # Billing Period
    # --------------------------------------------------------------

    def current_period(
        self,
        date,
    ):
        """
        Return subscriptions active
        during billing period.
        """

        return self.filter(
            current_period_start__lte=date,
            current_period_end__gte=date,
        )


class SubscriptionManager(
    models.Manager,
):
    """
    Manager for Subscription model.
    """

    def get_queryset(
        self,
    ):
        return SubscriptionQuerySet(
            self.model,
            using=self._db,
        )

    def active_for_organization(
        self,
        organization,
    ):
        """
        Get active organization subscription.
        """

        return (
            self.get_queryset()
            .by_organization(
                organization,
            )
            .accessible()
            .first()
        )


__all__ = [
    "SubscriptionManager",
    "SubscriptionQuerySet",
]
