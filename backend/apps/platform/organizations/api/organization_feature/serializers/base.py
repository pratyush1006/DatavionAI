"""
Base serializers for the Feature application.
"""

from __future__ import annotations

from apps.common.api.serializers.base import BaseModelSerializer
from apps.platform.organizations.models import OrganizationFeature


class OrganizationFeatureBaseSerializer(
    BaseModelSerializer,
):
    """
    Base serializer for Feature serializers.
    """

    class Meta:
        model = OrganizationFeature
        fields: tuple[str, ...] = ()


__all__ = [
    "OrganizationFeatureBaseSerializer",
]
