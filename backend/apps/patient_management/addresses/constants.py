"""Patient Address constants."""

from __future__ import annotations

from django.db import models


class AddressType(models.TextChoices):
    HOME = "home", "Home"
    WORK = "work", "Work"
    BILLING = "billing", "Billing"
    SHIPPING = "shipping", "Shipping"
    TEMPORARY = "temporary", "Temporary"
    EMERGENCY = "emergency", "Emergency"
    OTHER = "other", "Other"


class AddressUse(models.TextChoices):
    PRIMARY = "primary", "Primary"
    SECONDARY = "secondary", "Secondary"
    CORRESPONDENCE = "correspondence", "Correspondence"
    EMERGENCY = "emergency", "Emergency"


class AddressStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    VERIFIED = "verified", "Verified"
    UNVERIFIED = "unverified", "Unverified"


class AddressSource(models.TextChoices):
    PATIENT = "patient", "Patient"
    STAFF = "staff", "Staff"
    IMPORT = "import", "Import"
    API = "api", "API"
    SYSTEM = "system", "System"
    GEOGRAPHY = "geography", "Geography"


__all__ = ("AddressType", "AddressUse", "AddressStatus", "AddressSource")
