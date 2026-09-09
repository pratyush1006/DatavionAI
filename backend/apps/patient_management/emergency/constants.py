"""Constants for patient emergency records."""

from __future__ import annotations

from django.db import models


class EmergencyContactType(models.TextChoices):
    """Supported emergency contact relationship categories."""

    FAMILY = "family", "Family"
    SPOUSE = "spouse", "Spouse"
    PARENT = "parent", "Parent"
    CHILD = "child", "Child"
    SIBLING = "sibling", "Sibling"
    FRIEND = "friend", "Friend"
    CAREGIVER = "caregiver", "Caregiver"
    OTHER = "other", "Other"


class EmergencyContactPriority(models.TextChoices):
    """Priority assigned to an emergency contact."""

    PRIMARY = "primary", "Primary"
    SECONDARY = "secondary", "Secondary"


class EmergencyRecordStatus(models.TextChoices):
    """Lifecycle status of an emergency record."""

    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    DELETED = "deleted", "Deleted"


__all__ = (
    "EmergencyContactPriority",
    "EmergencyContactType",
    "EmergencyRecordStatus",
)
