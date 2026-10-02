"""
Organization created domain event.
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
class OrganizationCreatedEvent(DomainEvent):
    """
    Raised after a new organization has been created.
    """

    organization_id: UUID

    organization_code: str

    organization_name: str

    organization_type: str

    organization_category: str


__all__: tuple[str, ...] = ("OrganizationCreatedEvent",)
