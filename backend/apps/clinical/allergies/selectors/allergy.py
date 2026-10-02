"""
Allergy selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.clinical.allergies.models import Allergy


def get_allergies() -> QuerySet[Allergy]:
    """
    Return the allergies queryset.
    """

    return Allergy.objects.select_related(
        "organization",
        "patient",
        "provider",
        "encounter",
    )


def get_allergy_by_id(
    *,
    allergy_id,
) -> Allergy:
    """
    Return an allergy by ID.
    """

    return get_object_or_404(
        get_allergies(),
        id=allergy_id,
    )


__all__ = [
    "get_allergies",
    "get_allergy_by_id",
]
