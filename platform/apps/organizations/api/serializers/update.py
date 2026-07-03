"""
Update serializer for the Organizations application.
"""

from __future__ import annotations

from .base import OrganizationBaseSerializer
from .fields import _UPDATE_FIELDS


class OrganizationUpdateSerializer(
    OrganizationBaseSerializer,
):
    """
    Serializer for updating organizations.
    """

    class Meta(
        OrganizationBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS
