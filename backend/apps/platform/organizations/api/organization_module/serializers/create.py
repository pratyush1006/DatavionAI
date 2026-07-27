"""
Create serializer for Organization Module.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_module.serializers.base import (
    OrganizationModuleBaseSerializer,
)
from apps.platform.organizations.api.organization_module.serializers.fields import (
    _WRITE_FIELDS,
)


class OrganizationModuleCreateSerializer(
    OrganizationModuleBaseSerializer,
):
    """
    Serializer for creating organization module entitlements.
    """

    class Meta(
        OrganizationModuleBaseSerializer.Meta,
    ):
        fields = _WRITE_FIELDS


__all__ = [
    "OrganizationModuleCreateSerializer",
]
