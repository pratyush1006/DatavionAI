"""
Constants used by the Providers application.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class ProviderType(models.TextChoices):
    """
    Supported healthcare provider types.
    """

    # Medical
    PHYSICIAN = "physician", "Physician"
    SURGEON = "surgeon", "Surgeon"
    DENTIST = "dentist", "Dentist"

    # Nursing & Allied Health
    NURSE = "nurse", "Nurse"
    THERAPIST = "therapist", "Therapist"
    PHARMACIST = "pharmacist", "Pharmacist"

    # Diagnostics
    RADIOLOGIST = "radiologist", "Radiologist"
    PATHOLOGIST = "pathologist", "Pathologist"
    LAB_TECHNICIAN = "lab_technician", "Lab Technician"

    # Other
    OTHER = "other", "Other"


class ProviderStatus(models.TextChoices):
    """
    Provider lifecycle status.
    """

    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    ON_LEAVE = "on_leave", "On Leave"
    SUSPENDED = "suspended", "Suspended"
    RETIRED = "retired", "Retired"


DEFAULT_PROVIDER_STATUS: Final[ProviderStatus] = ProviderStatus.ACTIVE


__all__ = [
    "DEFAULT_PROVIDER_STATUS",
    "ProviderStatus",
    "ProviderType",
]
