"""
Update serializer for the Organizations application.
"""

from __future__ import annotations

from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.organizations.services import (
    update_organization,
)

from .base import OrganizationBaseSerializer
from .fields import _UPDATE_FIELDS


class OrganizationUpdateSerializer(
    OrganizationBaseSerializer,
):
    """
    Serializer used for updating organizations.
    """

    class Meta(
        OrganizationBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS

    def update(
        self,
        instance: Organization,
        validated_data: dict[str, object],
    ) -> Organization:
        """
        Update an organization.
        """

        return update_organization(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "OrganizationUpdateSerializer",
]
