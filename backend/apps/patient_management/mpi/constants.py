"""
Constants for the Master Patient Index (MPI) module.
"""

from __future__ import annotations

from django.db.models import TextChoices


class MPIStatus(TextChoices):
    """
    Status of the MPI record.
    """

    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    MERGED = "merged", "Merged"
    ARCHIVED = "archived", "Archived"


class MPIVerificationStatus(TextChoices):
    """
    Verification status.
    """

    PENDING = "pending", "Pending"
    VERIFIED = "verified", "Verified"
    REJECTED = "rejected", "Rejected"


class MPIMatchConfidence(TextChoices):
    """
    Confidence level for patient matching.
    """

    EXACT = "exact", "Exact Match"
    HIGH = "high", "High"
    MEDIUM = "medium", "Medium"
    LOW = "low", "Low"


class MPIRecordSource(TextChoices):
    """
    Source of the MPI record.
    """

    MANUAL = "manual", "Manual"
    REGISTRATION = "registration", "Registration"
    IMPORT = "import", "Import"
    API = "api", "API"
    ABHA = "abha", "ABHA"
    HL7 = "hl7", "HL7"
    FHIR = "fhir", "FHIR"


class MPIMergeStatus(TextChoices):
    """
    Merge status.
    """

    NOT_MERGED = "not_merged", "Not Merged"
    PENDING = "pending", "Pending"
    MERGED = "merged", "Merged"
    UNMERGED = "unmerged", "Unmerged"


__all__ = [
    "MPIMatchConfidence",
    "MPIMergeStatus",
    "MPIRecordSource",
    "MPIStatus",
    "MPIVerificationStatus",
]
