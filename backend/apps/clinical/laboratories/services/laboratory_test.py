"""
Services for laboratory tests.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.clinical.laboratories.constants import (
    LaboratoryTestStatus,
)
from apps.clinical.laboratories.models import (
    LaboratoryTest,
)
from apps.core.exceptions import (
    InvalidWorkflowTransition,
)

###############################################################################
# Constants
###############################################################################

EDITABLE_FIELDS = frozenset(
    {"name", "priority", "display_order", "notes"},
)


###############################################################################
# Create Services
###############################################################################


@transaction.atomic
def create_laboratory_test(
    *,
    validated_data: dict[str, Any],
) -> LaboratoryTest:
    """
    Create a laboratory test.
    """

    return LaboratoryTest.objects.create(
        **validated_data,
    )


###############################################################################
# Update Services
###############################################################################


@transaction.atomic
def update_laboratory_test(
    *,
    instance: LaboratoryTest,
    validated_data: dict[str, Any],
) -> LaboratoryTest:
    """
    Update a laboratory test.
    """
    if instance.status in (
        LaboratoryTestStatus.COMPLETED,
        LaboratoryTestStatus.CANCELLED,
    ):
        raise InvalidWorkflowTransition(
            "Inactive laboratory tests cannot be updated.",
        )

    updated_fields: list[str] = []

    for field in EDITABLE_FIELDS:
        if field not in validated_data:
            continue

        setattr(
            instance,
            field,
            validated_data[field],
        )

        updated_fields.append(
            field,
        )

    if updated_fields:
        instance.save(
            update_fields=[
                *updated_fields,
                "updated_at",
            ],
        )

    return instance


###############################################################################
# Workflow Services
###############################################################################


@transaction.atomic
def start_laboratory_test(
    *,
    instance: LaboratoryTest,
) -> LaboratoryTest:
    """
    Start laboratory test processing.
    """

    if instance.is_in_progress:
        return instance

    if not instance.is_pending:
        raise InvalidWorkflowTransition(
            "Only pending laboratory tests can be started.",
        )

    instance.status = LaboratoryTestStatus.IN_PROGRESS

    instance.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return instance


@transaction.atomic
def complete_laboratory_test(
    *,
    instance: LaboratoryTest,
) -> LaboratoryTest:
    """
    Complete a laboratory test.
    """

    if instance.is_completed:
        return instance

    if not instance.is_in_progress:
        raise InvalidWorkflowTransition(
            "Only laboratory tests in progress can be completed.",
        )

    instance.status = LaboratoryTestStatus.COMPLETED

    instance.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return instance


@transaction.atomic
def cancel_laboratory_test(
    *,
    instance: LaboratoryTest,
) -> LaboratoryTest:
    """
    Cancel a laboratory test.
    """

    if instance.is_completed:
        raise InvalidWorkflowTransition(
            "Completed laboratory tests cannot be cancelled.",
        )

    if instance.is_cancelled:
        return instance

    instance.status = LaboratoryTestStatus.CANCELLED

    instance.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return instance


__all__ = [
    "cancel_laboratory_test",
    "complete_laboratory_test",
    "create_laboratory_test",
    "start_laboratory_test",
    "update_laboratory_test",
]
