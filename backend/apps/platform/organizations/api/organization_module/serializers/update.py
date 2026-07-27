"""
Update serializer for Organization Module.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_module.serializers.base import (
    OrganizationModuleBaseSerializer,
)
from apps.platform.organizations.api.organization_module.serializers.fields import (
    _UPDATE_FIELDS,
)


class OrganizationModuleUpdateSerializer(
    OrganizationModuleBaseSerializer,
):
    """
    Serializer for updating organization module entitlements.
    """

    class Meta(
        OrganizationModuleBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS


__all__ = [
    "OrganizationModuleUpdateSerializer",
]
