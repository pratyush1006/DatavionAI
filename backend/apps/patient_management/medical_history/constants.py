"""Medical history domain constants."""

from __future__ import annotations

from django.db import models


class MedicalHistoryType(models.TextChoices):
    """MedicalHistoryType implementation."""

    CONDITION = "condition", "Condition"
    SURGERY = "surgery", "Surgery"
    HOSPITALIZATION = "hospitalization", "Hospitalization"
    ALLERGY = "allergy", "Allergy"
    FAMILY_HISTORY = "family_history", "Family History"
    SOCIAL_HISTORY = "social_history", "Social History"
    IMMUNIZATION = "immunization", "Immunization"
    OTHER = "other", "Other"


class ClinicalStatus(models.TextChoices):
    """ClinicalStatus implementation."""

    ACTIVE = "active", "Active"
    RESOLVED = "resolved", "Resolved"
    INACTIVE = "inactive", "Inactive"
    HISTORY = "history", "History"


class AlcoholUse(models.TextChoices):
    """AlcoholUse implementation."""

    NONE = "none", "None"
    OCCASIONAL = "occasional", "Occasional"
    MODERATE = "moderate", "Moderate"
    HEAVY = "heavy", "Heavy"
    UNKNOWN = "unknown", "Unknown"


__all__ = (
    "MedicalHistoryType",
    "ClinicalStatus",
    "AlcoholUse",
)
