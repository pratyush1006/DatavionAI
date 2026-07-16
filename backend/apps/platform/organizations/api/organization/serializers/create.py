"""
Create serializer for the Organizations application.
"""

from __future__ import annotations

from apps.platform.organizations.services import (
    create_organization,
)

from .base import OrganizationBaseSerializer
from .fields import _WRITE_FIELDS


class OrganizationCreateSerializer(
    OrganizationBaseSerializer,
):
    """
    Serializer used for creating organizations.
    """

    class Meta(
        OrganizationBaseSerializer.Meta,
    ):
        fields = _WRITE_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create an organization.
        """

        return create_organization(
            validated_data=validated_data,
        )


__all__ = [
    "OrganizationCreateSerializer",
]
