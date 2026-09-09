"""Medical History Deleted."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class MedicalHistoryDeletedEvent(DomainEvent):
    """MedicalHistoryDeletedEvent implementation."""

    tenant_id: UUID
    actor_id: UUID
    history_id: UUID
    patient_id: UUID
    organization_id: UUID


__all__ = ("MedicalHistoryDeletedEvent",)
