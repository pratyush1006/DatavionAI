"""
Diagnosis constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class DiagnosisType(TextChoices):
    """
    Diagnosis type choices.
    """

    PRIMARY = (
        "primary",
        "Primary",
    )

    SECONDARY = (
        "secondary",
        "Secondary",
    )

    ADMITTING = (
        "admitting",
        "Admitting",
    )

    DISCHARGE = (
        "discharge",
        "Discharge",
    )

    FINAL = (
        "final",
        "Final",
    )


class DiagnosisStatus(TextChoices):
    """
    Diagnosis status choices.
    """

    ACTIVE = (
        "active",
        "Active",
    )

    RESOLVED = (
        "resolved",
        "Resolved",
    )

    INACTIVE = (
        "inactive",
        "Inactive",
    )


__all__ = [
    "DiagnosisStatus",
    "DiagnosisType",
]
