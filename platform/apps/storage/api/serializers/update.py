"""
Update serializer for storage assets.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.storage.constants import (
    ASSET_VISIBILITY_CHOICES,
)
from apps.storage.models import Folder


class UpdateAssetSerializer(serializers.Serializer):
    """
    Serializer for updating asset metadata.
    """

    name = serializers.CharField(
        max_length=255,
        required=False,
    )

    folder = serializers.PrimaryKeyRelatedField(
        queryset=Folder.objects.all(),
        required=False,
        allow_null=True,
    )

    visibility = serializers.ChoiceField(
        choices=ASSET_VISIBILITY_CHOICES,
        required=False,
    )

    def validate(self, attrs):
        """
        Validate update payload.
        """

        if not attrs:
            raise serializers.ValidationError("At least one field must be provided.")

        return attrs
