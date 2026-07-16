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
    Serializer used for organization summary responses.
    """

    class Meta(
        OrganizationBaseSerializer.Meta,
    ):
        fields = _SUMMARY_FIELDS
        read_only_fields = _SUMMARY_FIELDS


__all__ = [
    "OrganizationSummarySerializer",
]
