"""
Update serializer for configurations.
"""

from __future__ import annotations

from typing import Any

from rest_framework import serializers

from apps.configuration.constants import (
    CONFIGURATION_CATEGORY_CHOICES,
)


class UpdateConfigurationSerializer(serializers.Serializer):
    """
    Serializer for updating a configuration.
    """

    category = serializers.ChoiceField(
        choices=CONFIGURATION_CATEGORY_CHOICES,
        required=False,
    )

    name = serializers.CharField(
        max_length=255,
        required=False,
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    value = serializers.CharField(
        required=False,
    )

    is_editable = serializers.BooleanField(
        required=False,
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the update payload.
        """

        if not attrs:
            raise serializers.ValidationError("At least one field must be provided.")

        return attrs

    def validate_value(self, value: str) -> str:
        """
        Validate the configuration value.
        """

        if not value.strip():
            raise serializers.ValidationError("Configuration value cannot be empty.")

        return value
