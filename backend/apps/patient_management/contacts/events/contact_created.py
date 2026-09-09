"""
Patient Contact created domain event.

The event intentionally excludes the contact value because contact values
are personally identifiable patient information.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class ContactCreatedEvent(
    DomainEvent,
):
    """
    Fired after a Patient Contact has been created.
    """

    tenant_id: UUID
    actor_id: UUID
    contact_id: UUID
    patient_id: UUID
    organization_id: UUID
    contact_type: str
    purpose: str
    status: str
    is_primary: bool
    is_preferred: bool


__all__ = ("ContactCreatedEvent",)
