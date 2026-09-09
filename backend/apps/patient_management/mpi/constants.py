"""
Domain constants for the Master Patient Index.
"""

from __future__ import annotations

from django.db import models


class MPIRecordStatus(models.TextChoices):
    """Lifecycle state of an MPI record."""

    ACTIVE = "ACTIVE", "Active"
    MERGED = "MERGED", "Merged"
    RETIRED = "RETIRED", "Retired"


class MPIMatchStatus(models.TextChoices):
    """Review state of an MPI candidate match."""

    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    REJECTED = "REJECTED", "Rejected"
    EXPIRED = "EXPIRED", "Expired"


class MPIMergeStatus(models.TextChoices):
    """Administrative status of an MPI merge operation."""

    ACTIVE = "ACTIVE", "Active"
    REVERSED = "REVERSED", "Reversed"


MPI_MATCH_THRESHOLD = 0.85
MPI_REVIEW_THRESHOLD = 0.65

MPI_MATCH_CLASS_AUTO = "AUTO_MATCH"
MPI_MATCH_CLASS_REVIEW = "REVIEW"
MPI_MATCH_CLASS_NO_MATCH = "NO_MATCH"

ALLOWED_RECORD_TRANSITIONS = {
    MPIRecordStatus.ACTIVE: {
        MPIRecordStatus.MERGED,
        MPIRecordStatus.RETIRED,
    },
    MPIRecordStatus.MERGED: set(),
    MPIRecordStatus.RETIRED: set(),
}

__all__ = (
    "ALLOWED_RECORD_TRANSITIONS",
    "MPI_MATCH_CLASS_AUTO",
    "MPI_MATCH_CLASS_NO_MATCH",
    "MPI_MATCH_CLASS_REVIEW",
    "MPI_MATCH_THRESHOLD",
    "MPI_REVIEW_THRESHOLD",
    "MPIMatchStatus",
    "MPIMergeStatus",
    "MPIRecordStatus",
)
