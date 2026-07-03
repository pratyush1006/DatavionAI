"""
Create serializer for storage assets.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.storage.constants import (
    ASSET_CATEGORY_CHOICES,
    ASSET_VISIBILITY_CHOICES,
)
from apps.storage.models import Folder


class CreateAssetSerializer(serializers.Serializer):
    """
    Serializer used for uploading assets.
    """

    file = serializers.FileField()

    folder = serializers.PrimaryKeyRelatedField(
        queryset=Folder.objects.all(),
        required=False,
        allow_null=True,
    )

    category = serializers.ChoiceField(
        choices=ASSET_CATEGORY_CHOICES,
    )

    visibility = serializers.ChoiceField(
        choices=ASSET_VISIBILITY_CHOICES,
    )

    def validate_file(self, value):
        """
        Validate uploaded file.
        """

        if value.size == 0:
            raise serializers.ValidationError("Uploaded file cannot be empty.")

        return value
