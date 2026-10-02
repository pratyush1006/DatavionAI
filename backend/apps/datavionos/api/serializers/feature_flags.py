"""
Platform feature flag serializer.

Serializes effective DatavionOS runtime feature flags.
"""

from __future__ import annotations

from rest_framework import serializers


class FeatureFlagSerializer(
    serializers.Serializer,
):
    """
    Serializer for platform runtime feature flags.

    These flags control dynamic SaaS capabilities
    exposed to the frontend runtime.
    """

    #
    # Core platform
    #
    dashboard = serializers.BooleanField(
        default=False,
    )

    notifications = serializers.BooleanField(
        default=False,
    )

    search = serializers.BooleanField(
        default=False,
    )

    #
    # Enterprise controls
    #
    audit_logs = serializers.BooleanField(
        default=False,
    )

    administration = serializers.BooleanField(
        default=False,
    )

    #
    # AI platform
    #
    ai_copilot = serializers.BooleanField(
        default=False,
    )

    ai_assistant = serializers.BooleanField(
        default=False,
    )

    ai_workflows = serializers.BooleanField(
        default=False,
    )

    #
    # Analytics
    #
    analytics = serializers.BooleanField(
        default=False,
    )

    #
    # Commercial
    #
    billing = serializers.BooleanField(
        default=False,
    )

    #
    # AI services
    #
    voice_assistant = serializers.BooleanField(
        default=False,
    )

    ocr = serializers.BooleanField(
        default=False,
    )

    #
    # Clinical capabilities
    #
    appointments = serializers.BooleanField(
        default=False,
    )


__all__ = [
    "FeatureFlagSerializer",
]
