"""
Platform feature flag resolver.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model

User = get_user_model()


class FeatureFlagResolver:
    """
    Resolve feature flags available for the current user.
    """

    def resolve(
        self,
        *,
        user: User,
    ) -> dict[str, bool]:
        """
        Return enabled feature flags.
        """

        if not user.is_authenticated:
            return {}

        return {
            "dashboard": True,
            "notifications": True,
            "search": True,
            "audit_logs": user.is_staff,
            "administration": user.is_staff,
            "ai_copilot": False,
            "analytics": False,
            "billing": False,
            "voice_assistant": False,
            "ocr": False,
        }

    def enabled(
        self,
        *,
        user: User,
        feature: str,
    ) -> bool:
        """
        Check whether a feature is enabled.
        """

        return self.resolve(
            user=user,
        ).get(
            feature,
            False,
        )


feature_flag_resolver = FeatureFlagResolver()


__all__ = [
    "FeatureFlagResolver",
    "feature_flag_resolver",
]
