"""
Family Member created domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class FamilyMemberCreatedEvent(
    DomainEvent,
):
    """
    Fired when a family member is created.

    Carries enough context for:

    - Audit logging
    - Notifications
    - Search indexing
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
    status: str
    is_next_of_kin: bool
    is_emergency_contact: bool


__all__ = ("FamilyMemberCreatedEvent",)
