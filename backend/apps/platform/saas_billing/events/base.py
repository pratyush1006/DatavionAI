"""
Base domain event definitions.

Common foundation for
DatavionOS SaaS Billing events.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(
    frozen=True,
)
class DomainEvent:
    """
    Base domain event.

    All SaaS billing events inherit
    from this class.
    """

    event_id: UUID = field(
        default_factory=uuid4,
    )

    occurred_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    aggregate_id: UUID | None = None

    metadata: dict = field(
        default_factory=dict,
    )


__all__ = [
    "DomainEvent",
]
