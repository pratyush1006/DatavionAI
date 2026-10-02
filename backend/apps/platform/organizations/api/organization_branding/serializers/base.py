"""
Base serializer for OrganizationBranding.
"""

from __future__ import annotations

from apps.common.api.serializers.base import (
    BaseModelSerializer,
)
from apps.platform.organizations.models import (
    OrganizationBranding,
)


class OrganizationBrandingBaseSerializer(
    BaseModelSerializer,
):
    """
    Base serializer for OrganizationBranding.

    Shared serializer configuration should be placed here.
    """

    class Meta:
        model = OrganizationBranding


__all__: tuple[str, ...] = ("OrganizationBrandingBaseSerializer",)
