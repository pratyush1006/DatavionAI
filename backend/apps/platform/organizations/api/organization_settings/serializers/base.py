"""
Base serializer for OrganizationSettings.
"""

from __future__ import annotations

from apps.common.api.serializers.base import (
    BaseModelSerializer,
)
from apps.platform.organizations.models import (
    OrganizationSettings,
)


class OrganizationSettingsBaseSerializer(
    BaseModelSerializer,
):
    """
    Base serializer for OrganizationSettings.

    Shared serializer configuration belongs here.
    """

    class Meta:
        model = OrganizationSettings

        fields: tuple[str, ...] = ()


__all__: tuple[str, ...] = ("OrganizationSettingsBaseSerializer",)
