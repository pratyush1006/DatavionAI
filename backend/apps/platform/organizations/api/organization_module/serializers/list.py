"""
List serializer for Organization Module.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_module.serializers.base import (
    OrganizationModuleBaseSerializer,
)
from apps.platform.organizations.api.organization_module.serializers.fields import (
    _LIST_FIELDS,
)


class OrganizationModuleListSerializer(
    OrganizationModuleBaseSerializer,
):
    """
    Serializer for listing organization module entitlements.
    """

    class Meta(
        OrganizationModuleBaseSerializer.Meta,
    ):
        fields = _LIST_FIELDS


__all__ = [
    "OrganizationModuleListSerializer",
]
