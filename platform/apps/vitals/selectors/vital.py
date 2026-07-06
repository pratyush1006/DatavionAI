"""
Vital selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.vitals.models import Vital


def get_vitals() -> QuerySet[Vital]:
    """
    Return the vitals queryset.
    """

    return Vital.objects.select_related(
        "organization",
        "patient",
        "provider",
        "encounter",
    )


def get_vital_by_id(
    *,
    vital_id,
) -> Vital:
    """
    Return a vital by ID.
    """

    return get_object_or_404(
        get_vitals(),
        id=vital_id,
    )


__all__ = [
    "get_vital_by_id",
    "get_vitals",
]
