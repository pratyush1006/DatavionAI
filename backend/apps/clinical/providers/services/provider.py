"""
Provider services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.clinical.providers.models import Provider


class ProviderService:
    """
    Service layer for provider write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
    ) -> Provider:
        """
        Create a new provider.
        """

        provider = Provider(
            **validated_data,
        )

        provider.full_clean()

        provider.save()

        return provider

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Provider,
        validated_data: Mapping[str, Any],
    ) -> Provider:
        """
        Update an existing provider.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save(
            update_fields=[
                *validated_data.keys(),
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Provider,
    ) -> None:
        """
        Delete a provider.
        """

        instance.delete()

    @staticmethod
    @transaction.atomic
    def archive(
        *,
        instance: Provider,
    ) -> Provider:
        """
        Archive a provider.
        """

        instance.is_active = False

        instance.full_clean()

        instance.save(
            update_fields=[
                "is_active",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        instance: Provider,
    ) -> Provider:
        """
        Restore an archived provider.
        """

        instance.is_active = True

        instance.full_clean()

        instance.save(
            update_fields=[
                "is_active",
                "updated_at",
            ],
        )

        return instance


# ---------------------------------------------------------------------
# Backward-compatible aliases
# ---------------------------------------------------------------------

create_provider = ProviderService.create
update_provider = ProviderService.update
delete_provider = ProviderService.delete


__all__ = [
    "ProviderService",
    "create_provider",
    "update_provider",
    "delete_provider",
]
