"""
Constants for the Allergies app.
"""

from __future__ import annotations

from django.db import models


class AllergyCategory(
    models.TextChoices,
):
    """
    Available allergy categories.
    """

    MEDICATION = (
        "medication",
        "Medication",
    )

    FOOD = (
        "food",
        "Food",
    )

    ENVIRONMENTAL = (
        "environmental",
        "Environmental",
    )

    LATEX = (
        "latex",
        "Latex",
    )

    INSECT = (
        "insect",
        "Insect",
    )

    OTHER = (
        "other",
        "Other",
    )


class AllergySeverity(
    models.TextChoices,
):
    """
    Allergy severity levels.
    """

    MILD = (
        "mild",
        "Mild",
    )

    MODERATE = (
        "moderate",
        "Moderate",
    )

    SEVERE = (
        "severe",
        "Severe",
    )

    LIFE_THREATENING = (
        "life_threatening",
        "Life Threatening",
    )


class AllergyStatus(
    models.TextChoices,
):
    """
    Allergy status.
    """

    ACTIVE = (
        "active",
        "Active",
    )

    RESOLVED = (
        "resolved",
        "Resolved",
    )

    ENTERED_IN_ERROR = (
        "entered_in_error",
        "Entered In Error",
    )


DEFAULT_ALLERGY_CATEGORY = AllergyCategory.MEDICATION

DEFAULT_ALLERGY_SEVERITY = AllergySeverity.MODERATE

DEFAULT_ALLERGY_STATUS = AllergyStatus.ACTIVE


__all__ = [
    "AllergyCategory",
    "AllergySeverity",
    "AllergyStatus",
    "DEFAULT_ALLERGY_CATEGORY",
    "DEFAULT_ALLERGY_SEVERITY",
    "DEFAULT_ALLERGY_STATUS",
]
