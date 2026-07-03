"""
Detail serializer for the Organizations application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organizations.models import Organization

from .fields import _DETAIL_FIELDS


class OrganizationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer used for retrieving organization details.
    """

    class Meta:
        model = Organization
        fields = _DETAIL_FIELDS
        read_only_fields = _DETAIL_FIELDS


__all__ = [
    "OrganizationDetailSerializer",
]
