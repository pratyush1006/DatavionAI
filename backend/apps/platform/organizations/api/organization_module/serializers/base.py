"""
Base serializers for the Module application.
"""

from __future__ import annotations

from apps.common.api.serializers.base import BaseModelSerializer
from apps.platform.organizations.models import OrganizationModule


class OrganizationModuleBaseSerializer(
    BaseModelSerializer,
):
    """
    Base serializer for Module serializers.
    """

    class Meta:
        model = OrganizationModule
        fields: tuple[str, ...] = ()


__all__ = [
    "OrganizationModuleBaseSerializer",
]
