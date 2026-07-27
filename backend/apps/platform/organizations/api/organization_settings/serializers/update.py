"""
Update serializer for OrganizationSettings.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_settings.serializers.base import (
    OrganizationSettingsBaseSerializer,
)
from apps.platform.organizations.api.organization_settings.serializers.fields import (
    _UPDATE_FIELDS,
)


class OrganizationSettingsUpdateSerializer(
    OrganizationSettingsBaseSerializer,
):
    """
    Serializer for updating organization settings.

    Validation only.

    Object updates are delegated to UpdateServiceMixin
    and the OrganizationSettings service layer.
    """

    class Meta(
        OrganizationSettingsBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS


__all__: tuple[str, ...] = ("OrganizationSettingsUpdateSerializer",)
