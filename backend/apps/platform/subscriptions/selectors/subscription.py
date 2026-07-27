"""
Tenant subscription selectors.
"""

from __future__ import annotations

from apps.platform.subscriptions.models import (
    TenantSubscription,
)


def get_tenant_subscription(
    *,
    tenant,
) -> TenantSubscription | None:
    """
    Return active tenant subscription.
    """

    if tenant is None:
        return None

    return (
        TenantSubscription.objects.select_related(
            "plan",
        )
        .filter(
            tenant=tenant,
            status=TenantSubscription.Status.ACTIVE,
        )
        .first()
    )


def has_active_subscription(
    *,
    tenant,
) -> bool:
    """
    Check tenant subscription status.
    """

    return (
        get_tenant_subscription(
            tenant=tenant,
        )
        is not None
    )


def get_subscription_plan(
    *,
    tenant,
):
    """
    Return tenant active plan.
    """

    subscription = get_tenant_subscription(
        tenant=tenant,
    )

    if subscription is None:
        return None

    return subscription.plan


__all__ = [
    "get_tenant_subscription",
    "has_active_subscription",
    "get_subscription_plan",
]
