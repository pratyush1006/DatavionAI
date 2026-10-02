"""Medical History Verified."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class MedicalHistoryVerifiedEvent(DomainEvent):
    """MedicalHistoryVerifiedEvent implementation."""

    tenant_id: UUID
    actor_id: UUID
    history_id: UUID
    patient_id: UUID
    organization_id: UUID
    verified_at: str


__all__ = ("MedicalHistoryVerifiedEvent",)
