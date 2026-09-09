"""
Provider domain constants.

Defines provider lifecycle states,
provider categories, credential types,
license lifecycle, verification states,
and availability states.

DatavionOS Healthcare Platform.

Supports:

- Multi-tenant SaaS
- Healthcare provider lifecycle
- Credential compliance
- License management
- Appointment scheduling
- Workflow-driven architecture
- AI provider matching
"""

from __future__ import annotations

from django.db import models

# ============================================================================
# Provider Lifecycle
# ============================================================================


class ProviderStatus(
    models.TextChoices,
):
    """
    Provider lifecycle state.

    Workflow:

        PENDING
            |
            v
        UNDER_REVIEW
            |
            v
        VERIFIED
            |
            v
        ACTIVE
            |
            +--> INACTIVE
            |
            +--> SUSPENDED
    """

    PENDING = (
        "pending",
        "Pending",
    )

    UNDER_REVIEW = (
        "under_review",
        "Under Review",
    )

    VERIFIED = (
        "verified",
        "Verified",
    )

    ACTIVE = (
        "active",
        "Active",
    )

    INACTIVE = (
        "inactive",
        "Inactive",
    )

    SUSPENDED = (
        "suspended",
        "Suspended",
    )


DEFAULT_PROVIDER_STATUS = ProviderStatus.PENDING


# ============================================================================
# Provider Classification
# ============================================================================


class ProviderType(
    models.TextChoices,
):
    """
    Healthcare provider classification.
    """

    PHYSICIAN = (
        "physician",
        "Physician",
    )

    SPECIALIST = (
        "specialist",
        "Specialist",
    )

    SURGEON = (
        "surgeon",
        "Surgeon",
    )

    NURSE = (
        "nurse",
        "Nurse",
    )

    DENTIST = (
        "dentist",
        "Dentist",
    )

    PHARMACIST = (
        "pharmacist",
        "Pharmacist",
    )

    THERAPIST = (
        "therapist",
        "Therapist",
    )

    PSYCHOLOGIST = (
        "psychologist",
        "Psychologist",
    )

    DIETITIAN = (
        "dietitian",
        "Dietitian",
    )

    TECHNICIAN = (
        "technician",
        "Technician",
    )

    OTHER = (
        "other",
        "Other",
    )


# ============================================================================
# Credential Management
# ============================================================================


class CredentialType(
    models.TextChoices,
):
    """
    Provider credential category.
    """

    DEGREE = (
        "degree",
        "Degree",
    )

    CERTIFICATION = (
        "certification",
        "Certification",
    )

    FELLOWSHIP = (
        "fellowship",
        "Fellowship",
    )

    TRAINING = (
        "training",
        "Training",
    )

    LICENSE = (
        "license",
        "License",
    )


class CredentialStatus(
    models.TextChoices,
):
    """
    Credential verification lifecycle.
    """

    PENDING = (
        "pending",
        "Pending",
    )

    VERIFIED = (
        "verified",
        "Verified",
    )

    REJECTED = (
        "rejected",
        "Rejected",
    )

    EXPIRED = (
        "expired",
        "Expired",
    )


# ============================================================================
# License Management
# ============================================================================


class LicenseStatus(
    models.TextChoices,
):
    """
    Medical license lifecycle.
    """

    PENDING = (
        "pending",
        "Pending",
    )

    VERIFIED = (
        "verified",
        "Verified",
    )

    EXPIRED = (
        "expired",
        "Expired",
    )

    SUSPENDED = (
        "suspended",
        "Suspended",
    )

    REVOKED = (
        "revoked",
        "Revoked",
    )


# ============================================================================
# Provider Assignment
# ============================================================================


class ProviderAssignmentStatus(
    models.TextChoices,
):
    """
    Provider assignment lifecycle.

    Used for:

    - Department assignment
    - Team assignment
    - Location assignment
    """

    ACTIVE = (
        "active",
        "Active",
    )

    INACTIVE = (
        "inactive",
        "Inactive",
    )


# ============================================================================
# Availability
# ============================================================================


class AvailabilityDay(
    models.IntegerChoices,
):
    """
    ISO weekday values.
    """

    MONDAY = (
        1,
        "Monday",
    )

    TUESDAY = (
        2,
        "Tuesday",
    )

    WEDNESDAY = (
        3,
        "Wednesday",
    )

    THURSDAY = (
        4,
        "Thursday",
    )

    FRIDAY = (
        5,
        "Friday",
    )

    SATURDAY = (
        6,
        "Saturday",
    )

    SUNDAY = (
        7,
        "Sunday",
    )


class AvailabilityStatus(
    models.TextChoices,
):
    """
    Provider schedule availability.
    """

    AVAILABLE = (
        "available",
        "Available",
    )

    UNAVAILABLE = (
        "unavailable",
        "Unavailable",
    )

    BLOCKED = (
        "blocked",
        "Blocked",
    )


__all__ = [
    "ProviderStatus",
    "DEFAULT_PROVIDER_STATUS",
    "ProviderType",
    "CredentialType",
    "CredentialStatus",
    "LicenseStatus",
    "ProviderAssignmentStatus",
    "AvailabilityDay",
    "AvailabilityStatus",
]
