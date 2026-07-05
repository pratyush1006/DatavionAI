"""
Prescription selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.prescriptions.models import Prescription


def get_prescriptions() -> QuerySet[Prescription]:
    """
    Return the prescriptions queryset.
    """

    return Prescription.objects.select_related(
        "organization",
        "patient",
        "provider",
        "encounter",
        "medication",
    )


def get_prescription_by_id(
    *,
    prescription_id,
) -> Prescription:
    """
    Return a prescription by ID.
    """

    return get_object_or_404(
        get_prescriptions(),
        id=prescription_id,
    )


__all__ = [
    "get_prescription_by_id",
    "get_prescriptions",
]