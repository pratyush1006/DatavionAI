"""
Platform navigation serializer.
"""

from __future__ import annotations

from rest_framework import serializers


class NavigationItemSerializer(serializers.Serializer):
    """
    Serializer for a navigation item.
    """

    title = serializers.CharField()

    route = serializers.CharField()

    icon = serializers.CharField()

    category = serializers.CharField()


__all__ = [
    "NavigationItemSerializer",
]
