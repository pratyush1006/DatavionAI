"""
Patient Identifier created domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class IdentifierCreatedEvent(DomainEvent):
    """
    Fired when a patient identifier is created.

    The event intentionally contains identifier metadata only. Sensitive
    identifier values are never included in domain events.
    """

    tenant_id: UUID
    actor_id: UUID
    identifier_id: UUID
    patient_id: UUID
    organization_id: UUID
    identifier_type: str
    status: str


__all__ = ("IdentifierCreatedEvent",)
