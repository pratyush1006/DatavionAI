"""
Detail serializer for the Organizations application.
"""

from __future__ import annotations

from .base import OrganizationBaseSerializer
from .fields import _DETAIL_FIELDS


class OrganizationDetailSerializer(
    OrganizationBaseSerializer,
):
    """
    Serializer used for retrieving organization details.
    """

    class Meta(
        OrganizationBaseSerializer.Meta,
    ):
        fields = _DETAIL_FIELDS
        read_only_fields = _DETAIL_FIELDS


__all__ = [
    "OrganizationDetailSerializer",
]
