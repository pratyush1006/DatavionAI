"""Medical History Created."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class MedicalHistoryCreatedEvent(DomainEvent):
    """MedicalHistoryCreatedEvent implementation."""

    tenant_id: UUID
    actor_id: UUID
    history_id: UUID
    patient_id: UUID
    organization_id: UUID
    history_type: str
    clinical_status: str


__all__ = ("MedicalHistoryCreatedEvent",)
