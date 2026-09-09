"""
Patient Identifier updated domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class IdentifierUpdatedEvent(DomainEvent):
    """
    Fired when a patient identifier is updated.

    Raw identifier values are deliberately excluded.
    """

    tenant_id: UUID
    actor_id: UUID
    identifier_id: UUID
    patient_id: UUID
    organization_id: UUID
    identifier_type: str


__all__ = ("IdentifierUpdatedEvent",)
