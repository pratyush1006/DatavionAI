"""
Platform feature flag serializer.
"""

from __future__ import annotations

from rest_framework import serializers


class FeatureFlagSerializer(serializers.Serializer):
    """
    Serializer for platform feature flags.
    """

    dashboard = serializers.BooleanField()

    notifications = serializers.BooleanField()

    search = serializers.BooleanField()

    audit_logs = serializers.BooleanField()

    administration = serializers.BooleanField()

    ai_copilot = serializers.BooleanField()

    analytics = serializers.BooleanField()

    billing = serializers.BooleanField()

    voice_assistant = serializers.BooleanField()

    ocr = serializers.BooleanField()


__all__ = [
    "FeatureFlagSerializer",
]
