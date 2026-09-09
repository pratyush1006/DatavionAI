"""
Domain event for the Master Patient Index.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class MPIRecordStatusChangedEvent(DomainEvent):
    """Represent an immutable MPI record lifecycle change event."""

    tenant_id: UUID
    actor_id: UUID
    organization_id: UUID
    record_id: UUID
    previous_status: str
    status: str


__all__ = ("MPIRecordStatusChangedEvent",)
