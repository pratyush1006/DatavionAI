"""
Subscription entitlement selectors.

Resolves module and feature access
from tenant subscription.
"""

from __future__ import annotations

from apps.platform.subscriptions.models import (
    FeatureEntitlement,
    ModuleEntitlement,
)

from .subscription import (
    get_subscription_plan,
)


def get_available_modules(
    *,
    tenant,
) -> set[str]:
    """
    Return module identifiers available
    for tenant.
    """

    plan = get_subscription_plan(
        tenant=tenant,
    )

    if plan is None:
        return set()

    return set(
        ModuleEntitlement.objects.filter(
            plan=plan,
            enabled=True,
        ).values_list(
            "module_identifier",
            flat=True,
        )
    )


def has_module_access(
    *,
    tenant,
    module_identifier: str,
) -> bool:
    """
    Check module entitlement.
    """

    return module_identifier in get_available_modules(
        tenant=tenant,
    )


def get_enabled_features(
    *,
    tenant,
) -> set[str]:
    """
    Return enabled feature keys.
    """

    plan = get_subscription_plan(
        tenant=tenant,
    )

    if plan is None:
        return set()

    return set(
        FeatureEntitlement.objects.filter(
            plan=plan,
            enabled=True,
        ).values_list(
            "feature_key",
            flat=True,
        )
    )


def has_feature(
    *,
    tenant,
    feature_key: str,
) -> bool:
    """
    Check feature entitlement.
    """

    return feature_key in get_enabled_features(
        tenant=tenant,
    )


__all__ = [
    "get_available_modules",
    "has_module_access",
    "get_enabled_features",
    "has_feature",
]
