"""
Create serializer for the Organization Feature API.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_feature.serializers.base import (
    OrganizationFeatureBaseSerializer,
)
from apps.platform.organizations.api.organization_feature.serializers.fields import (
    _WRITE_FIELDS,
)


class OrganizationFeatureCreateSerializer(
    OrganizationFeatureBaseSerializer,
):
    """
    Serializer used when creating an organization feature entitlement.
    """

    class Meta(
        OrganizationFeatureBaseSerializer.Meta,
    ):
        fields = _WRITE_FIELDS


__all__: tuple[str, ...] = ("OrganizationFeatureCreateSerializer",)
