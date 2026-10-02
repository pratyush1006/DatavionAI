"""
Update serializer for Organization Branding.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_branding.serializers.base import (
    OrganizationBrandingBaseSerializer,
)
from apps.platform.organizations.api.organization_branding.serializers.fields import (
    _UPDATE_FIELDS,
)


class OrganizationBrandingUpdateSerializer(
    OrganizationBrandingBaseSerializer,
):
    """
    Serializer for updating organization branding.
    """

    class Meta(
        OrganizationBrandingBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS


__all__ = [
    "OrganizationBrandingUpdateSerializer",
]
