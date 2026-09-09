"""
Provider specialization services.

Handles provider specialty operations.

Responsibilities:

- Create specialization
- Update specialization
- Remove specialization
- Manage primary specialization

Business workflows should call
these services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.clinical.providers.models import (
    Provider,
    ProviderSpecialization,
)


class ProviderSpecializationService:
    """
    Domain service for provider specialties.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        provider: Provider,
        validated_data: Mapping[str, Any],
    ) -> ProviderSpecialization:
        """
        Create provider specialization.
        """

        specialization = ProviderSpecialization(
            provider=provider,
            **validated_data,
        )

        specialization.full_clean()

        specialization.save()

        if specialization.is_primary:
            ProviderSpecializationService._unset_other_primary(
                specialization,
            )

        return specialization

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: ProviderSpecialization,
        validated_data: Mapping[str, Any],
    ) -> ProviderSpecialization:
        """
        Update specialization.
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

        if instance.is_primary:
            ProviderSpecializationService._unset_other_primary(
                instance,
            )

        return instance

    @staticmethod
    @transaction.atomic
    def set_primary(
        *,
        instance: ProviderSpecialization,
    ) -> ProviderSpecialization:
        """
        Mark specialization as primary.
        """

        ProviderSpecialization.objects.filter(
            provider=instance.provider,
            is_primary=True,
        ).exclude(
            pk=instance.pk,
        ).update(
            is_primary=False,
        )

        instance.is_primary = True

        instance.full_clean()

        instance.save(
            update_fields=[
                "is_primary",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: ProviderSpecialization,
    ) -> None:
        """
        Delete specialization.
        """

        instance.delete()

    @staticmethod
    def _unset_other_primary(
        instance: ProviderSpecialization,
    ) -> None:
        """
        Ensure only one primary specialty exists.
        """

        ProviderSpecialization.objects.filter(
            provider=instance.provider,
            is_primary=True,
        ).exclude(
            pk=instance.pk,
        ).update(
            is_primary=False,
        )


# Backward-compatible aliases

create_provider_specialization = ProviderSpecializationService.create

update_provider_specialization = ProviderSpecializationService.update

delete_provider_specialization = ProviderSpecializationService.delete


__all__ = [
    "ProviderSpecializationService",
    "create_provider_specialization",
    "update_provider_specialization",
    "delete_provider_specialization",
]
