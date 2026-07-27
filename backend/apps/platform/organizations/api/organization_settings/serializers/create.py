"""
Create serializer for OrganizationSettings.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_settings.serializers.base import (
    OrganizationSettingsBaseSerializer,
)
from apps.platform.organizations.api.organization_settings.serializers.fields import (
    _WRITE_FIELDS,
)


class OrganizationSettingsCreateSerializer(
    OrganizationSettingsBaseSerializer,
):
    """
    Serializer for creating organization settings.

    Validation only.

    Object creation is delegated to CreateServiceMixin
    and the OrganizationSettings service layer.
    """

    class Meta(
        OrganizationSettingsBaseSerializer.Meta,
    ):
        fields = _WRITE_FIELDS


__all__: tuple[str, ...] = ("OrganizationSettingsCreateSerializer",)
