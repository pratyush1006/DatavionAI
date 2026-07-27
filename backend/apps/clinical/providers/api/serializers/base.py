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

    @staticmethod
    def _normalize_text(
        value: str,
    ) -> str:
        """
        Normalize text input.
        """

        return value.strip()

    def validate_provider_number(
        self,
        value: str,
    ) -> str:
        """
        Validate the provider number.
        """

        return self._normalize_text(
            value,
        )

    def validate_license_number(
        self,
        value: str,
    ) -> str:
        """
        Validate the license number.
        """

        return self._normalize_text(
            value,
        )

    def validate_bio(
        self,
        value: str,
    ) -> str:
        """
        Validate the provider biography.
        """

        return self._normalize_text(
            value,
        )

    class Meta(
        ProviderFieldsSerializer.Meta,
    ):
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


__all__ = [
    "ProviderBaseSerializer",
]
