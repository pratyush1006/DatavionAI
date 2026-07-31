"""
Document updated domain event.
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
class DocumentUpdatedEvent(
    DomainEvent,
):
    """
    Fired after document update.
    """

    tenant_id: UUID

    actor_id: UUID

    document_id: UUID

    organization_id: UUID


__all__ = ("DocumentUpdatedEvent",)
