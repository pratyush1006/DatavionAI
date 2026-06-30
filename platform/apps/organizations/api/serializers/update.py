"""
Update serializer for organizations.
"""

from __future__ import annotations

from .base import OrganizationBaseSerializer
from .fields import UPDATE_FIELDS


class OrganizationUpdateSerializer(OrganizationBaseSerializer):
    """
    Serializer for updating organizations.
    """

    class Meta(OrganizationBaseSerializer.Meta):
        fields = UPDATE_FIELDS
