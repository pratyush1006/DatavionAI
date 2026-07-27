"""
Subscription plan selectors.
"""

from __future__ import annotations

from apps.platform.subscriptions.models import (
    SubscriptionPlan,
)


def get_active_plans():
    """
    Return all active subscription plans.
    """

    return SubscriptionPlan.objects.filter(
        is_active=True,
    ).order_by(
        "name",
    )


def get_plan_by_code(
    *,
    code: str,
) -> SubscriptionPlan | None:
    """
    Return subscription plan by code.
    """

    return SubscriptionPlan.objects.filter(
        code=code,
        is_active=True,
    ).first()


__all__ = [
    "get_active_plans",
    "get_plan_by_code",
]
