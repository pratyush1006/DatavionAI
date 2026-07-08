"""
Services for laboratory orders.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from apps.core.exceptions import (
    InvalidWorkflowTransition,
)
from apps.laboratories.constants import (
    LaboratoryOrderStatus,
)
from apps.laboratories.models import (
    LaboratoryOrder,
)

###############################################################################
# Constants
###############################################################################

EDITABLE_FIELDS = frozenset(
    {
        "priority",
        "clinical_notes",
        "instructions",
    },
)

###############################################################################
# Create Services
###############################################################################


@transaction.atomic
def create_laboratory_order(
    *,
    validated_data: dict[str, Any],
) -> LaboratoryOrder:
    """
    Create a laboratory order.

    Args:
        validated_data:
            Serializer validated data.

    Returns:
        Newly created laboratory order.
    """

    return LaboratoryOrder.objects.create(
        **validated_data,
    )


###############################################################################
# Update Services
###############################################################################


@transaction.atomic
def update_laboratory_order(
    *,
    instance: LaboratoryOrder,
    validated_data: dict[str, Any],
) -> LaboratoryOrder:
    """
    Update an existing laboratory order.

    Only editable fields are updated.

    Args:
        instance:
            Laboratory order instance.

        validated_data:
            Serializer validated data.

    Returns:
        Updated laboratory order.

    Raises:
        InvalidWorkflowTransition:
            If the laboratory order is inactive.
    """

    if not instance.is_active:
        raise InvalidWorkflowTransition(
            "Completed or cancelled laboratory orders cannot be updated.",
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
def cancel_laboratory_order(
    *,
    instance: LaboratoryOrder,
) -> LaboratoryOrder:
    """
    Cancel a laboratory order.

    Args:
        instance:
            Laboratory order instance.

    Returns:
        Cancelled laboratory order.

    Raises:
        InvalidWorkflowTransition:
            If the laboratory order has already been completed.
    """

    if instance.is_completed:
        raise InvalidWorkflowTransition(
            "Completed laboratory orders cannot be cancelled.",
        )

    if instance.is_cancelled:
        return instance

    instance.status = LaboratoryOrderStatus.CANCELLED

    instance.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return instance


__all__ = [
    "cancel_laboratory_order",
    "create_laboratory_order",
    "update_laboratory_order",
]
