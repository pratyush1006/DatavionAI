"""
Constants for the Patient Relationships module.
"""

from __future__ import annotations

from django.db.models import TextChoices


class RelationshipType(TextChoices):
    """
    Types of patient relationships.
    """

    PARENT = "parent", "Parent"
    CHILD = "child", "Child"
    SPOUSE = "spouse", "Spouse"
    GUARDIAN = "guardian", "Guardian"
    CAREGIVER = "caregiver", "Caregiver"
    EMERGENCY_CONTACT = "emergency_contact", "Emergency Contact"
    NEXT_OF_KIN = "next_of_kin", "Next of Kin"
    SIBLING = "sibling", "Sibling"
    GRANDPARENT = "grandparent", "Grandparent"
    GRANDCHILD = "grandchild", "Grandchild"
    EMPLOYER = "employer", "Employer"
    INSURER = "insurer", "Insurer"
    REFERRING_PROVIDER = "referring_provider", "Referring Provider"
    PRIMARY_CARE_PROVIDER = (
        "primary_care_provider",
        "Primary Care Provider",
    )
    OTHER = "other", "Other"


class RelationshipStatus(TextChoices):
    """
    Relationship status.
    """

    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    TERMINATED = "terminated", "Terminated"


class RelationshipVerificationStatus(TextChoices):
    """
    Verification status.
    """

    PENDING = "pending", "Pending"
    VERIFIED = "verified", "Verified"
    REJECTED = "rejected", "Rejected"


class RelationshipSource(TextChoices):
    """
    Source of the relationship.
    """

    MANUAL = "manual", "Manual"
    PATIENT = "patient", "Patient"
    REGISTRATION = "registration", "Registration"
    IMPORT = "import", "Import"
    API = "api", "API"
    FHIR = "fhir", "FHIR"


__all__ = [
    "RelationshipSource",
    "RelationshipStatus",
    "RelationshipType",
    "RelationshipVerificationStatus",
]
