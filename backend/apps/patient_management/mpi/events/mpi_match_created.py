"""
Domain event for the Master Patient Index.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class MPIMatchCreatedEvent(DomainEvent):
    """Represent an immutable MPI candidate creation event."""

    event_type = "patient_mpi.match_created"

    tenant_id: UUID
    actor_id: UUID
    organization_id: UUID
    candidate_id: UUID
    left_record_id: UUID
    right_record_id: UUID


__all__ = ("MPIMatchCreatedEvent",)
