"""
List serializer for configurations.
"""

from __future__ import annotations

from apps.configuration.api.serializers.base import (
    BaseConfigurationSerializer,
)


class ConfigurationListSerializer(BaseConfigurationSerializer):
    """
    Serializer for listing configurations.
    """

    class Meta(BaseConfigurationSerializer.Meta):
        fields = (
            "id",
            "key",
            "category",
            "name",
            "value",
            "value_type",
            "is_editable",
            "created_at",
        )
