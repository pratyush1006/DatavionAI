"""
Services for laboratory results.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.core.exceptions import (
    InvalidWorkflowTransition,
)
from apps.laboratories.constants import (
    LaboratoryResultStatus,
)
from apps.laboratories.models import (
    LaboratoryResult,
)
from apps.laboratories.selectors import (
    get_laboratory_result,
)

###############################################################################
# Constants
###############################################################################

EDITABLE_FIELDS = frozenset(
    {
        "result_value_numeric",
        "result_value_text",
        "unit",
        "reference_range",
        "abnormal_flag",
        "notes",
    },
)


###############################################################################
# Create Services
###############################################################################


@transaction.atomic
def create_laboratory_result(
    *,
    validated_data: dict[str, Any],
) -> LaboratoryResult:
    """
    Create a laboratory result.
    """

    return LaboratoryResult.objects.create(
        **validated_data,
    )


###############################################################################
# Update Services
###############################################################################


@transaction.atomic
def update_laboratory_result(
    *,
    laboratory_result_id,
    validated_data: dict[str, Any],
) -> LaboratoryResult:
    """
    Update a laboratory result.
    """

    laboratory_result = get_laboratory_result(
        pk=laboratory_result_id,
    )

    if laboratory_result.is_final:
        raise InvalidWorkflowTransition(
            "Final laboratory results cannot be updated.",
        )

    updated_fields: list[str] = []

    for field in EDITABLE_FIELDS:
        if field not in validated_data:
            continue

        setattr(
            laboratory_result,
            field,
            validated_data[field],
        )

        updated_fields.append(
            field,
        )

    if updated_fields:
        laboratory_result.save(
            update_fields=[
                *updated_fields,
                "updated_at",
            ],
        )

    return laboratory_result


###############################################################################
# Workflow Services
###############################################################################


@transaction.atomic
def record_laboratory_result(
    *,
    laboratory_result_id,
) -> LaboratoryResult:
    """
    Mark a laboratory result as recorded.
    """

    laboratory_result = get_laboratory_result(
        pk=laboratory_result_id,
    )

    if laboratory_result.is_recorded:
        return laboratory_result

    laboratory_result.status = LaboratoryResultStatus.RECORDED

    laboratory_result.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return laboratory_result


@transaction.atomic
def verify_laboratory_result(
    *,
    laboratory_result_id,
    verified_by_id,
) -> LaboratoryResult:
    """
    Verify a laboratory result.
    """

    laboratory_result = get_laboratory_result(
        pk=laboratory_result_id,
    )

    if laboratory_result.is_verified:
        return laboratory_result

    if not laboratory_result.is_recorded:
        raise InvalidWorkflowTransition(
            "Only recorded laboratory results can be verified.",
        )

    laboratory_result.status = LaboratoryResultStatus.VERIFIED

    laboratory_result.verified_by_id = verified_by_id

    laboratory_result.verified_at = timezone.now()

    laboratory_result.save(
        update_fields=[
            "status",
            "verified_by",
            "verified_at",
            "updated_at",
        ],
    )

    return laboratory_result


@transaction.atomic
def amend_laboratory_result(
    *,
    laboratory_result_id,
    validated_data: dict[str, Any],
) -> LaboratoryResult:
    """
    Amend a laboratory result.
    """

    laboratory_result = get_laboratory_result(
        pk=laboratory_result_id,
    )

    if not laboratory_result.is_verified:
        raise InvalidWorkflowTransition(
            "Only verified laboratory results can be amended.",
        )

    updated_fields: list[str] = []

    for field in EDITABLE_FIELDS:
        if field not in validated_data:
            continue

        setattr(
            laboratory_result,
            field,
            validated_data[field],
        )

        updated_fields.append(
            field,
        )

    laboratory_result.status = LaboratoryResultStatus.AMENDED

    updated_fields.append(
        "status",
    )

    laboratory_result.save(
        update_fields=[
            *updated_fields,
            "updated_at",
        ],
    )

    return laboratory_result


@transaction.atomic
def invalidate_laboratory_result(
    *,
    laboratory_result_id,
) -> LaboratoryResult:
    """
    Invalidate a laboratory result.
    """

    laboratory_result = get_laboratory_result(
        pk=laboratory_result_id,
    )

    if laboratory_result.is_invalidated:
        return laboratory_result

    laboratory_result.status = LaboratoryResultStatus.INVALIDATED

    laboratory_result.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return laboratory_result


__all__ = [
    "amend_laboratory_result",
    "create_laboratory_result",
    "invalidate_laboratory_result",
    "record_laboratory_result",
    "update_laboratory_result",
    "verify_laboratory_result",
]
