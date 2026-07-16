"""
Detail serializer for configurations.
"""

from __future__ import annotations

from apps.configuration.api.serializers.base import (
    BaseConfigurationSerializer,
)


class ConfigurationDetailSerializer(BaseConfigurationSerializer):
    """
    Serializer for configuration details.
    """

    class Meta(BaseConfigurationSerializer.Meta):
        fields = BaseConfigurationSerializer.Meta.fields
