"""
DatavionOS SaaS entitlement service.

This service is the canonical business-logic boundary for subscription
entitlements.

Architecture
------------

    Tenant
       |
       v
    Organization
       |
       v
    Subscription
       |
       v
      Plan
       |
       +------------------+
       |                  |
       v                  v
    Snapshots          Plan Config
       |
       v
    EntitlementService
       |
       +---- Modules
       |
       +---- Features
       |
       +---- Limits
       |
       +---- Capabilities


Ownership
---------

This service owns:

- Active subscription resolution
- Subscription validity
- Module entitlement resolution
- Feature entitlement resolution
- Limit resolution
- Entitlement access checks
- Runtime capability payload construction

DatavionOS owns:

- Module registry
- Tenant-type eligibility
- RBAC
- Navigation
- Dashboard
- Bootstrap assembly

Design Principles
-----------------

- Single source of truth
- Fail closed
- No direct frontend concerns
- Snapshot-based runtime resolution
- No duplicate entitlement models
- Explicit subscription lifecycle handling
- Stable capability contract
- Type-safe service boundary
- Enterprise ready
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db.models import Q
from django.utils import timezone

from apps.platform.saas_billing.models import (
    Subscription,
)


class EntitlementService:
    """
    Canonical SaaS entitlement service.

    All application layers that need subscription entitlement information
    should use this service rather than querying Subscription, Plan, or
    entitlement configuration directly.
    """

    # ==================================================================
    # Subscription Lifecycle
    # ==================================================================

    ACTIVE_STATUSES = frozenset(
        {
            Subscription.Status.TRIAL,
            Subscription.Status.ACTIVE,
        }
    )

    # ==================================================================
    # Subscription Resolution
    # ==================================================================

    @staticmethod
    def get_subscription(
        *,
        organization,
    ) -> Subscription | None:
        """
        Resolve the currently effective subscription for an organization.

        A subscription is considered effective when:

        1. It belongs to the organization.
        2. Its status is TRIAL or ACTIVE.
        3. Its current billing period has not ended.

        ``current_period_end`` is nullable in the Subscription model.
        A NULL period end is therefore treated as an open-ended period.

        The related Plan is eagerly loaded because entitlement resolution
        frequently requires plan metadata.
        """

        if organization is None:
            return None

        now = timezone.now()

        return (
            Subscription.objects.filter(
                organization=organization,
                status__in=EntitlementService.ACTIVE_STATUSES,
            )
            .filter(
                Q(
                    current_period_end__isnull=True,
                )
                | Q(
                    current_period_end__gte=now,
                )
            )
            .select_related(
                "plan",
            )
            .order_by(
                "-created_at",
            )
            .first()
        )

    # ==================================================================
    # Snapshot Resolution
    # ==================================================================

    @staticmethod
    def get_snapshot(
        *,
        organization,
    ) -> dict[str, Any]:
        """
        Return the feature entitlement snapshot.

        The subscription snapshot represents the entitlement state captured
        for the subscription and is preferred over recalculating entitlement
        data from relational records at runtime.
        """

        subscription = EntitlementService.get_subscription(
            organization=organization,
        )

        if subscription is None:
            return {}

        return EntitlementService._mapping_or_empty(
            subscription.feature_snapshot,
        )

    # ==================================================================
    # Module Entitlements
    # ==================================================================

    @staticmethod
    def get_modules(
        *,
        organization,
    ) -> dict[str, bool]:
        """
        Return the complete module entitlement map.

        Example:

            {
                "patients": True,
                "appointments": True,
                "laboratory": False,
            }
        """

        snapshot = EntitlementService.get_snapshot(
            organization=organization,
        )

        return EntitlementService._boolean_mapping(
            snapshot.get(
                "modules",
                {},
            )
        )

    @staticmethod
    def get_enabled_modules(
        *,
        organization,
    ) -> list[str]:
        """
        Return identifiers of enabled modules.

        Ordering follows the insertion order of the stored entitlement
        snapshot.
        """

        return [
            module
            for module, enabled in EntitlementService.get_modules(
                organization=organization,
            ).items()
            if enabled
        ]

    # ==================================================================
    # Feature Entitlements
    # ==================================================================

    @staticmethod
    def get_features(
        *,
        organization,
    ) -> dict[str, bool]:
        """
        Return the complete feature entitlement map.

        Example:

            {
                "telemedicine": True,
                "ai.copilot": True,
                "advanced.analytics": False,
            }
        """

        snapshot = EntitlementService.get_snapshot(
            organization=organization,
        )

        return EntitlementService._boolean_mapping(
            snapshot.get(
                "features",
                {},
            )
        )

    @staticmethod
    def get_enabled_features(
        *,
        organization,
    ) -> list[str]:
        """
        Return identifiers of enabled features.
        """

        return [
            feature
            for feature, enabled in EntitlementService.get_features(
                organization=organization,
            ).items()
            if enabled
        ]

    # ==================================================================
    # Limits
    # ==================================================================

    @staticmethod
    def get_limits(
        *,
        organization,
    ) -> dict[str, Any]:
        """
        Return the complete subscription limit configuration.

        Limits are read from the frozen plan snapshot associated with
        the active subscription.
        """

        subscription = EntitlementService.get_subscription(
            organization=organization,
        )

        if subscription is None:
            return {}

        plan_snapshot = EntitlementService._mapping_or_empty(
            subscription.plan_snapshot,
        )

        return EntitlementService._mapping_or_empty(
            plan_snapshot.get(
                "limits",
                {},
            )
        )

    @staticmethod
    def get_limit(
        *,
        organization,
        key: str,
    ) -> Any:
        """
        Return one configured usage limit.

        Returns ``None`` when the organization has no active subscription
        or the requested limit is not configured.
        """

        normalized_key = EntitlementService._normalize_key(
            key,
        )

        if not normalized_key:
            return None

        return EntitlementService.get_limits(
            organization=organization,
        ).get(
            normalized_key,
        )

    @staticmethod
    def check_limit(
        *,
        organization,
        limit_key: str,
        requested_value: int = 1,
    ) -> bool:
        """
        Determine whether a requested quantity is within the subscription
        limit.

        Supported limit formats include:

            1000

        and:

            {
                "included": 1000,
                "overage_rate": "0.02",
                "unit": "request",
            }

        An undefined limit is treated as unrestricted because the service
        has no configured quota to enforce.

        A missing organization or invalid negative request fails closed.
        """

        if organization is None:
            return False

        if requested_value < 0:
            return False

        maximum = EntitlementService.get_limit(
            organization=organization,
            key=limit_key,
        )

        if maximum is None:
            return True

        if isinstance(
            maximum,
            Mapping,
        ):
            maximum = maximum.get(
                "included",
            )

        if maximum is None:
            return True

        if isinstance(
            maximum,
            bool,
        ):
            return bool(maximum)

        if not isinstance(
            maximum,
            int | float,
        ):
            return False

        return requested_value <= maximum

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
        Determine whether the organization has an enabled module.

        This method evaluates SaaS entitlement only.

        It does not evaluate:

        - ModuleRegistry availability
        - Tenant-type eligibility
        - User permissions
        - Feature flags
        """

        normalized_module = EntitlementService._normalize_key(
            module,
        )

        if organization is None or not normalized_module:
            return False

        return bool(
            EntitlementService.get_modules(
                organization=organization,
            ).get(
                normalized_module,
                False,
            )
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
        Determine whether the organization has an enabled feature.
        """

        normalized_feature = EntitlementService._normalize_key(
            feature,
        )

        if organization is None or not normalized_feature:
            return False

        return bool(
            EntitlementService.get_features(
                organization=organization,
            ).get(
                normalized_feature,
                False,
            )
        )

    # ==================================================================
    # General Access
    # ==================================================================

    @staticmethod
    def can_access(
        *,
        organization,
        module: str | None = None,
        feature: str | None = None,
    ) -> bool:
        """
        Determine whether the requested SaaS entitlement is available.

        Module access takes precedence when both module and feature are
        supplied, preserving the existing service contract.
        """

        if organization is None:
            return False

        if module:
            return EntitlementService.has_module(
                organization=organization,
                module=module,
            )

        if feature:
            return EntitlementService.has_feature(
                organization=organization,
                feature=feature,
            )

        return False

    # ==================================================================
    # Runtime Capabilities
    # ==================================================================

    @staticmethod
    def get_capabilities(
        *,
        organization,
    ) -> dict[str, Any]:
        """
        Build the canonical runtime capability payload.

        The payload intentionally uses boolean maps rather than lists so
        consumers can perform constant-time entitlement checks without
        reconstructing the capability state.

        Example:

            {
                "subscription": {
                    "status": "ACTIVE",
                    "plan": {
                        "name": "Professional",
                        "code": "professional",
                    },
                },
                "modules": {
                    "patients": True,
                    "appointments": True,
                },
                "features": {
                    "telemedicine": True,
                },
                "limits": {
                    "patients": {
                        "included": 5000,
                    },
                },
            }

        No active subscription produces an explicit fail-closed payload.
        """

        subscription = EntitlementService.get_subscription(
            organization=organization,
        )

        if subscription is None:
            return {
                "subscription": None,
                "modules": {},
                "features": {},
                "limits": {},
            }

        modules = EntitlementService.get_modules(
            organization=organization,
        )

        features = EntitlementService.get_features(
            organization=organization,
        )

        limits = EntitlementService.get_limits(
            organization=organization,
        )

        plan = subscription.plan

        return {
            "subscription": {
                "status": subscription.status,
                "plan": {
                    "name": plan.name,
                    "code": plan.code,
                },
            },
            "modules": modules,
            "features": features,
            "limits": limits,
        }

    # ==================================================================
    # Internal Helpers
    # ==================================================================

    @staticmethod
    def _mapping_or_empty(
        value: object,
    ) -> dict[str, Any]:
        """
        Return a plain dictionary for a mapping value.

        JSONField values should normally already be dictionaries, but the
        service keeps a defensive boundary around persisted configuration.
        """

        if not isinstance(
            value,
            Mapping,
        ):
            return {}

        return dict(value)

    @staticmethod
    def _boolean_mapping(
        value: object,
    ) -> dict[str, bool]:
        """
        Normalize a module/feature entitlement mapping.

        Only explicit boolean ``True`` values are treated as enabled.

        This prevents malformed persisted values such as arbitrary strings,
        numbers, nested objects, or lists from accidentally becoming
        entitlements through Python truthiness.
        """

        if not isinstance(
            value,
            Mapping,
        ):
            return {}

        return {
            str(key): True
            for key, enabled in value.items()
            if isinstance(
                key,
                str,
            )
            and isinstance(
                enabled,
                bool,
            )
            and enabled
        }

    @staticmethod
    def _normalize_key(
        value: str,
    ) -> str:
        """
        Normalize an entitlement identifier.
        """

        if not isinstance(
            value,
            str,
        ):
            return ""

        return value.strip()


__all__ = [
    "EntitlementService",
]
