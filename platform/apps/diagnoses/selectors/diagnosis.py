"""
Diagnosis selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.diagnoses.models import Diagnosis


def get_diagnoses() -> QuerySet[Diagnosis]:
    """
    Return the diagnoses queryset.
    """

    return Diagnosis.objects.select_related(
        "organization",
        "encounter",
        "encounter__patient",
        "encounter__provider",
        "encounter__provider__employee",
        "encounter__provider__employee__user",
    )


def get_diagnosis_by_id(
    *,
    diagnosis_id,
) -> Diagnosis:
    """
    Return a diagnosis by ID.
    """

    return get_object_or_404(
        get_diagnoses(),
        id=diagnosis_id,
    )


__all__ = [
    "get_diagnosis_by_id",
    "get_diagnoses",
]
