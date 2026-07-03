"""
Base serializers for the Configuration application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.configuration.models import Configuration


class BaseConfigurationSerializer(serializers.ModelSerializer):
    """
    Base serializer for configuration objects.
    """

    class Meta:
        model = Configuration

        fields = (
            "id",
            "key",
            "category",
            "name",
            "description",
            "value",
            "value_type",
            "is_editable",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
