"""
Provider domain services.

Handles provider write operations.

Lifecycle orchestration is performed
by workflows.

Services are responsible for:

- Domain validation
- Database writes
- State transitions
- Transaction boundaries
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.clinical.providers.constants import (
    ProviderStatus,
)
from apps.clinical.providers.models import Provider


class ProviderService:
    """
    Provider domain write service.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
    ) -> Provider:
        """
        Create provider profile.
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
        Update provider profile.
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
    def verify(
        *,
        instance: Provider,
    ) -> Provider:
        """
        Move provider to verified state.
        """

        instance.status = ProviderStatus.VERIFIED

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: Provider,
    ) -> Provider:
        """
        Activate provider.
        """

        instance.status = ProviderStatus.ACTIVE

        instance.is_accepting_patients = True

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "is_accepting_patients",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        instance: Provider,
    ) -> Provider:
        """
        Deactivate provider.
        """

        instance.status = ProviderStatus.INACTIVE

        instance.is_accepting_patients = False

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "is_accepting_patients",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def suspend(
        *,
        instance: Provider,
    ) -> Provider:
        """
        Suspend provider.
        """

        instance.status = ProviderStatus.SUSPENDED

        instance.is_accepting_patients = False

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "is_accepting_patients",
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
        Soft delete provider.
        """

        instance.delete()

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        instance: Provider,
    ) -> Provider:
        """
        Restore provider.
        """

        instance.restore()

        return instance


# Backward compatibility

create_provider = ProviderService.create
update_provider = ProviderService.update
delete_provider = ProviderService.delete


__all__ = [
    "ProviderService",
    "create_provider",
    "update_provider",
    "delete_provider",
]
