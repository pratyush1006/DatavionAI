"""
DatavionOS subscription selectors.
"""

from __future__ import annotations

from apps.platform.saas_billing.models.subscription import Subscription


def get_organization_subscription(
    organization,
) -> Subscription | None:
    """
    Return the organization's current subscription.
    """

    return (
        Subscription.objects.select_related("plan", "organization", "tenant")
        .filter(organization=organization)
        .first()
    )


def get_active_organization_subscription(
    organization,
) -> Subscription | None:
    """
    Return the organization's active/trial subscription.
    """

    return (
        Subscription.objects.select_related("plan", "organization", "tenant")
        .filter(
            organization=organization,
            status__in=[
                Subscription.Status.TRIAL,
                Subscription.Status.ACTIVE,
                Subscription.Status.PAST_DUE,
            ],
        )
        .first()
    )


__all__ = [
    "get_active_organization_subscription",
    "get_organization_subscription",
]
