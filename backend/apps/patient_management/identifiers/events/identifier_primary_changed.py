"""
Patient Identifier primary-status domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class IdentifierPrimaryChangedEvent(DomainEvent):
    """
    Fired when an identifier becomes or ceases to be primary.

    Only identifiers belonging to the same patient and identifier type are
    affected by the primary designation.
    """

    tenant_id: UUID
    actor_id: UUID
    identifier_id: UUID
    patient_id: UUID
    organization_id: UUID
    identifier_type: str
    previous_primary: bool
    new_primary: bool


__all__ = ("IdentifierPrimaryChangedEvent",)
