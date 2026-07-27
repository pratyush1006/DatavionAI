"""
Organization restored domain event.
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
class OrganizationRestoredEvent(DomainEvent):
    """
    Raised when a previously deleted or suspended organization is restored.
    """

    organization_id: UUID


__all__: tuple[str, ...] = ("OrganizationRestoredEvent",)
