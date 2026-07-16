"""
Provider update serializer.
"""

from __future__ import annotations

from apps.clinical.providers.api.serializers.base import (
    ProviderBaseSerializer,
)


class ProviderUpdateSerializer(
    ProviderBaseSerializer,
):
    """
    Serializer used for provider updates.
    """
