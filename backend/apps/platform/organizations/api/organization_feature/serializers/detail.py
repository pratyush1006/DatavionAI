"""
Detail serializer for the Organization Feature API.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_feature.serializers.base import (
    OrganizationFeatureBaseSerializer,
)
from apps.platform.organizations.api.organization_feature.serializers.fields import (
    _DETAIL_FIELDS,
)


class OrganizationFeatureDetailSerializer(
    OrganizationFeatureBaseSerializer,
):
    """
    Serializer used for retrieving a single organization feature entitlement.
    """

    class Meta(
        OrganizationFeatureBaseSerializer.Meta,
    ):
        fields = _DETAIL_FIELDS
        read_only_fields = _DETAIL_FIELDS


__all__: tuple[str, ...] = ("OrganizationFeatureDetailSerializer",)
