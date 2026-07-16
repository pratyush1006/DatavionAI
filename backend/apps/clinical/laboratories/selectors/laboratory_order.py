"""
Selectors for laboratory orders.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.clinical.laboratories.constants import (
    LaboratoryOrderStatus,
)
from apps.clinical.laboratories.models import (
    LaboratoryOrder,
)

###############################################################################
# Core Selectors
###############################################################################


def list_laboratory_orders() -> QuerySet[LaboratoryOrder]:
    """
    Return all laboratory orders.
    """

    return LaboratoryOrder.objects.select_related(
        "organization",
        "patient",
        "provider",
        "encounter",
    ).prefetch_related(
        "tests",
    )


def get_laboratory_order(
    *,
    pk: int,
) -> LaboratoryOrder:
    """
    Return a laboratory order by primary key.

    Raises:
        LaboratoryOrder.DoesNotExist:
            If the laboratory order does not exist.
    """

    return list_laboratory_orders().get(
        pk=pk,
    )


###############################################################################
# Relationship Selectors
###############################################################################


def list_patient_laboratory_orders(
    *,
    patient_id: int,
) -> QuerySet[LaboratoryOrder]:
    """
    Return all laboratory orders for a patient.
    """

    return list_laboratory_orders().filter(
        patient_id=patient_id,
    )


def list_encounter_laboratory_orders(
    *,
    encounter_id: int,
) -> QuerySet[LaboratoryOrder]:
    """
    Return all laboratory orders for an encounter.
    """

    return list_laboratory_orders().filter(
        encounter_id=encounter_id,
    )


###############################################################################
# Status Selectors
###############################################################################


def list_pending_laboratory_orders() -> QuerySet[LaboratoryOrder]:
    """
    Return all pending laboratory orders.
    """

    return list_laboratory_orders().filter(
        status=LaboratoryOrderStatus.ORDERED,
    )


def list_completed_laboratory_orders() -> QuerySet[LaboratoryOrder]:
    """
    Return all completed laboratory orders.
    """

    return list_laboratory_orders().filter(
        status=LaboratoryOrderStatus.COMPLETED,
    )


###############################################################################
# Aggregate Selectors
###############################################################################


def exists_order_number(
    *,
    organization_id: int,
    order_number: str,
) -> bool:
    """
    Return whether a laboratory order number already exists
    within an organization.
    """

    return LaboratoryOrder.objects.filter(
        organization_id=organization_id,
        order_number=order_number,
    ).exists()


def count_patient_laboratory_orders(
    *,
    patient_id: int,
) -> int:
    """
    Return the total number of laboratory orders for a patient.
    """

    return list_patient_laboratory_orders(
        patient_id=patient_id,
    ).count()


__all__ = [
    "count_patient_laboratory_orders",
    "exists_order_number",
    "get_laboratory_order",
    "list_completed_laboratory_orders",
    "list_encounter_laboratory_orders",
    "list_laboratory_orders",
    "list_patient_laboratory_orders",
    "list_pending_laboratory_orders",
]
