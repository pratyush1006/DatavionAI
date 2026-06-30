"""
List serializer for organizations.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organizations.models import Organization

from .fields import LIST_FIELDS


class OrganizationListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing organizations.
    """

    class Meta:
        model = Organization
        fields = LIST_FIELDS
        read_only_fields = LIST_FIELDS
