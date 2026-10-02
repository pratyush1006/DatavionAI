"""
Create serializer for the Organizations application.
"""

from __future__ import annotations

from .base import OrganizationBaseSerializer
from .fields import _WRITE_FIELDS


class OrganizationCreateSerializer(
    OrganizationBaseSerializer,
):
    """
    Serializer used for creating organizations.

    Validation only.
    Object creation is delegated to CreateServiceMixin.
    """

    class Meta(
        OrganizationBaseSerializer.Meta,
    ):
        fields = _WRITE_FIELDS


__all__: tuple[str, ...] = ("OrganizationCreateSerializer",)
