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

API
 |
Selector
 |
EntitlementService
 |
Subscription Snapshot
 |
Database
"""

from __future__ import annotations

from apps.platform.saas_billing.models import (
    Subscription,
)
from apps.platform.saas_billing.services.entitlement_service import (
    EntitlementService,
)


class EntitlementSelector:
    """
    SaaS entitlement read operations.
    """

    # ==============================================================
    # Subscription
    # ==============================================================

    @staticmethod
    def get_subscription(
        *,
        organization,
    ) -> Subscription | None:
        """
        Return active organization subscription.
        """

        return EntitlementService.get_subscription(
            organization=organization,
        )

    # ==============================================================
    # Modules
    # ==============================================================

    @staticmethod
    def get_modules(
        *,
        organization,
    ) -> dict:
        """
        Return module entitlement map.
        """

        return EntitlementService.get_modules(
            organization=organization,
        )

    @staticmethod
    def get_enabled_modules(
        *,
        organization,
    ) -> list[str]:
        """
        Return enabled module names.

        Example:

        [
            "clinical",
            "billing",
            "laboratory"
        ]
        """

        return EntitlementService.get_enabled_modules(
            organization=organization,
        )

    # ==============================================================
    # Features
    # ==============================================================

    @staticmethod
    def get_features(
        *,
        organization,
    ) -> dict:
        """
        Return feature entitlement map.
        """

        return EntitlementService.get_features(
            organization=organization,
        )

    @staticmethod
    def get_enabled_features(
        *,
        organization,
    ) -> list[str]:
        """
        Return enabled feature names.
        """

        return EntitlementService.get_enabled_features(
            organization=organization,
        )

    # ==============================================================
    # Limits
    # ==============================================================

    @staticmethod
    def get_limits(
        *,
        organization,
    ) -> dict:
        """
        Return SaaS resource limits.
        """

        return EntitlementService.get_limits(
            organization=organization,
        )

    # ==============================================================
    # Access Checks
    # ==============================================================

    @staticmethod
    def has_module(
        *,
        organization,
        module: str,
    ) -> bool:
        """
        Check module entitlement.
        """

        return EntitlementService.has_module(
            organization=organization,
            module=module,
        )

    @staticmethod
    def has_feature(
        *,
        organization,
        feature: str,
    ) -> bool:
        """
        Check feature entitlement.
        """

        return EntitlementService.has_feature(
            organization=organization,
            feature=feature,
        )

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

        return EntitlementService.can_access(
            organization=organization,
            module=module,
            feature=feature,
        )

    # ==============================================================
    # Bootstrap Context
    # ==============================================================

    @staticmethod
    def get_dashboard_context(
        *,
        organization,
    ) -> dict:
        """
        Frontend bootstrap entitlement payload.

        Used by:

        - Platform Bootstrap API
        - Next.js dashboard
        - Dynamic navigation
        - Feature flags
        """

        return {
            "modules": (
                EntitlementSelector.get_enabled_modules(
                    organization=organization,
                )
            ),
            "features": (
                EntitlementSelector.get_enabled_features(
                    organization=organization,
                )
            ),
            "limits": (
                EntitlementSelector.get_limits(
                    organization=organization,
                )
            ),
        }


__all__ = [
    "EntitlementSelector",
]
