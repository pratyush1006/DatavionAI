"""
List serializer for storage assets.
"""

from __future__ import annotations

from apps.storage.api.serializers.base import BaseAssetSerializer


class AssetListSerializer(BaseAssetSerializer):
    """
    Serializer for listing storage assets.
    """

    class Meta(BaseAssetSerializer.Meta):
        fields = (
            "id",
            "name",
            "original_name",
            "category",
            "mime_type",
            "size",
            "visibility",
            "status",
            "created_at",
        )
