"""
DatavionOS entitlement resolver.

This module provides the DatavionOS runtime-facing adapter over the
SaaS Billing entitlement service.

Architecture
------------

    DatavionOS Runtime
            |
            v
    EntitlementResolver
            |
            v
    SaaS Billing EntitlementService
            |
            v
       Subscription
            |
            v
           Plan
            |
       +----+----+----------------+
       |         |                |
       v         v                v
    Modules   Features          Limits
       |         |                |
       +---------+----------------+
                 |
                 v
        Runtime Capabilities


Ownership
---------

SaaS Billing owns:

- Subscription lifecycle
- Plan
- Module entitlements
- Feature entitlements
- Usage limits
- Capability resolution

DatavionOS owns:

- Runtime bootstrap
- Module registry
- Module availability
- Navigation
- Dashboard
- Runtime capability consumption

This resolver intentionally does NOT:

- Query subscription models directly
- Query module entitlement models directly
- Query feature entitlement models directly
- Apply RBAC rules
- Apply tenant-type rules
- Build navigation
- Build dashboard cards
- Duplicate SaaS Billing business rules

Design Principles
-----------------

- Single entitlement ownership
- Dependency inversion
- Thin runtime adapter
- Stable DatavionOS API
- Snapshot-based runtime resolution
- No duplicate billing logic
- No direct ORM access
- Explicit failure-safe defaults
- Enterprise ready
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.platform.saas_billing.services.entitlement_service import (
    EntitlementService,
)


class EntitlementResolver:
    """
    Runtime entitlement resolver for DatavionOS.

    This class is the boundary between the DatavionOS runtime kernel and
    the SaaS Billing entitlement domain.

    DatavionOS callers should use this resolver instead of accessing
    SaaS Billing models or entitlement tables directly.
    """

    # ==================================================================
    # Runtime Capability Resolution
    # ==================================================================

    @staticmethod
    def resolve(
        *,
        organization,
    ) -> dict[str, Any]:
        """
        Resolve the complete runtime entitlement payload.

        The resolver performs one subscription lookup and derives the
        runtime entitlement data from the subscription snapshots.

        Returns:

            {
                "modules": {
                    "patients": True,
                    ...
                },
                "features": {
                    "clinical.ai": True,
                    ...
                },
                "limits": {
                    "patients": {
                        "included": 1000,
                        ...
                    },
                    ...
                },
                "capabilities": {
                    "subscription": {...},
                    "modules": {...},
                    "features": {...},
                    "limits": {...},
                },
            }

        When no active subscription exists, an explicit empty capability
        payload is returned.

        This is intentional: absence of a subscription must never grant
        entitlement implicitly.
        """

        if organization is None:
            return EntitlementResolver._empty_capabilities()

        subscription = EntitlementService.get_subscription(
            organization=organization,
        )

        if subscription is None:
            return EntitlementResolver._empty_capabilities()

        feature_snapshot = EntitlementResolver._mapping_or_empty(
            getattr(
                subscription,
                "feature_snapshot",
                None,
            )
        )

        plan_snapshot = EntitlementResolver._mapping_or_empty(
            getattr(
                subscription,
                "plan_snapshot",
                None,
            )
        )

        modules = EntitlementResolver._mapping_or_empty(
            feature_snapshot.get(
                "modules",
                {},
            )
        )

        features = EntitlementResolver._mapping_or_empty(
            feature_snapshot.get(
                "features",
                {},
            )
        )

        limits = EntitlementResolver._mapping_or_empty(
            plan_snapshot.get(
                "limits",
                {},
            )
        )

        plan = getattr(
            subscription,
            "plan",
            None,
        )

        subscription_payload: dict[str, Any] = {
            "status": subscription.status,
            "plan": {
                "name": (
                    getattr(
                        plan,
                        "name",
                        "",
                    )
                ),
                "code": (
                    getattr(
                        plan,
                        "code",
                        "",
                    )
                ),
            },
        }

        capabilities = {
            "subscription": subscription_payload,
            "modules": modules,
            "features": features,
            "limits": limits,
        }

        return {
            "modules": modules,
            "features": features,
            "limits": limits,
            "capabilities": capabilities,
        }

    # ==================================================================
    # Module Access
    # ==================================================================

    @staticmethod
    def has_module(
        *,
        organization,
        module: str,
    ) -> bool:
        """
        Determine whether an organization is entitled to a module.

        SaaS Billing remains the owner of the entitlement rule.

        This method does not determine:

        - Whether the module is registered
        - Whether the module is enabled at platform level
        - Whether the tenant type supports the module
        - Whether the user has RBAC permission

        Those concerns belong to their respective DatavionOS layers.
        """

        if organization is None:
            return False

        normalized_module = EntitlementResolver._normalize_key(
            module,
        )

        if not normalized_module:
            return False

        return EntitlementService.has_module(
            organization=organization,
            module=normalized_module,
        )

    # ==================================================================
    # Feature Access
    # ==================================================================

    @staticmethod
    def has_feature(
        *,
        organization,
        feature: str,
    ) -> bool:
        """
        Determine whether an organization is entitled to a feature.

        SaaS Billing remains the owner of the feature entitlement rule.
        """

        if organization is None:
            return False

        normalized_feature = EntitlementResolver._normalize_key(
            feature,
        )

        if not normalized_feature:
            return False

        return EntitlementService.has_feature(
            organization=organization,
            feature=normalized_feature,
        )

    # ==================================================================
    # Limits
    # ==================================================================

    @staticmethod
    def get_limit(
        *,
        organization,
        key: str,
    ) -> Any:
        """
        Return a single subscription usage limit.

        ``None`` means the limit is not defined by the active subscription.
        The underlying SaaS Billing service remains responsible for
        interpreting the limit configuration.
        """

        if organization is None:
            return None

        normalized_key = EntitlementResolver._normalize_key(
            key,
        )

        if not normalized_key:
            return None

        return EntitlementService.get_limit(
            organization=organization,
            key=normalized_key,
        )

    @staticmethod
    def check_limit(
        *,
        organization,
        limit_key: str,
        requested_value: int = 1,
    ) -> bool:
        """
        Check whether a requested quantity is permitted by the
        organization's active subscription.

        The actual limit semantics belong to SaaS Billing.
        """

        if organization is None:
            return False

        if requested_value < 0:
            return False

        normalized_key = EntitlementResolver._normalize_key(
            limit_key,
        )

        if not normalized_key:
            return False

        return EntitlementService.check_limit(
            organization=organization,
            limit_key=normalized_key,
            requested_value=requested_value,
        )

    # ==================================================================
    # Access Resolution
    # ==================================================================

    @staticmethod
    def can_access(
        *,
        organization,
        module: str | None = None,
        feature: str | None = None,
    ) -> bool:
        """
        Determine whether the organization has the requested entitlement.

        Exactly one entitlement dimension should normally be supplied.

        Module access is checked before feature access to preserve the
        existing EntitlementService contract.
        """

        if organization is None:
            return False

        normalized_module = (
            EntitlementResolver._normalize_key(
                module,
            )
            if module is not None
            else ""
        )

        normalized_feature = (
            EntitlementResolver._normalize_key(
                feature,
            )
            if feature is not None
            else ""
        )

        if normalized_module:
            return EntitlementResolver.has_module(
                organization=organization,
                module=normalized_module,
            )

        if normalized_feature:
            return EntitlementResolver.has_feature(
                organization=organization,
                feature=normalized_feature,
            )

        return False

    # ==================================================================
    # Internal Helpers
    # ==================================================================

    @staticmethod
    def _mapping_or_empty(
        value: object,
    ) -> dict[str, Any]:
        """
        Convert a mapping-like snapshot into a plain dictionary.

        Subscription snapshots are JSON-backed dictionaries. This helper
        provides a defensive boundary so malformed/null snapshot values
        cannot break runtime bootstrap construction.
        """

        if not isinstance(
            value,
            Mapping,
        ):
            return {}

        return dict(value)

    @staticmethod
    def _normalize_key(
        value: str,
    ) -> str:
        """
        Normalize an entitlement identifier.

        Empty identifiers are rejected by returning an empty string.
        """

        if not isinstance(
            value,
            str,
        ):
            return ""

        return value.strip()

    @staticmethod
    def _empty_capabilities() -> dict[str, Any]:
        """
        Return the explicit no-entitlement runtime payload.

        An absent subscription must fail closed.
        """

        return {
            "modules": {},
            "features": {},
            "limits": {},
            "capabilities": {
                "subscription": None,
                "modules": {},
                "features": {},
                "limits": {},
            },
        }


__all__ = [
    "EntitlementResolver",
]
