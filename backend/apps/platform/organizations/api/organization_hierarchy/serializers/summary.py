"""
Summary serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_hierarchy.serializers.base import (
    OrganizationHierarchyBaseSerializer,
)
from apps.platform.organizations.api.organization_hierarchy.serializers.fields import (
    _SUMMARY_FIELDS,
)


class OrganizationHierarchySummarySerializer(
    OrganizationHierarchyBaseSerializer,
):
    """
    Summary serializer for organization hierarchy.
    """

    class Meta(
        OrganizationHierarchyBaseSerializer.Meta,
    ):
        fields = _SUMMARY_FIELDS
        read_only_fields = fields


__all__: tuple[str, ...] = ("OrganizationHierarchySummarySerializer",)
