"""
Provider list serializer.
"""

from __future__ import annotations

from apps.clinical.providers.api.serializers.base import (
    ProviderBaseSerializer,
)
from apps.clinical.providers.api.serializers.fields import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class ProviderListSerializer(
    ProviderBaseSerializer,
):
    """
    Serializer used when listing providers.
    """

    class Meta(
        ProviderBaseSerializer.Meta,
    ):
        fields = LIST_FIELDS

        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "ProviderListSerializer",
]
