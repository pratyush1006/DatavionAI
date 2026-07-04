"""
Provider list serializer.
"""

from __future__ import annotations

from apps.providers.api.serializers.base import (
    ProviderBaseSerializer,
)


class ProviderListSerializer(
    ProviderBaseSerializer,
):
    """
    Serializer used when listing providers.
    """
