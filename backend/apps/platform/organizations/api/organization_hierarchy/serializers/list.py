"""
List serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from rest_framework import serializers

from .fields import _LIST_FIELDS


class OrganizationHierarchyListSerializer(
    serializers.ModelSerializer,
):
    """
    List serializer.
    """

    class Meta:
        model = OrganizationHierarchy

        fields = _LIST_FIELDS

        read_only_fields = fields


__all__ = [
    "OrganizationHierarchyListSerializer",
]
