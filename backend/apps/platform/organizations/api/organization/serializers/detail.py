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
    Serializer used for retrieving a complete organization.

    This serializer exposes the full read-only representation
    of an Organization for retrieve endpoints.
    """

    class Meta(
        OrganizationBaseSerializer.Meta,
    ):
        fields = _DETAIL_FIELDS
        read_only_fields = _DETAIL_FIELDS


__all__: tuple[str, ...] = ("OrganizationDetailSerializer",)
