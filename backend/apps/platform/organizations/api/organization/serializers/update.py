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
    Serializer used for updating organizations.

    Validation only.
    Object updates are delegated to UpdateServiceMixin.
    """

    class Meta(
        OrganizationBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS


__all__: tuple[str, ...] = ("OrganizationUpdateSerializer",)
