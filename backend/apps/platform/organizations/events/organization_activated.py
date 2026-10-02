"""
Organization activated domain event.
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
class OrganizationActivatedEvent(DomainEvent):
    """
    Raised when an organization is activated.
    """

    organization_id: UUID


__all__: tuple[str, ...] = ("OrganizationActivatedEvent",)
