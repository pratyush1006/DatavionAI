"""
Constants for the Patient Identifiers module.

This module defines the enumerations used throughout the Patient
Identifiers bounded context. These values are shared by models,
validators, services, selectors, serializers, and APIs to ensure
consistent behavior across the platform.
"""

from __future__ import annotations

from django.db import models


class IdentifierType(models.TextChoices):
    """
    Supported patient identifier types.
    """

    MRN = "MRN", "Medical Record Number"
    ABHA = "ABHA", "ABHA Number"
    AADHAAR = "AADHAAR", "Aadhaar Number"
    PASSPORT = "PASSPORT", "Passport"
    DRIVING_LICENSE = "DRIVING_LICENSE", "Driving License"
    NATIONAL_ID = "NATIONAL_ID", "National ID"
    INSURANCE_MEMBER_ID = "INSURANCE_MEMBER_ID", "Insurance Member ID"
    EMPLOYEE_ID = "EMPLOYEE_ID", "Employee ID"
    EXTERNAL_EMR_ID = "EXTERNAL_EMR_ID", "External EMR ID"
    LEGACY_HOSPITAL_ID = "LEGACY_HOSPITAL_ID", "Legacy Hospital ID"
    OTHER = "OTHER", "Other"


class IdentifierStatus(models.TextChoices):
    """
    Operational status of an identifier.
    """

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    EXPIRED = "EXPIRED", "Expired"
    REVOKED = "REVOKED", "Revoked"


class VerificationStatus(models.TextChoices):
    """
    Verification state of an identifier.
    """

    PENDING = "PENDING", "Pending"
    VERIFIED = "VERIFIED", "Verified"
    REJECTED = "REJECTED", "Rejected"
    EXPIRED = "EXPIRED", "Expired"


class IdentifierSource(models.TextChoices):
    """
    Source from which the identifier was obtained.
    """

    PATIENT = "PATIENT", "Patient"
    REGISTRATION = "REGISTRATION", "Registration"
    STAFF = "STAFF", "Staff"
    GOVERNMENT = "GOVERNMENT", "Government"
    EXTERNAL_SYSTEM = "EXTERNAL_SYSTEM", "External System"
    IMPORT = "IMPORT", "Import"
    API = "API", "API"


class IdentifierPriority(models.TextChoices):
    """
    Priority assigned to an identifier.
    """

    PRIMARY = "PRIMARY", "Primary"
    SECONDARY = "SECONDARY", "Secondary"
    ARCHIVED = "ARCHIVED", "Archived"


__all__ = [
    "IdentifierPriority",
    "IdentifierSource",
    "IdentifierStatus",
    "IdentifierType",
    "VerificationStatus",
]
