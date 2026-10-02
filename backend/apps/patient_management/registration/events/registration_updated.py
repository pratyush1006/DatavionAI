"""
Patient Registration updated domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(frozen=True, slots=True)
class RegistrationUpdatedEvent(DomainEvent):
    """
    Published after a patient registration is successfully updated.

    The event contains identifiers and operation metadata only.
    Sensitive patient data is not embedded in the event payload.
    """

    tenant_id: UUID
    actor_id: UUID
    registration_id: UUID
    patient_id: UUID
    organization_id: UUID
    registration_number: str
    changes: dict[str, Any]

    @property
    def event_type(self) -> str:
        """Return the stable event type identifier."""
        return "patient_registration.updated"


__all__ = ("RegistrationUpdatedEvent",)
