"""
Patient Identifier deleted domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class IdentifierDeletedEvent(DomainEvent):
    """
    Fired when a patient identifier is deleted.

    The identifier value is intentionally not included.
    """

    tenant_id: UUID
    actor_id: UUID
    identifier_id: UUID
    patient_id: UUID
    organization_id: UUID
    identifier_type: str


__all__ = ("IdentifierDeletedEvent",)
