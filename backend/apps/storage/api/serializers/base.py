"""
Base serializers for the Storage application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.storage.models import Asset


class BaseAssetSerializer(serializers.ModelSerializer):
    """
    Base serializer for storage assets.
    """

    class Meta:
        model = Asset

        fields = (
            "id",
            "organization",
            "uploaded_by",
            "folder",
            "name",
            "original_name",
            "extension",
            "mime_type",
            "category",
            "size",
            "provider",
            "storage_key",
            "path",
            "checksum",
            "visibility",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "provider",
            "storage_key",
            "path",
            "checksum",
            "status",
            "created_at",
            "updated_at",
        )
