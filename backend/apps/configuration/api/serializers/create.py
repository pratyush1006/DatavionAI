"""
Create serializer for configurations.
"""

from __future__ import annotations

import re

from rest_framework import serializers

from apps.configuration.constants import (
    CONFIGURATION_CATEGORY_CHOICES,
    CONFIGURATION_TYPE_CHOICES,
)
from apps.configuration.models import Configuration

KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")


class CreateConfigurationSerializer(serializers.Serializer):
    """
    Serializer for creating a configuration.
    """

    key = serializers.CharField(
        max_length=100,
    )

    category = serializers.ChoiceField(
        choices=CONFIGURATION_CATEGORY_CHOICES,
    )

    name = serializers.CharField(
        max_length=255,
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    value = serializers.CharField()

    value_type = serializers.ChoiceField(
        choices=CONFIGURATION_TYPE_CHOICES,
    )

    is_editable = serializers.BooleanField(
        default=True,
    )

    def validate_key(self, value: str) -> str:
        """
        Validate the configuration key.
        """

        value = value.strip().upper()

        if not KEY_PATTERN.fullmatch(value):
            raise serializers.ValidationError(
                "Configuration key must contain only uppercase letters, numbers, and underscores."
            )

        if Configuration.objects.filter(
            key=value,
        ).exists():
            raise serializers.ValidationError(
                "A configuration with this key already exists."
            )

        return value

    def validate(self, attrs: dict) -> dict:
        """
        Validate the configuration payload.
        """

        return attrs
