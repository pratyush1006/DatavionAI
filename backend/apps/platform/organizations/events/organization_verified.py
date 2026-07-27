"""
Organization verified domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationVerifiedEvent(DomainEvent):
    """
    Raised when an organization has been verified.
    """

    organization_id: UUID

    verification_status: str


__all__: tuple[str, ...] = ("OrganizationVerifiedEvent",)
