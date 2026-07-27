"""
Platform dashboard serializer.
"""

from __future__ import annotations

from rest_framework import serializers


class DashboardCardSerializer(serializers.Serializer):
    """
    Serializer for a dashboard card.
    """

    key = serializers.CharField()

    title = serializers.CharField()

    description = serializers.CharField()

    icon = serializers.CharField()

    route = serializers.CharField()

    category = serializers.CharField()

    order = serializers.IntegerField()


__all__ = [
    "DashboardCardSerializer",
]
