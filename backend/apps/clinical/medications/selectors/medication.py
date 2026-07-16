"""
Medication selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.clinical.medications.models import Medication


def get_medications() -> QuerySet[Medication]:
    """
    Return the medications queryset.
    """

    return Medication.objects.select_related(
        "organization",
    )


def get_medication_by_id(
    *,
    medication_id,
) -> Medication:
    """
    Return a medication by ID.
    """

    return get_object_or_404(
        get_medications(),
        id=medication_id,
    )


__all__ = [
    "get_medication_by_id",
    "get_medications",
]
