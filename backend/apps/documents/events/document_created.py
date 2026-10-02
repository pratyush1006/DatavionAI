"""
Document created domain event.
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
class DocumentCreatedEvent(
    DomainEvent,
):
    """
    Fired after document creation.
    """

    tenant_id: UUID

    actor_id: UUID

    document_id: UUID

    organization_id: UUID


__all__ = ("DocumentCreatedEvent",)
