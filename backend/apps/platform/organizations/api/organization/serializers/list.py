"""
List serializer for the Organizations application.
"""

from __future__ import annotations

from .base import OrganizationBaseSerializer
from .fields import (
    _LIST_FIELDS,
)


class OrganizationListSerializer(
    OrganizationBaseSerializer,
):
    """
    Serializer used for listing organizations.
    """

    class Meta(
        OrganizationBaseSerializer.Meta,
    ):
        fields = _LIST_FIELDS
        read_only_fields = _LIST_FIELDS


__all__ = [
    "OrganizationListSerializer",
]
