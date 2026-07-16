"""
Provider detail serializer.
"""

from __future__ import annotations

from apps.clinical.providers.api.serializers.base import (
    ProviderBaseSerializer,
)


class ProviderDetailSerializer(
    ProviderBaseSerializer,
):
    """
    Serializer used for provider details.
    """
