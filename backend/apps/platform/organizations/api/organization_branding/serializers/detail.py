"""
Detail serializer for OrganizationBranding.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_branding.serializers.base import (
    OrganizationBrandingBaseSerializer,
)
from apps.platform.organizations.api.organization_branding.serializers.fields import (
    _DETAIL_FIELDS,
)


class OrganizationBrandingDetailSerializer(
    OrganizationBrandingBaseSerializer,
):
    """
    Serializer for retrieving organization branding details.
    """

    class Meta(
        OrganizationBrandingBaseSerializer.Meta,
    ):
        fields = _DETAIL_FIELDS
        read_only_fields = fields


__all__: tuple[str, ...] = ("OrganizationBrandingDetailSerializer",)
