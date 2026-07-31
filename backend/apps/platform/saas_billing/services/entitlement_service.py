"""
Entitlement services.

Business logic layer for DatavionOS SaaS
feature, module and capability access.

Responsibilities:

- Resolve enabled modules
- Resolve feature permissions
- Resolve subscription limits
- Validate access
- Generate frontend capabilities
- Support dynamic SaaS dashboards

Architecture:

Organization
      |
Subscription
      |
Plan Snapshot
      |
EntitlementService
      |
      +── Modules
      |
      +── Features
      |
      +── Limits
      |
      +── Capabilities
"""

from __future__ import annotations

from django.utils import timezone

from apps.platform.saas_billing.models import (
    Subscription,
)


class EntitlementService:
    """
    Enterprise SaaS entitlement service.
    """

    ACTIVE_STATUSES = {
        Subscription.Status.TRIAL,
        Subscription.Status.ACTIVE,
    }

    # ==============================================================
    # Subscription Resolver
    # ==============================================================

    @staticmethod
    def get_subscription(
        *,
        organization,
    ) -> Subscription | None:
        """
        Resolve active organization subscription.
        """

        now = timezone.now()

        return (
            Subscription.objects.filter(
                organization=organization,
                status__in=EntitlementService.ACTIVE_STATUSES,
            )
            .filter(
                current_period_end__gte=now,
            )
            .select_related(
                "plan",
            )
            .first()
        )

    # ==============================================================
    # Snapshot
    # ==============================================================

    @staticmethod
    def get_snapshot(
        *,
        organization,
    ) -> dict:

        subscription = EntitlementService.get_subscription(
            organization=organization,
        )

        if not subscription:
            return {}

        return subscription.feature_snapshot or {}

    # ==============================================================
    # Modules
    # ==============================================================

    @staticmethod
    def get_modules(
        *,
        organization,
    ) -> dict:

        return EntitlementService.get_snapshot(
            organization=organization,
        ).get(
            "modules",
            {},
        )

    @staticmethod
    def get_enabled_modules(
        *,
        organization,
    ) -> list[str]:
        """
        Return enabled module names.
        """

        return [
            key
            for key, value in EntitlementService.get_modules(
                organization=organization,
            ).items()
            if value
        ]

    # ==============================================================
    # Features
    # ==============================================================

    @staticmethod
    def get_features(
        *,
        organization,
    ) -> dict:

        return EntitlementService.get_snapshot(
            organization=organization,
        ).get(
            "features",
            {},
        )

    @staticmethod
    def get_enabled_features(
        *,
        organization,
    ) -> list[str]:
        """
        Return enabled features.
        """

        return [
            key
            for key, value in EntitlementService.get_features(
                organization=organization,
            ).items()
            if value
        ]

    # ==============================================================
    # Limits
    # ==============================================================

    @staticmethod
    def get_limits(
        *,
        organization,
    ) -> dict:

        subscription = EntitlementService.get_subscription(
            organization=organization,
        )

        if not subscription:
            return {}

        return subscription.plan_snapshot.get(
            "limits",
            {},
        )

    @staticmethod
    def get_limit(
        *,
        organization,
        key: str,
    ):
        """
        Return single quota value.
        """

        return EntitlementService.get_limits(
            organization=organization,
        ).get(
            key,
        )

    @staticmethod
    def check_limit(
        *,
        organization,
        limit_key: str,
        requested_value: int = 1,
    ) -> bool:

        maximum = EntitlementService.get_limit(
            organization=organization,
            key=limit_key,
        )

        if maximum is None:
            return True

        if isinstance(
            maximum,
            dict,
        ):
            maximum = maximum.get(
                "included",
            )

        return requested_value <= maximum

    # ==============================================================
    # Access Checks
    # ==============================================================

    @staticmethod
    def has_module(
        *,
        organization,
        module: str,
    ) -> bool:

        return bool(
            EntitlementService.get_modules(
                organization=organization,
            ).get(
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

        return bool(
            EntitlementService.get_features(
                organization=organization,
            ).get(
                feature,
                False,
            )
        )

    @staticmethod
    def can_access(
        *,
        organization,
        module: str | None = None,
        feature: str | None = None,
    ) -> bool:

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

    # ==============================================================
    # Frontend Capability Payload
    # ==============================================================

    @staticmethod
    def get_capabilities(
        *,
        organization,
    ) -> dict:
        """
        Payload consumed by Next.js bootstrap.
        """

        subscription = EntitlementService.get_subscription(
            organization=organization,
        )

        if not subscription:
            return {
                "subscription": None,
                "modules": [],
                "features": [],
                "limits": {},
            }

        return {
            "subscription": {
                "status": subscription.status,
                "plan": {
                    "name": subscription.plan.name,
                    "code": subscription.plan.code,
                },
            },
            "modules": (
                EntitlementService.get_enabled_modules(
                    organization=organization,
                )
            ),
            "features": (
                EntitlementService.get_enabled_features(
                    organization=organization,
                )
            ),
            "limits": (
                EntitlementService.get_limits(
                    organization=organization,
                )
            ),
        }


__all__ = [
    "EntitlementService",
]
