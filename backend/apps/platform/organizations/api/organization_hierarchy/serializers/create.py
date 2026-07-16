"""
Create serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_hierarchy.serializers.fields import (
    _WRITE_FIELDS,
)
from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from apps.platform.organizations.services import (
    create_organization_hierarchy,
)
from rest_framework import serializers


class OrganizationHierarchyCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating an organization hierarchy.
    """

    class Meta:
        model = OrganizationHierarchy

        fields = _WRITE_FIELDS

    def create(
        self,
        validated_data: dict,
    ) -> OrganizationHierarchy:
        """
        Create an organization hierarchy.
        """

        return create_organization_hierarchy(
            validated_data=validated_data,
        )


__all__ = [
    "OrganizationHierarchyCreateSerializer",
]
