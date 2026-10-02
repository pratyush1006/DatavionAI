"""
Document version created domain event.
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
class DocumentVersionCreatedEvent(
    DomainEvent,
):
    """
    Fired after a new document version is created.
    """

    tenant_id: UUID

    actor_id: UUID

    document_id: UUID

    version_id: UUID

    organization_id: UUID


__all__ = ("DocumentVersionCreatedEvent",)
