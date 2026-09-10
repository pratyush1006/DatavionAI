"""
DatavionOS platform navigation serializer.

Serializes the backend-resolved runtime navigation contract consumed
by the frontend bootstrap subsystem.
"""

from __future__ import annotations

from rest_framework import serializers


class NavigationItemSerializer(
    serializers.Serializer,
):
    """
    Serializer for a runtime navigation item.

    Backend navigation is already resolved for:

    - module availability
    - feature entitlements
    - RBAC permissions
    - ordering

    The serializer therefore exposes the complete runtime navigation
    DTO without applying additional business rules.
    """

    title = serializers.CharField(
        read_only=True,
    )

    route = serializers.CharField(
        read_only=True,
    )

    icon = serializers.CharField(
        read_only=True,
    )

    category = serializers.CharField(
        read_only=True,
    )

    permissions = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
    )

    order = serializers.IntegerField(
        read_only=True,
    )


__all__ = (
    "NavigationItemSerializer",
)
