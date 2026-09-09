"""
Patient updated domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientUpdatedEvent(DomainEvent):
    """
    Emitted when mutable patient information is updated.
    """

    tenant_id: UUID
    actor_id: UUID
    patient_id: UUID
    organization_id: UUID


__all__: tuple[str, ...] = ("PatientUpdatedEvent",)
