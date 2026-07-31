"""
Document deleted domain event.
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
class DocumentDeletedEvent(
    DomainEvent,
):
    """
    Fired after document deletion.
    """

    tenant_id: UUID

    actor_id: UUID

    document_id: UUID

    organization_id: UUID


__all__ = ("DocumentDeletedEvent",)
