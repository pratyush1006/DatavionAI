"""
Create serializer for organizations.
"""

from __future__ import annotations

from .base import OrganizationBaseSerializer
from .fields import WRITE_FIELDS


class OrganizationCreateSerializer(OrganizationBaseSerializer):
    """
    Serializer for creating organizations.
    """

    class Meta(OrganizationBaseSerializer.Meta):
        fields = WRITE_FIELDS

    def validate_code(self, value: str) -> str:
        """
        Normalize organization code.
        """
        return value.strip().upper()
