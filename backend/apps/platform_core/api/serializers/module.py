"""
Platform module serializer.
"""

from __future__ import annotations

from rest_framework import serializers


class PlatformModuleSerializer(serializers.Serializer):
    """
    Serializer for a platform module.
    """

    key = serializers.CharField()

    title = serializers.CharField()

    description = serializers.CharField()

    route = serializers.CharField()

    icon = serializers.CharField()

    category = serializers.CharField()

    permission = serializers.CharField()

    enabled = serializers.BooleanField()

    order = serializers.IntegerField()


__all__ = [
    "PlatformModuleSerializer",
]
