"""
Provider update serializer.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.clinical.providers.api.serializers.base import (
    ProviderBaseSerializer,
)
from apps.clinical.providers.api.serializers.fields import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)
from apps.clinical.providers.models import Provider
from apps.clinical.providers.services import (
    ProviderService,
)


class ProviderUpdateSerializer(
    ProviderBaseSerializer,
):
    """
    Serializer used for provider updates.
    """

    class Meta(
        ProviderBaseSerializer.Meta,
    ):
        fields = UPDATE_FIELDS

        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: Provider,
        validated_data: Mapping[str, Any],
    ) -> Provider:
        """
        Update and return a provider.
        """

        return ProviderService.update(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "ProviderUpdateSerializer",
]
