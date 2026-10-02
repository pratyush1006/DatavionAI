"""
Provider detail serializer.
"""

from __future__ import annotations

from apps.clinical.providers.api.serializers.base import (
    ProviderBaseSerializer,
)
from apps.clinical.providers.api.serializers.fields import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class ProviderDetailSerializer(
    ProviderBaseSerializer,
):
    """
    Serializer used for provider details.
    """

    class Meta(
        ProviderBaseSerializer.Meta,
    ):
        fields = DETAIL_FIELDS

        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "ProviderDetailSerializer",
]
