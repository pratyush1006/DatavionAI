"""
Detail serializer for Organization Module.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_module.serializers.base import (
    OrganizationModuleBaseSerializer,
)
from apps.platform.organizations.api.organization_module.serializers.fields import (
    _DETAIL_FIELDS,
)


class OrganizationModuleDetailSerializer(
    OrganizationModuleBaseSerializer,
):
    """
    Serializer for retrieving organization module entitlement details.
    """

    class Meta(
        OrganizationModuleBaseSerializer.Meta,
    ):
        fields = _DETAIL_FIELDS


__all__ = [
    "OrganizationModuleDetailSerializer",
]
