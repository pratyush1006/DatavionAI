"""
Detail serializer for organizations.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organizations.models import Organization

from .fields import DETAIL_FIELDS


class OrganizationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving organization details.
    """

    class Meta:
        model = Organization
        fields = DETAIL_FIELDS
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
