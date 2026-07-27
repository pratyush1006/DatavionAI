"""
Constants for the Medical History module.
"""

from __future__ import annotations

from django.db import models


class MedicalHistoryType(models.TextChoices):
    """
    Type of medical history entry.
    """

    CONDITION = "condition", "Condition"

    SURGERY = "surgery", "Surgery"

    INJURY = "injury", "Injury"

    HOSPITALIZATION = "hospitalization", "Hospitalization"

    ALLERGY = "allergy", "Allergy"

    MEDICATION_HISTORY = "medication_history", "Medication History"

    FAMILY_HISTORY = "family_history", "Family History"

    SOCIAL_HISTORY = "social_history", "Social History"


class ClinicalStatus(models.TextChoices):
    """
    Clinical status of a history entry.
    """

    ACTIVE = "active", "Active"

    RESOLVED = "resolved", "Resolved"

    CHRONIC = "chronic", "Chronic"

    INACTIVE = "inactive", "Inactive"


__all__ = [
    "ClinicalStatus",
    "MedicalHistoryType",
]
