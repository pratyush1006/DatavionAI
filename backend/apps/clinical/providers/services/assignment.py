"""
Provider assignment services.

Handles provider assignment lifecycle operations.

Responsibilities:

- Create assignment
- Update assignment
- Delete assignment
- Activate assignment
- Deactivate assignment
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.clinical.providers.models import (
    ProviderAssignment,
)


class ProviderAssignmentService:
    """
    Service layer for provider assignments.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
    ) -> ProviderAssignment:
        """
        Create provider assignment.
        """

        assignment = ProviderAssignment(
            **validated_data,
        )

        assignment.full_clean()

        assignment.save()

        return assignment

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: ProviderAssignment,
        validated_data: Mapping[str, Any],
    ) -> ProviderAssignment:
        """
        Update provider assignment.
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
        instance: ProviderAssignment,
    ) -> None:
        """
        Delete provider assignment.
        """

        instance.delete()

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: ProviderAssignment,
    ) -> ProviderAssignment:
        """
        Activate provider assignment.
        """

        from apps.clinical.providers.constants import (
            ProviderAssignmentStatus,
        )

        instance.status = ProviderAssignmentStatus.ACTIVE

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
        instance: ProviderAssignment,
    ) -> ProviderAssignment:
        """
        Deactivate provider assignment.
        """

        from apps.clinical.providers.constants import (
            ProviderAssignmentStatus,
        )

        instance.status = ProviderAssignmentStatus.INACTIVE

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return instance


# Backward compatible aliases

create_provider_assignment = ProviderAssignmentService.create

update_provider_assignment = ProviderAssignmentService.update

delete_provider_assignment = ProviderAssignmentService.delete


__all__ = (
    "ProviderAssignmentService",
    "create_provider_assignment",
    "update_provider_assignment",
    "delete_provider_assignment",
)
