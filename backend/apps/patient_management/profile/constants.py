"""
Constants for the Patient Profile module.
"""

from __future__ import annotations

from django.db import models


class LanguageProficiency(models.TextChoices):
    """
    Language proficiency level.
    """

    FLUENT = "fluent", "Fluent"

    CONVERSATIONAL = "conversational", "Conversational"

    BASIC = "basic", "Basic"

    NONE = "none", "None"


class EmploymentStatus(models.TextChoices):
    """
    Patient employment status.
    """

    EMPLOYED = "employed", "Employed"

    SELF_EMPLOYED = "self_employed", "Self Employed"

    UNEMPLOYED = "unemployed", "Unemployed"

    STUDENT = "student", "Student"

    RETIRED = "retired", "Retired"

    OTHER = "other", "Other"


class EducationLevel(models.TextChoices):
    """
    Patient education level.
    """

    NONE = "none", "None"

    PRIMARY = "primary", "Primary"

    SECONDARY = "secondary", "Secondary"

    DIPLOMA = "diploma", "Diploma"

    GRADUATE = "graduate", "Graduate"

    POSTGRADUATE = "postgraduate", "Postgraduate"


__all__ = [
    "EducationLevel",
    "EmploymentStatus",
    "LanguageProficiency",
]
