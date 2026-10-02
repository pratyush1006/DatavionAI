"""
Constants for the Patient Relationships module.
"""

from __future__ import annotations

from django.db import models


class RelationshipType(models.TextChoices):
    SPOUSE = "spouse", "Spouse"
    PARTNER = "partner", "Partner"
    PARENT = "parent", "Parent"
    CHILD = "child", "Child"
    SIBLING = "sibling", "Sibling"
    GRANDPARENT = "grandparent", "Grandparent"
    GRANDCHILD = "grandchild", "Grandchild"
    GUARDIAN = "guardian", "Guardian"
    DEPENDENT = "dependent", "Dependent"
    CAREGIVER = "caregiver", "Caregiver"
    EMERGENCY_CONTACT = "emergency_contact", "Emergency Contact"
    OTHER = "other", "Other"


class RelationshipStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    TERMINATED = "terminated", "Terminated"


class VerificationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    VERIFIED = "verified", "Verified"
    REJECTED = "rejected", "Rejected"


__all__ = (
    "RelationshipType",
    "RelationshipStatus",
    "VerificationStatus",
)
