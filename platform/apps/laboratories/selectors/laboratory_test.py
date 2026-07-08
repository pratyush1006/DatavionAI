"""
Selectors for laboratory tests.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.laboratories.constants import (
    LaboratoryCategory,
    LaboratoryPriority,
    LaboratorySpecimenType,
    LaboratoryTestStatus,
)
from apps.laboratories.models import (
    LaboratoryTest,
)

###############################################################################
# Core Selectors
###############################################################################


def list_laboratory_tests() -> QuerySet[LaboratoryTest]:
    """
    Return all laboratory tests.
    """

    return LaboratoryTest.objects.select_related(
        "laboratory_order",
        "laboratory_order__organization",
        "laboratory_order__patient",
        "laboratory_order__provider",
        "laboratory_order__encounter",
        "result",
    ).order_by(
        "display_order",
        "created_at",
    )


def get_laboratory_test(
    *,
    pk: UUID,
) -> LaboratoryTest:
    """
    Return a laboratory test by primary key.

    Raises:
        LaboratoryTest.DoesNotExist:
            If the laboratory test does not exist.
    """

    return list_laboratory_tests().get(
        pk=pk,
    )


###############################################################################
# Relationship Selectors
###############################################################################


def list_laboratory_order_tests(
    *,
    laboratory_order_id: UUID,
) -> QuerySet[LaboratoryTest]:
    """
    Return all laboratory tests belonging to a laboratory order.
    """

    return list_laboratory_tests().filter(
        laboratory_order_id=laboratory_order_id,
    )


###############################################################################
# Filter Selectors
###############################################################################


def list_status_laboratory_tests(
    *,
    status: LaboratoryTestStatus,
) -> QuerySet[LaboratoryTest]:
    """
    Return laboratory tests filtered by status.
    """

    return list_laboratory_tests().filter(
        status=status,
    )


def list_pending_laboratory_tests() -> QuerySet[LaboratoryTest]:
    """
    Return all pending laboratory tests.
    """

    return list_status_laboratory_tests(
        status=LaboratoryTestStatus.PENDING,
    )


def list_completed_laboratory_tests() -> QuerySet[LaboratoryTest]:
    """
    Return all completed laboratory tests.
    """

    return list_status_laboratory_tests(
        status=LaboratoryTestStatus.COMPLETED,
    )


def list_category_laboratory_tests(
    *,
    category: LaboratoryCategory,
) -> QuerySet[LaboratoryTest]:
    """
    Return laboratory tests filtered by category.
    """

    return list_laboratory_tests().filter(
        category=category,
    )


def list_priority_laboratory_tests(
    *,
    priority: LaboratoryPriority,
) -> QuerySet[LaboratoryTest]:
    """
    Return laboratory tests filtered by priority.
    """

    return list_laboratory_tests().filter(
        priority=priority,
    )


def list_specimen_laboratory_tests(
    *,
    specimen_type: LaboratorySpecimenType,
) -> QuerySet[LaboratoryTest]:
    """
    Return laboratory tests filtered by specimen type.
    """

    return list_laboratory_tests().filter(
        specimen_type=specimen_type,
    )


###############################################################################
# Aggregate Selectors
###############################################################################


def exists_laboratory_test(
    *,
    laboratory_order_id: UUID,
    code: str,
) -> bool:
    """
    Return whether a laboratory test already exists
    within a laboratory order.
    """

    return (
        list_laboratory_tests()
        .filter(
            laboratory_order_id=laboratory_order_id,
            code=code,
        )
        .exists()
    )


def count_laboratory_order_tests(
    *,
    laboratory_order_id: UUID,
) -> int:
    """
    Return the total number of laboratory tests
    within a laboratory order.
    """

    return list_laboratory_order_tests(
        laboratory_order_id=laboratory_order_id,
    ).count()


__all__ = [
    "count_laboratory_order_tests",
    "exists_laboratory_test",
    "get_laboratory_test",
    "list_category_laboratory_tests",
    "list_completed_laboratory_tests",
    "list_laboratory_order_tests",
    "list_laboratory_tests",
    "list_pending_laboratory_tests",
    "list_priority_laboratory_tests",
    "list_specimen_laboratory_tests",
    "list_status_laboratory_tests",
]
