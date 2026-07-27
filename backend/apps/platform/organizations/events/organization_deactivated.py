"""
Organization deactivated domain event.
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
class OrganizationDeactivatedEvent(DomainEvent):
    """
    Raised when an organization is deactivated.
    """

    organization_id: UUID

    reason: str | None = None


__all__: tuple[str, ...] = ("OrganizationDeactivatedEvent",)
