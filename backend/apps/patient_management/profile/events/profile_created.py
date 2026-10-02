"""
Patient Profile created domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import (
    DomainEvent,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ProfileCreatedEvent(
    DomainEvent,
):
    """
    Fired when a patient profile is created.
    """

    tenant_id: UUID
    actor_id: UUID
    profile_id: UUID
    patient_id: UUID
    organization_id: UUID


__all__ = ("ProfileCreatedEvent",)
