"""
List serializer for the Organizations application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organizations.models import Organization

from .fields import (
    _LIST_FIELDS,
)


class OrganizationListSerializer(serializers.ModelSerializer):
    """
    Serializer used for listing organizations.
    """

    class Meta:
        model = Organization
        fields = _LIST_FIELDS
        read_only_fields = _LIST_FIELDS


__all__ = [
    "OrganizationListSerializer",
]
