"""
Base serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.common.api.serializers.base import (
    BaseModelSerializer,
)
from apps.platform.organizations.models import (
    OrganizationHierarchy,
)


class OrganizationHierarchyBaseSerializer(
    BaseModelSerializer,
):
    """
    Base serializer for OrganizationHierarchy.
    """

    class Meta:
        model = OrganizationHierarchy
        fields: tuple[str, ...] = ()


__all__: tuple[str, ...] = ("OrganizationHierarchyBaseSerializer",)
