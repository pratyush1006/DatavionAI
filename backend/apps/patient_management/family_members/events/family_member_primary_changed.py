"""
Family Member designation changed domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class FamilyMemberPrimaryChangedEvent(
    DomainEvent,
):
    """
    Fired when a family member's special designation changes.

    The flag identifies which designation changed:

    - next_of_kin
    - emergency_contact
    """

    tenant_id: UUID
    actor_id: UUID
    family_member_id: UUID
    patient_id: UUID
    organization_id: UUID
    flag: str
    previous_value: bool
    new_value: bool


__all__ = ("FamilyMemberPrimaryChangedEvent",)
