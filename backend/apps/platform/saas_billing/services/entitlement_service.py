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
Plan
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
                status__in=(EntitlementService.ACTIVE_STATUSES),
            )
            .select_related(
                "plan",
            )
            .first()
        )

    @staticmethod
    def get_snapshot(
        *,
        organization,
    ) -> dict:
        """
        Return entitlement snapshot.
        """

        subscription = EntitlementService.get_subscription(
            organization=organization,
        )

        if not subscription:
            return {}

        return subscription.feature_snapshot or {}

    @staticmethod
    def get_modules(
        *,
        organization,
    ) -> dict:
        """
        Return enabled DatavionOS modules.
        """

        snapshot = EntitlementService.get_snapshot(
            organization=organization,
        )

        return snapshot.get(
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

        snapshot = EntitlementService.get_snapshot(
            organization=organization,
        )

        return snapshot.get(
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
        """

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
    def has_module(
        *,
        organization,
        module: str,
    ) -> bool:
        """
        Check module entitlement.

        Examples:

        clinical
        pharmacy
        laboratory
        imaging
        ai
        """

        modules = EntitlementService.get_modules(
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
        Check feature entitlement.
        """

        features = EntitlementService.get_features(
            organization=organization,
        )

        return bool(
            features.get(
                feature,
                False,
            )
        )

    @staticmethod
    def check_limit(
        *,
        organization,
        limit_key: str,
        requested_value: int = 1,
    ) -> bool:
        """
        Validate resource quota.

        Example:

        users
        patients
        storage_gb
        ai_requests
        """

        limits = EntitlementService.get_limits(
            organization=organization,
        )

        maximum = limits.get(
            limit_key,
        )

        if maximum is None:
            return True

        return requested_value <= maximum

    @staticmethod
    def get_capabilities(
        *,
        organization,
    ) -> dict:
        """
        Generate frontend capability payload.

        Used by:

        - Platform Bootstrap API
        - Next.js application
        - Dashboard rendering
        """

        subscription = EntitlementService.get_subscription(
            organization=organization,
        )

        if not subscription:
            return {
                "subscription": None,
                "modules": {},
                "features": {},
                "limits": {},
            }

        return {
            "subscription": {
                "status": (subscription.status),
                "plan": {
                    "name": (subscription.plan.name),
                    "code": (subscription.plan.code),
                },
            },
            "modules": (
                EntitlementService.get_modules(
                    organization=organization,
                )
            ),
            "features": (
                EntitlementService.get_features(
                    organization=organization,
                )
            ),
            "limits": (
                EntitlementService.get_limits(
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
        Generic access checker.
        """

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


__all__ = [
    "EntitlementService",
]
