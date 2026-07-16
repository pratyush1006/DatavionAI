"""
Detail serializer for storage assets.
"""

from __future__ import annotations

from apps.storage.api.serializers.base import BaseAssetSerializer


class AssetDetailSerializer(BaseAssetSerializer):
    """
    Serializer for storage asset details.
    """

    class Meta(BaseAssetSerializer.Meta):
        fields = BaseAssetSerializer.Meta.fields
