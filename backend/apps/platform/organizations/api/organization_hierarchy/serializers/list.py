"""
List serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_hierarchy.serializers.base import (
    OrganizationHierarchyBaseSerializer,
)
from apps.platform.organizations.api.organization_hierarchy.serializers.fields import (
    _LIST_FIELDS,
)


class OrganizationHierarchyListSerializer(
    OrganizationHierarchyBaseSerializer,
):
    """
    Serializer for listing organization hierarchies.
    """

    class Meta(
        OrganizationHierarchyBaseSerializer.Meta,
    ):
        fields = _LIST_FIELDS
        read_only_fields = fields


__all__: tuple[str, ...] = ("OrganizationHierarchyListSerializer",)
