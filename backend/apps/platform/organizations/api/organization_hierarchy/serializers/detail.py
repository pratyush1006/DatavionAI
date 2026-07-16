"""
Detail serializer for OrganizationHierarchy.
"""

from __future__ import annotations

from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from rest_framework import serializers

from .fields import _DETAIL_FIELDS


class OrganizationHierarchyDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Detail serializer.
    """

    class Meta:
        model = OrganizationHierarchy

        fields = _DETAIL_FIELDS

        read_only_fields = fields
