"""
Medication constants.
"""

from __future__ import annotations

from django.db import models


class MedicationDosageForm(models.TextChoices):
    """
    Medication dosage form choices.
    """

    TABLET = (
        "tablet",
        "Tablet",
    )

    CAPSULE = (
        "capsule",
        "Capsule",
    )

    SYRUP = (
        "syrup",
        "Syrup",
    )

    SUSPENSION = (
        "suspension",
        "Suspension",
    )

    INJECTION = (
        "injection",
        "Injection",
    )

    CREAM = (
        "cream",
        "Cream",
    )

    OINTMENT = (
        "ointment",
        "Ointment",
    )

    GEL = (
        "gel",
        "Gel",
    )

    DROPS = (
        "drops",
        "Drops",
    )

    INHALER = (
        "inhaler",
        "Inhaler",
    )


class MedicationRoute(models.TextChoices):
    """
    Medication administration route choices.
    """

    ORAL = (
        "oral",
        "Oral",
    )

    INTRAVENOUS = (
        "intravenous",
        "Intravenous",
    )

    INTRAMUSCULAR = (
        "intramuscular",
        "Intramuscular",
    )

    SUBCUTANEOUS = (
        "subcutaneous",
        "Subcutaneous",
    )

    TOPICAL = (
        "topical",
        "Topical",
    )

    OPHTHALMIC = (
        "ophthalmic",
        "Ophthalmic",
    )

    OTIC = (
        "otic",
        "Otic",
    )

    NASAL = (
        "nasal",
        "Nasal",
    )

    RECTAL = (
        "rectal",
        "Rectal",
    )

    INHALATION = (
        "inhalation",
        "Inhalation",
    )


DEFAULT_DOSAGE_FORM = MedicationDosageForm.TABLET

DEFAULT_ROUTE = MedicationRoute.ORAL


__all__ = [
    "DEFAULT_DOSAGE_FORM",
    "DEFAULT_ROUTE",
    "MedicationDosageForm",
    "MedicationRoute",
]
