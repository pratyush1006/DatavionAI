"""
Create serializer for Organization Branding.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_branding.serializers.base import (
    OrganizationBrandingBaseSerializer,
)
from apps.platform.organizations.api.organization_branding.serializers.fields import (
    _WRITE_FIELDS,
)


class OrganizationBrandingCreateSerializer(
    OrganizationBrandingBaseSerializer,
):
    """
    Serializer for creating organization branding.
    """

    class Meta(
        OrganizationBrandingBaseSerializer.Meta,
    ):
        fields = _WRITE_FIELDS


__all__ = [
    "OrganizationBrandingCreateSerializer",
]
