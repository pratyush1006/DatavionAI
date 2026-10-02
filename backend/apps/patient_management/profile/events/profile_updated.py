"""
Patient Profile updated domain event.
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
class ProfileUpdatedEvent(
    DomainEvent,
):
    """
    Fired when a patient profile is updated.
    """

    tenant_id: UUID
    actor_id: UUID
    profile_id: UUID
    patient_id: UUID
    organization_id: UUID


__all__ = ("ProfileUpdatedEvent",)
