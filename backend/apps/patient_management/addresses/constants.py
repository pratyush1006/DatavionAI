"""
Constants for the Addresses module.
"""

from __future__ import annotations

from django.db import models


class AddressType(models.TextChoices):
    """Types of addresses."""

    HOME = "HOME", "Home"
    WORK = "WORK", "Work"
    BILLING = "BILLING", "Billing"
    SHIPPING = "SHIPPING", "Shipping"
    TEMPORARY = "TEMPORARY", "Temporary"
    EMERGENCY = "EMERGENCY", "Emergency"
    OTHER = "OTHER", "Other"


class AddressUse(models.TextChoices):
    """Usage of an address."""

    PRIMARY = "PRIMARY", "Primary"
    SECONDARY = "SECONDARY", "Secondary"
    CORRESPONDENCE = "CORRESPONDENCE", "Correspondence"
    EMERGENCY = "EMERGENCY", "Emergency"


class AddressStatus(models.TextChoices):
    """Status of an address."""

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    VERIFIED = "VERIFIED", "Verified"
    UNVERIFIED = "UNVERIFIED", "Unverified"


class AddressSource(models.TextChoices):
    """Source of an address."""

    PATIENT = "PATIENT", "Patient"
    STAFF = "STAFF", "Staff"
    IMPORT = "IMPORT", "Import"
    API = "API", "API"
    SYSTEM = "SYSTEM", "System"


__all__ = [
    "AddressSource",
    "AddressStatus",
    "AddressType",
    "AddressUse",
]
