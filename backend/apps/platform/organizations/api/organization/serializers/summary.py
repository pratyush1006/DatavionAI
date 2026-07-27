"""
Summary serializer for the Organizations application.
"""

from __future__ import annotations

from .base import OrganizationBaseSerializer
from .fields import _SUMMARY_FIELDS


class OrganizationSummarySerializer(
    OrganizationBaseSerializer,
):
    """
    Serializer used for lightweight organization representations.

    Intended for nested serializers, dropdowns, autocomplete,
    relationship references, and other compact responses.
    """

    class Meta(
        OrganizationBaseSerializer.Meta,
    ):
        fields = _SUMMARY_FIELDS
        read_only_fields = _SUMMARY_FIELDS


__all__: tuple[str, ...] = ("OrganizationSummarySerializer",)
