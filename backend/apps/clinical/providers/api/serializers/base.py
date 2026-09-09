"""
Base provider serializer.

Shared validation and normalization
for Provider API serializers.
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

    @staticmethod
    def _normalize_text(
        value: str | None,
    ) -> str:
        """
        Normalize text input.
        """

        if not value:
            return ""

        return value.strip()

    def validate_provider_number(
        self,
        value: str,
    ) -> str:
        """
        Validate provider identifier.
        """

        return self._normalize_text(
            value,
        ).upper()

    def validate_bio(
        self,
        value: str,
    ) -> str:
        """
        Validate provider biography.
        """

        return self._normalize_text(
            value,
        )

    class Meta(
        ProviderFieldsSerializer.Meta,
    ):
        """
        Serializer metadata.
        """

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


__all__ = ("ProviderBaseSerializer",)
