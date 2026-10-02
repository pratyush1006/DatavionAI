"""
Subscription selectors.

Read-only query layer for DatavionOS
SaaS subscriptions.

Responsibilities:

- Organization subscription lookup
- Active subscription queries
- Trial subscription queries
- Plan based filtering
- Expiry monitoring
- Renewal candidates

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
    Subscription,
)


class SubscriptionSelector:
    """
    Subscription read operations.
    """

    @staticmethod
    def get_by_organization(
        *,
        organization,
    ) -> Subscription | None:
        """
        Return organization subscription.
        """

        return (
            Subscription.objects.filter(
                organization=organization,
            )
            .select_related(
                "plan",
                "organization",
            )
            .first()
        )

    @staticmethod
    def get_active_subscription(
        *,
        organization,
    ) -> Subscription | None:
        """
        Return active subscription.
        """

        return (
            Subscription.objects.active()
            .filter(
                organization=organization,
            )
            .select_related(
                "plan",
            )
            .first()
        )

    @staticmethod
    def get_trial_subscription(
        *,
        organization,
    ) -> Subscription | None:
        """
        Return trial subscription.
        """

        return (
            Subscription.objects.trial()
            .filter(
                organization=organization,
            )
            .select_related(
                "plan",
            )
            .first()
        )

    @staticmethod
    def by_plan(
        *,
        plan,
    ):
        """
        Return subscriptions using plan.
        """

        return Subscription.objects.by_plan(
            plan,
        ).select_related(
            "organization",
        )

    @staticmethod
    def active_subscriptions():
        """
        Return all active subscriptions.
        """

        return Subscription.objects.active().select_related(
            "organization",
            "plan",
        )

    @staticmethod
    def expiring_subscriptions(
        *,
        days: int = 7,
    ):
        """
        Return subscriptions expiring soon.
        """

        expiry_date = timezone.now() + timezone.timedelta(
            days=days,
        )

        return Subscription.objects.active().filter(
            expires_at__lte=expiry_date,
        )

    @staticmethod
    def renewal_candidates():
        """
        Return subscriptions eligible
        for automatic renewal.
        """

        return (
            Subscription.objects.auto_renewing()
            .active()
            .select_related(
                "plan",
                "organization",
            )
        )

    @staticmethod
    def has_subscription(
        *,
        organization,
    ) -> bool:
        """
        Check subscription existence.
        """

        return Subscription.objects.filter(
            organization=organization,
        ).exists()


__all__ = [
    "SubscriptionSelector",
]
