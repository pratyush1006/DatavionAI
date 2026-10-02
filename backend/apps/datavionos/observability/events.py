"""
Observability event contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
)
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class ObservationEventType(
    StrEnum,
):
    """
    Supported observability event types.
    """

    LOG = "log"

    METRIC = "metric"

    TRACE = "trace"

    AUDIT = "audit"

    SECURITY = "security"

    DIAGNOSTIC = "diagnostic"

    SYSTEM = "system"


@dataclass(
    frozen=True,
    slots=True,
)
class ObservationEvent:
    """
    Immutable observability event.
    """

    id: str

    type: ObservationEventType

    name: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    attributes: dict[str, Any] | None = None


@runtime_checkable
class ObservationEventPublisher(
    Protocol,
):
    """
    Publishes observability events.
    """

    async def publish(
        self,
        event: ObservationEvent,
    ) -> None:
        """
        Publish an observability event.
        """

    async def publish_batch(
        self,
        events: tuple[ObservationEvent, ...],
    ) -> None:
        """
        Publish multiple observability events.
        """


__all__ = [
    "ObservationEvent",
    "ObservationEventPublisher",
    "ObservationEventType",
]
