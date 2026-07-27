"""
List serializer for the Organization Feature API.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_feature.serializers.base import (
    OrganizationFeatureBaseSerializer,
)
from apps.platform.organizations.api.organization_feature.serializers.fields import (
    _LIST_FIELDS,
)


class OrganizationFeatureListSerializer(
    OrganizationFeatureBaseSerializer,
):
    """
    Serializer used for listing organization feature entitlements.
    """

    class Meta(
        OrganizationFeatureBaseSerializer.Meta,
    ):
        fields = _LIST_FIELDS


__all__: tuple[str, ...] = ("OrganizationFeatureListSerializer",)
