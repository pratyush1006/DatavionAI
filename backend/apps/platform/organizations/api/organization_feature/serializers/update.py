"""
Update serializer for the Organization Feature API.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_feature.serializers.base import (
    OrganizationFeatureBaseSerializer,
)
from apps.platform.organizations.api.organization_feature.serializers.fields import (
    _UPDATE_FIELDS,
)


class OrganizationFeatureUpdateSerializer(
    OrganizationFeatureBaseSerializer,
):
    """
    Serializer used when updating an organization feature entitlement.
    """

    class Meta(
        OrganizationFeatureBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS


__all__: tuple[str, ...] = ("OrganizationFeatureUpdateSerializer",)
