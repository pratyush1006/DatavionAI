"""
Platform module serializer.

Serializes DatavionOS module contracts.
"""

from __future__ import annotations

from rest_framework import serializers


class PlatformModuleSerializer(
    serializers.Serializer,
):
    """
    Serializer for a DatavionOS platform module.

    Maps directly to ModuleContract.
    """

    identifier = serializers.CharField()

    name = serializers.CharField()

    display_name = serializers.CharField()

    description = serializers.CharField()

    version = serializers.CharField()

    category = serializers.CharField()

    route = serializers.CharField()

    api_prefix = serializers.CharField()

    icon = serializers.CharField()

    permissions = serializers.ListField(
        child=serializers.CharField(),
    )

    enabled = serializers.BooleanField()

    system = serializers.BooleanField()

    tenant_scoped = serializers.BooleanField()

    order = serializers.IntegerField()

    tags = serializers.ListField(
        child=serializers.CharField(),
    )

    feature_flags = serializers.ListField(
        child=serializers.CharField(),
    )


__all__ = ("PlatformModuleSerializer",)
