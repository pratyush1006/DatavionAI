"""
Entitlement selectors.

Read-only query layer for DatavionOS
SaaS entitlement management.

Responsibilities:

- Subscription entitlement lookup
- Module access queries
- Feature access queries
- Plan limits lookup
- Dashboard configuration support

Architecture:

Organization
      |
Subscription
      |
Plan
      |
EntitlementSelector
      |
Modules / Features / Limits
"""

from __future__ import annotations

from apps.platform.saas_billing.models import (
    Subscription,
)


class EntitlementSelector:
    """
    SaaS entitlement read operations.
    """

    @staticmethod
    def get_subscription(
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
            )
            .first()
        )

    @staticmethod
    def get_modules(
        *,
        organization,
    ) -> dict:
        """
        Return enabled DatavionOS modules.

        Example:

        {
            "clinical": True,
            "pharmacy": True,
            "laboratory": False,
            "ai": True
        }
        """

        subscription = EntitlementSelector.get_subscription(
            organization=organization,
        )

        if not subscription:
            return {}

        return subscription.feature_snapshot.get(
            "modules",
            {},
        )

    @staticmethod
    def get_features(
        *,
        organization,
    ) -> dict:
        """
        Return enabled features.
        """

        subscription = EntitlementSelector.get_subscription(
            organization=organization,
        )

        if not subscription:
            return {}

        return subscription.feature_snapshot.get(
            "features",
            {},
        )

    @staticmethod
    def get_limits(
        *,
        organization,
    ) -> dict:
        """
        Return subscription limits.

        Example:

        {
            "users": 100,
            "patients": 50000,
            "storage_gb": 500
        }
        """

        subscription = EntitlementSelector.get_subscription(
            organization=organization,
        )

        if not subscription:
            return {}

        return subscription.plan_snapshot.get(
            "limits",
            {},
        )

    @staticmethod
    def has_module(
        *,
        organization,
        module: str,
    ) -> bool:
        """
        Check module access.
        """

        modules = EntitlementSelector.get_modules(
            organization=organization,
        )

        return bool(
            modules.get(
                module,
                False,
            )
        )

    @staticmethod
    def has_feature(
        *,
        organization,
        feature: str,
    ) -> bool:
        """
        Check feature access.
        """

        features = EntitlementSelector.get_features(
            organization=organization,
        )

        return bool(
            features.get(
                feature,
                False,
            )
        )

    @staticmethod
    def get_dashboard_context(
        *,
        organization,
    ) -> dict:
        """
        Return frontend bootstrap entitlement data.

        Used by DatavionOS dynamic UI.

        Example:

        Clinic:
            patients
            appointments

        Pharmacy:
            inventory
            sales

        Hospital:
            clinical
            laboratory
            imaging
        """

        return {
            "modules": (
                EntitlementSelector.get_modules(
                    organization=organization,
                )
            ),
            "features": (
                EntitlementSelector.get_features(
                    organization=organization,
                )
            ),
            "limits": (
                EntitlementSelector.get_limits(
                    organization=organization,
                )
            ),
        }

    @staticmethod
    def can_access(
        *,
        organization,
        module: str | None = None,
        feature: str | None = None,
    ) -> bool:
        """
        Generic entitlement check.
        """

        if module:
            return EntitlementSelector.has_module(
                organization=organization,
                module=module,
            )

        if feature:
            return EntitlementSelector.has_feature(
                organization=organization,
                feature=feature,
            )

        return False


__all__ = [
    "EntitlementSelector",
]
