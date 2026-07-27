"""
Detail serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_hierarchy.serializers.base import (
    OrganizationHierarchyBaseSerializer,
)
from apps.platform.organizations.api.organization_hierarchy.serializers.fields import (
    _DETAIL_FIELDS,
)


class OrganizationHierarchyDetailSerializer(
    OrganizationHierarchyBaseSerializer,
):
    """
    Serializer for retrieving organization hierarchy details.
    """

    class Meta(
        OrganizationHierarchyBaseSerializer.Meta,
    ):
        fields = _DETAIL_FIELDS
        read_only_fields = fields


__all__: tuple[str, ...] = ("OrganizationHierarchyDetailSerializer",)
