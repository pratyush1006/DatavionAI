"""
Summary serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization.serializers.fields import (
    _SUMMARY_FIELDS,
)
from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from rest_framework import serializers


class OrganizationHierarchySummarySerializer(
    serializers.ModelSerializer,
):
    """
    Summary serializer.
    """

    class Meta:
        model = OrganizationHierarchy

        fields = _SUMMARY_FIELDS

        read_only_fields = fields


__all__ = [
    "OrganizationHierarchySummarySerializer",
]
