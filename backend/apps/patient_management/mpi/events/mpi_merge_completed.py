"""
Domain event for the Master Patient Index.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class MPIMergeCompletedEvent(DomainEvent):
    """Represent an immutable MPI merge completion event."""

    tenant_id: UUID
    actor_id: UUID
    organization_id: UUID
    record_id: UUID
    survivor_id: UUID
    merge_status: str


__all__ = ("MPIMergeCompletedEvent",)
