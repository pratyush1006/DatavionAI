"""
Domain event for the Master Patient Index.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class MPIRecordUpdatedEvent(DomainEvent):
    """Represent an immutable MPI record update event."""

    event_type = "patient_mpi.record_updated"

    tenant_id: UUID
    actor_id: UUID
    organization_id: UUID
    record_id: UUID


__all__ = ("MPIRecordUpdatedEvent",)
