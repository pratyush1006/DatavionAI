"""
Family Member deleted domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class FamilyMemberDeletedEvent(
    DomainEvent,
):
    """
    Fired when a family member is soft-deleted.

    Carries enough context for:

    - Audit logging
    - Notifications
    - Search cleanup
    - Integration events
    - Analytics pipelines
    """

    tenant_id: UUID
    actor_id: UUID
    family_member_id: UUID
    patient_id: UUID
    organization_id: UUID
    family_member_number: str
    relationship: str
    was_next_of_kin: bool
    was_emergency_contact: bool


__all__ = ("FamilyMemberDeletedEvent",)
