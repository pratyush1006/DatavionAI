"""
Family Member status changed domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class FamilyMemberStatusChangedEvent(
    DomainEvent,
):
    """
    Fired when a family member lifecycle status changes.
    """

    tenant_id: UUID
    actor_id: UUID
    family_member_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str


__all__ = ("FamilyMemberStatusChangedEvent",)
