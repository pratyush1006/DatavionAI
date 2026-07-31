"""
Platform feature flag resolver.

Resolves effective feature flags for DatavionOS runtime.

Resolution order:

1. Authentication
2. Platform defaults
3. Tenant subscription feature entitlements
4. Registered module feature flags
5. Staff overrides

Subscription entitlements are the source of truth.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model

from apps.datavionos.registries.module import (
    module_registry,
)
from apps.platform.subscriptions.models import (
    FeatureEntitlement,
)

User = get_user_model()


class FeatureFlagResolver:
    """
    Resolve runtime feature availability.
    """

    def resolve(
        self,
        *,
        user: User,
        tenant=None,
    ) -> dict[str, bool]:
        """
        Resolve effective feature flags.
        """

        if not user.is_authenticated:
            return {}

        flags: dict[str, bool] = {
            "dashboard": True,
            "notifications": True,
            "search": True,
            "audit_logs": False,
            "administration": False,
            "ai_copilot": False,
            "ai_assistant": False,
            "ai_workflows": False,
            "analytics": False,
            "billing": False,
            "voice_assistant": False,
            "ocr": False,
        }

        #
        # Subscription entitlements
        #
        tenant_features = self._get_subscription_features(
            tenant=tenant,
        )

        flags.update(
            tenant_features,
        )

        #
        # Module declared features
        #
        # Modules declare capabilities only.
        # Subscription controls activation.
        #
        for module in module_registry.enabled_modules():
            for feature in module.feature_flags:
                flags.setdefault(
                    feature,
                    False,
                )

        #
        # Staff overrides
        #
        if user.is_staff:
            flags.update(
                {
                    "audit_logs": True,
                    "administration": True,
                }
            )

        return flags

    def _get_subscription_features(
        self,
        *,
        tenant=None,
    ) -> dict[str, bool]:
        """
        Resolve tenant subscription entitlements.
        """

        if tenant is None:
            return {}

        subscription = getattr(
            tenant,
            "subscription",
            None,
        )

        if subscription is None:
            return {}

        return {
            entitlement.feature_key: True
            for entitlement in FeatureEntitlement.objects.filter(
                plan=subscription.plan,
                enabled=True,
            )
        }

    def enabled(
        self,
        *,
        user: User,
        feature: str,
        tenant=None,
    ) -> bool:
        """
        Check feature availability.
        """

        return self.resolve(
            user=user,
            tenant=tenant,
        ).get(
            feature,
            False,
        )


feature_flag_resolver = FeatureFlagResolver()


__all__ = [
    "FeatureFlagResolver",
    "feature_flag_resolver",
]
