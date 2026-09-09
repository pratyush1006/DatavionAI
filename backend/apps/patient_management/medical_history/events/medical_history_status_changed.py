"""Medical History Status Changed."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class MedicalHistoryStatusChangedEvent(DomainEvent):
    """MedicalHistoryStatusChangedEvent implementation."""

    tenant_id: UUID
    actor_id: UUID
    history_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str


__all__ = ("MedicalHistoryStatusChangedEvent",)
