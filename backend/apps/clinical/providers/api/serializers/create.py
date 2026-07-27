"""
Provider create serializer.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.clinical.providers.api.serializers.base import (
    ProviderBaseSerializer,
)
from apps.clinical.providers.api.serializers.fields import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)
from apps.clinical.providers.models import Provider
from apps.clinical.providers.services import (
    ProviderService,
)


class ProviderCreateSerializer(
    ProviderBaseSerializer,
):
    """
    Serializer used for provider creation.
    """

    class Meta(
        ProviderBaseSerializer.Meta,
    ):
        fields = WRITE_FIELDS

        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: Mapping[str, Any],
    ) -> Provider:
        """
        Create and return a provider.
        """

        return ProviderService.create(
            validated_data=validated_data,
        )


__all__ = [
    "ProviderCreateSerializer",
]
