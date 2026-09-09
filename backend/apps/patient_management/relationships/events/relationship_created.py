"""
Patient Relationship created domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class PatientRelationshipCreatedEvent(
    DomainEvent,
):
    """
    Emitted after a patient relationship is successfully created.
    """

    tenant_id: UUID
    actor_id: UUID
    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
    related_patient_id: UUID | None
    relationship_type: str
    status: str
    is_primary: bool


__all__ = ("PatientRelationshipCreatedEvent",)
