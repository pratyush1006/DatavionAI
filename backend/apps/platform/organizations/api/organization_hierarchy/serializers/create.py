"""
Create serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_hierarchy.serializers.base import (
    OrganizationHierarchyBaseSerializer,
)
from apps.platform.organizations.api.organization_hierarchy.serializers.fields import (
    _WRITE_FIELDS,
)


class OrganizationHierarchyCreateSerializer(
    OrganizationHierarchyBaseSerializer,
):
    """
    Serializer for creating an organization hierarchy.
    """

    class Meta(
        OrganizationHierarchyBaseSerializer.Meta,
    ):
        fields = _WRITE_FIELDS


__all__: tuple[str, ...] = ("OrganizationHierarchyCreateSerializer",)
