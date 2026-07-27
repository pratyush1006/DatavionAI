"""
Update serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_hierarchy.serializers.base import (
    OrganizationHierarchyBaseSerializer,
)
from apps.platform.organizations.api.organization_hierarchy.serializers.fields import (
    _UPDATE_FIELDS,
)


class OrganizationHierarchyUpdateSerializer(
    OrganizationHierarchyBaseSerializer,
):
    """
    Serializer for updating an organization hierarchy.
    """

    class Meta(
        OrganizationHierarchyBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS


__all__: tuple[str, ...] = ("OrganizationHierarchyUpdateSerializer",)
