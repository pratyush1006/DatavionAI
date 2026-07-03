"""
Patient-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class PatientStatus(models.TextChoices):
    """
    Patient lifecycle status.
    """

    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    DECEASED = "deceased", "Deceased"
    ARCHIVED = "archived", "Archived"


class PatientGender(models.TextChoices):
    """
    Supported patient genders.
    """

    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"
    UNKNOWN = "unknown", "Unknown"


class PatientMaritalStatus(models.TextChoices):
    """
    Supported marital statuses.
    """

    SINGLE = "single", "Single"
    MARRIED = "married", "Married"
    DIVORCED = "divorced", "Divorced"
    WIDOWED = "widowed", "Widowed"
    SEPARATED = "separated", "Separated"
    UNKNOWN = "unknown", "Unknown"


class BloodGroup(models.TextChoices):
    """
    Supported blood groups.
    """

    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"
    UNKNOWN = "unknown", "Unknown"


DEFAULT_PATIENT_STATUS: Final[str] = PatientStatus.ACTIVE


__all__ = [
    "BloodGroup",
    "DEFAULT_PATIENT_STATUS",
    "PatientGender",
    "PatientMaritalStatus",
    "PatientStatus",
]
