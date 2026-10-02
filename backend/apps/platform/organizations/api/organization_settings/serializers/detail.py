"""
Detail serializer for OrganizationSettings.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_settings.serializers.base import (
    OrganizationSettingsBaseSerializer,
)
from apps.platform.organizations.api.organization_settings.serializers.fields import (
    _DETAIL_FIELDS,
)


class OrganizationSettingsDetailSerializer(
    OrganizationSettingsBaseSerializer,
):
    """
    Serializer for retrieving organization settings.
    """

    class Meta(
        OrganizationSettingsBaseSerializer.Meta,
    ):
        fields = _DETAIL_FIELDS

        read_only_fields = fields


__all__: tuple[str, ...] = ("OrganizationSettingsDetailSerializer",)
