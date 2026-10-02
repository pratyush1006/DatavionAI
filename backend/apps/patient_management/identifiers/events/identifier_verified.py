"""
Patient Identifier verification domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class IdentifierVerifiedEvent(DomainEvent):
    """
    Fired when a patient identifier verification is completed.

    The event contains verification state and actor context, but no raw
    identifier value or verification reference.
    """

    tenant_id: UUID
    actor_id: UUID
    identifier_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str


__all__ = ("IdentifierVerifiedEvent",)
