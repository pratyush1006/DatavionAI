"""
List serializer for Organization Branding.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_branding.serializers.base import (
    OrganizationBrandingBaseSerializer,
)
from apps.platform.organizations.api.organization_branding.serializers.fields import (
    _LIST_FIELDS,
)


class OrganizationBrandingListSerializer(
    OrganizationBrandingBaseSerializer,
):
    """
    Serializer for listing organization branding.
    """

    class Meta(
        OrganizationBrandingBaseSerializer.Meta,
    ):
        fields = _LIST_FIELDS


__all__ = [
    "OrganizationBrandingListSerializer",
]
