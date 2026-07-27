"""
List serializer for OrganizationSettings.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_settings.serializers.base import (
    OrganizationSettingsBaseSerializer,
)
from apps.platform.organizations.api.organization_settings.serializers.fields import (
    _LIST_FIELDS,
)


class OrganizationSettingsListSerializer(
    OrganizationSettingsBaseSerializer,
):
    """
    Serializer for listing organization settings.
    """

    class Meta(
        OrganizationSettingsBaseSerializer.Meta,
    ):
        fields = _LIST_FIELDS

        read_only_fields = fields


__all__: tuple[str, ...] = ("OrganizationSettingsListSerializer",)
