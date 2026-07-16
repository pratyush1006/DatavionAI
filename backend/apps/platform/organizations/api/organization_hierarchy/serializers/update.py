"""
Update serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_hierarchy.serializers.fields import (
    _UPDATE_FIELDS,
)
from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from apps.platform.organizations.services import (
    update_organization_hierarchy,
)
from rest_framework import serializers


class OrganizationHierarchyUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating an organization hierarchy.
    """

    class Meta:
        model = OrganizationHierarchy

        fields = _UPDATE_FIELDS

    def update(
        self,
        instance: OrganizationHierarchy,
        validated_data: dict,
    ) -> OrganizationHierarchy:
        """
        Update an organization hierarchy.
        """

        return update_organization_hierarchy(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "OrganizationHierarchyUpdateSerializer",
]
