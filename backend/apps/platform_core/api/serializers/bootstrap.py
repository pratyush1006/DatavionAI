"""
Platform bootstrap serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform_core.api.serializers.branding import (
    BrandingSerializer,
)
from apps.platform_core.api.serializers.dashboard import (
    DashboardCardSerializer,
)
from apps.platform_core.api.serializers.feature_flags import (
    FeatureFlagSerializer,
)
from apps.platform_core.api.serializers.module import (
    PlatformModuleSerializer,
)
from apps.platform_core.api.serializers.navigation import (
    NavigationItemSerializer,
)


class PlatformBootstrapSerializer(serializers.Serializer):
    """
    Serializer for the platform bootstrap response.
    """

    user = serializers.DictField()

    organization = serializers.DictField(
        allow_null=True,
    )

    employee = serializers.DictField(
        allow_null=True,
    )

    roles = serializers.ListField(
        child=serializers.CharField(),
    )

    permissions = serializers.ListField(
        child=serializers.CharField(),
    )

    modules = PlatformModuleSerializer(
        many=True,
    )

    navigation = NavigationItemSerializer(
        many=True,
    )

    dashboard = DashboardCardSerializer(
        many=True,
    )

    branding = BrandingSerializer()

    feature_flags = FeatureFlagSerializer()

    subscription = serializers.DictField(
        required=False,
        allow_null=True,
    )

    preferences = serializers.DictField(
        required=False,
        allow_null=True,
    )


__all__ = [
    "PlatformBootstrapSerializer",
]
