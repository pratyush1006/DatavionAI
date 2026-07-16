"""
Base provider serializer.
"""

from __future__ import annotations

from apps.clinical.providers.api.serializers.fields import (
    ProviderFieldsSerializer,
)


class ProviderBaseSerializer(
    ProviderFieldsSerializer,
):
    """
    Base serializer shared by provider serializers.
    """

    class Meta(
        ProviderFieldsSerializer.Meta,
    ):
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
