"""
Create serializer for the Organizations application.
"""

from __future__ import annotations

from .base import OrganizationBaseSerializer
from .fields import _WRITE_FIELDS


class OrganizationCreateSerializer(OrganizationBaseSerializer):
    """
    Serializer used for creating organizations.
    """

    class Meta(OrganizationBaseSerializer.Meta):
        fields = _WRITE_FIELDS

    def validate_code(
        self,
        value: str,
    ) -> str:
        """
        Normalize the organization code.
        """

        return value.strip().upper()


__all__ = [
    "OrganizationCreateSerializer",
]
