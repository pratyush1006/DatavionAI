"""
Master Patient Index domain event exports.
"""

from __future__ import annotations

from apps.patient_management.mpi.events.mpi_match_created import MPIMatchCreatedEvent
from apps.patient_management.mpi.events.mpi_match_reviewed import MPIMatchReviewedEvent
from apps.patient_management.mpi.events.mpi_merge_completed import (
    MPIMergeCompletedEvent,
)
from apps.patient_management.mpi.events.mpi_merge_reversed import MPIMergeReversedEvent
from apps.patient_management.mpi.events.mpi_record_created import MPIRecordCreatedEvent
from apps.patient_management.mpi.events.mpi_record_deleted import MPIRecordDeletedEvent
from apps.patient_management.mpi.events.mpi_record_status_changed import (
    MPIRecordStatusChangedEvent,
)
from apps.patient_management.mpi.events.mpi_record_updated import MPIRecordUpdatedEvent

__all__ = (
    "MPIMatchCreatedEvent",
    "MPIMatchReviewedEvent",
    "MPIMergeCompletedEvent",
    "MPIMergeReversedEvent",
    "MPIRecordCreatedEvent",
    "MPIRecordDeletedEvent",
    "MPIRecordStatusChangedEvent",
    "MPIRecordUpdatedEvent",
)
