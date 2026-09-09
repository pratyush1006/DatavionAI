"""
Patient status changed domain event.
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
class PatientStatusChangedEvent(DomainEvent):
    """
    Emitted when a patient's lifecycle status changes.
    """

    tenant_id: UUID
    actor_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str


__all__: tuple[str, ...] = ("PatientStatusChangedEvent",)
