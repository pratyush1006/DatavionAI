"""
Constants for the Contacts module.
"""

from __future__ import annotations

from django.db import models


class ContactType(models.TextChoices):
    """Types of patient contacts."""

    MOBILE = "MOBILE", "Mobile"
    HOME = "HOME", "Home"
    WORK = "WORK", "Work"
    EMERGENCY = "EMERGENCY", "Emergency"
    FAX = "FAX", "Fax"
    OTHER = "OTHER", "Other"


class ContactPurpose(models.TextChoices):
    """Purpose of a patient contact."""

    PRIMARY = "PRIMARY", "Primary"
    BILLING = "BILLING", "Billing"
    APPOINTMENT = "APPOINTMENT", "Appointment"
    EMERGENCY = "EMERGENCY", "Emergency"
    NOTIFICATION = "NOTIFICATION", "Notification"
    OTHER = "OTHER", "Other"


class ContactStatus(models.TextChoices):
    """Status of a patient contact."""

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    VERIFIED = "VERIFIED", "Verified"
    UNVERIFIED = "UNVERIFIED", "Unverified"


class ContactSource(models.TextChoices):
    """Source of a patient contact."""

    PATIENT = "PATIENT", "Patient"
    STAFF = "STAFF", "Staff"
    IMPORT = "IMPORT", "Import"
    API = "API", "API"
    SYSTEM = "SYSTEM", "System"


__all__ = [
    "ContactPurpose",
    "ContactSource",
    "ContactStatus",
    "ContactType",
]
