"""
DatavionOS Domain Event Contract.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(
    slots=True,
    frozen=True,
    kw_only=True,
)
class Event(ABC):
    """
    Base class for all DatavionOS events.

    Events represent facts that have
    already occurred and are immutable.
    """

    event_id: str = field(
        default_factory=lambda: str(
            uuid4(),
        ),
    )

    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    correlation_id: str = ""

    causation_id: str = ""

    aggregate_id: str = ""

    aggregate_type: str = ""

    aggregate_version: int = 1

    tenant_id: str = ""

    organization_id: str = ""

    user_id: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def event_name(
        self,
    ) -> str:
        """
        Fully qualified event name.
        """

        return self.__class__.__qualname__

    @property
    def event_version(
        self,
    ) -> int:
        """
        Schema version.

        Override in derived events when
        introducing breaking changes.
        """

        return 1

    @property
    def is_domain_event(
        self,
    ) -> bool:
        """
        Indicates whether this is a
        domain event.
        """

        return True

    @property
    def is_integration_event(
        self,
    ) -> bool:
        """
        Indicates whether this is an
        integration event.
        """

        return False

    def with_metadata(
        self,
        **metadata: Any,
    ) -> Event:
        """
        Return a copy with merged
        metadata.
        """

        merged = {
            **self.metadata,
            **metadata,
        }

        return self.__class__(
            event_id=self.event_id,
            occurred_at=self.occurred_at,
            correlation_id=self.correlation_id,
            causation_id=self.causation_id,
            aggregate_id=self.aggregate_id,
            aggregate_type=self.aggregate_type,
            aggregate_version=self.aggregate_version,
            tenant_id=self.tenant_id,
            organization_id=self.organization_id,
            user_id=self.user_id,
            metadata=merged,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.event_name}("
            f"id={self.event_id!r}, "
            f"aggregate={self.aggregate_type!r}, "
            f"version={self.aggregate_version})"
        )


__all__ = [
    "Event",
]
