"""
Base domain event infrastructure.

This module defines the immutable base class for all domain events emitted
throughout the DatavionAI platform.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DomainEvent:
    """
    Base class for all domain events.

    Every domain event should inherit from this class and declare only
    its business-specific payload.
    """

    event_id: UUID = field(
        default_factory=uuid4,
    )

    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    correlation_id: UUID | None = None

    causation_id: UUID | None = None

    tenant_id: UUID | None = None

    actor_id: UUID | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def event_name(self) -> str:
        """
        Return the event class name.
        """
        return self.__class__.__name__

    @property
    def event_type(self) -> str:
        """
        Return the fully-qualified event type.
        """
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}"

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the event into a dictionary.
        """
        return {
            "event_id": str(self.event_id),
            "event_name": self.event_name,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at.isoformat(),
            "correlation_id": (
                str(self.correlation_id) if self.correlation_id else None
            ),
            "causation_id": (str(self.causation_id) if self.causation_id else None),
            "tenant_id": (str(self.tenant_id) if self.tenant_id else None),
            "actor_id": (str(self.actor_id) if self.actor_id else None),
            "metadata": self.metadata,
        }


__all__: tuple[str, ...] = ("DomainEvent",)
