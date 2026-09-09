"""
Provider creation serializer.

Responsible for:

- Validating provider creation payload
- Normalizing provider input
- Preparing workflow input

Business rules do not belong here.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.providers.models import (
    Provider,
)


class ProviderCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Provider creation serializer.

    Used by:

        ProviderListCreateAPIView
                |
                v
        ProviderCreationWorkflow
    """

    class Meta:
        model = Provider

        fields = (
            "employee",
            "provider_number",
            "provider_type",
            "years_of_experience",
            "is_accepting_patients",
            "bio",
        )

    def validate_provider_number(
        self,
        value: str,
    ) -> str:
        """
        Normalize provider number.
        """

        return value.strip().upper()

    def validate_bio(
        self,
        value: str,
    ) -> str:
        """
        Normalize biography.
        """

        return value.strip()


__all__ = ("ProviderCreateSerializer",)
