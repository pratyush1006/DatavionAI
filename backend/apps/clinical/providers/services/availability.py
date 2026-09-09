"""
Provider availability services.

Handles provider schedule
and availability lifecycle.

Responsibilities:

- Create availability slots
- Update availability slots
- Activate availability
- Disable availability
- Delete availability

Workflow layer controls
business orchestration.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.clinical.providers.constants import (
    AvailabilityStatus,
)
from apps.clinical.providers.models import (
    Provider,
    ProviderAvailability,
)


class ProviderAvailabilityService:
    """
    Domain service for provider availability.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        provider: Provider,
        validated_data: Mapping[str, Any],
    ) -> ProviderAvailability:
        """
        Create provider availability.
        """

        availability = ProviderAvailability(
            provider=provider,
            **validated_data,
        )

        availability.full_clean()

        availability.save()

        return availability

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: ProviderAvailability,
        validated_data: Mapping[str, Any],
    ) -> ProviderAvailability:
        """
        Update provider availability.
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
    def activate(
        *,
        instance: ProviderAvailability,
    ) -> ProviderAvailability:
        """
        Activate availability slot.
        """

        instance.status = AvailabilityStatus.AVAILABLE

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
    def block(
        *,
        instance: ProviderAvailability,
    ) -> ProviderAvailability:
        """
        Block availability slot.
        """

        instance.status = AvailabilityStatus.BLOCKED

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
    def deactivate(
        *,
        instance: ProviderAvailability,
    ) -> ProviderAvailability:
        """
        Disable availability slot.
        """

        instance.status = AvailabilityStatus.UNAVAILABLE

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
    def delete(
        *,
        instance: ProviderAvailability,
    ) -> None:
        """
        Delete availability.
        """

        instance.delete()


# Backward-compatible aliases

create_provider_availability = ProviderAvailabilityService.create

update_provider_availability = ProviderAvailabilityService.update

delete_provider_availability = ProviderAvailabilityService.delete


__all__ = [
    "ProviderAvailabilityService",
    "create_provider_availability",
    "update_provider_availability",
    "delete_provider_availability",
]
