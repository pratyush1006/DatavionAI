"""
DatavionOS entitlement resolver.

Bridges:

DatavionOS Kernel
        |
        v
SaaS Billing Entitlements
        |
        v
Subscription
        |
        v
Plan Capabilities


Responsibilities:

- Resolve enabled modules
- Resolve enabled features
- Resolve subscription limits
- Provide runtime capabilities
- Optimize bootstrap entitlement loading

Architecture:

SaaS Billing owns:
    - Subscription
    - Plan
    - Limits
    - Features

DatavionOS owns:
    - Runtime bootstrap
    - Module loading
    - Dashboard
    - Navigation
"""

from __future__ import annotations

from apps.platform.saas_billing.services.entitlement_service import (
    EntitlementService,
)


class EntitlementResolver:
    """
    Runtime entitlement resolver.

    Used by:

    - DatavionOS Bootstrap
    - Dashboard builder
    - Navigation builder
    - Module loader
    """

    # ==============================================================
    # Resolve Runtime Capabilities
    # ==============================================================

    @staticmethod
    def resolve(
        *,
        organization,
    ) -> dict:
        """
        Resolve organization runtime capabilities.

        Performs a single subscription lookup
        and builds frontend bootstrap payload.

        Returns:

        {
            modules: {},
            features: {},
            limits: {},
            capabilities: {}
        }
        """

        subscription = EntitlementService.get_subscription(
            organization=organization,
        )

        if not subscription:
            return {
                "modules": {},
                "features": {},
                "limits": {},
                "capabilities": {},
            }

        modules = subscription.feature_snapshot.get(
            "modules",
            {},
        )

        features = subscription.feature_snapshot.get(
            "features",
            {},
        )

        limits = subscription.plan_snapshot.get(
            "limits",
            {},
        )

        return {
            # ------------------------------------------------------
            # Module access
            # ------------------------------------------------------
            "modules": modules,
            # ------------------------------------------------------
            # Feature access
            # ------------------------------------------------------
            "features": features,
            # ------------------------------------------------------
            # Resource limits
            # ------------------------------------------------------
            "limits": limits,
            # ------------------------------------------------------
            # Complete runtime capability payload
            # ------------------------------------------------------
            "capabilities": {
                "subscription": {
                    "status": subscription.status,
                    "plan": {
                        "name": subscription.plan.name,
                        "code": subscription.plan.code,
                    },
                },
                "modules": modules,
                "features": features,
                "limits": limits,
            },
        }

    # ==============================================================
    # Module Check
    # ==============================================================

    @staticmethod
    def has_module(
        *,
        organization,
        module: str,
    ) -> bool:
        """
        Check module availability.
        """

        return EntitlementService.has_module(
            organization=organization,
            module=module,
        )

    # ==============================================================
    # Feature Check
    # ==============================================================

    @staticmethod
    def has_feature(
        *,
        organization,
        feature: str,
    ) -> bool:
        """
        Check feature availability.
        """

        return EntitlementService.has_feature(
            organization=organization,
            feature=feature,
        )


__all__ = [
    "EntitlementResolver",
]
