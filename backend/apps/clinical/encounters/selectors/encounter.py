"""
Encounter selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.clinical.encounters.models import Encounter


def get_encounters() -> QuerySet[Encounter]:
    """
    Return the encounter queryset.
    """

    return Encounter.objects.select_related(
        "organization",
        "appointment",
        "patient",
        "provider",
        "provider__employee",
        "provider__employee__user",
    )


def get_encounter_by_id(
    *,
    encounter_id,
) -> Encounter:
    """
    Return an encounter by ID.
    """

    return get_encounters().get(
        id=encounter_id,
    )


__all__ = [
    "get_encounter_by_id",
    "get_encounters",
]
