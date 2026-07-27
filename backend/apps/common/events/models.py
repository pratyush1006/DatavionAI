"""
Event models for DatavionOS.

Provides immutable event models used by the platform event
framework.

Events are framework objects and should not contain business logic.
Feature applications define concrete event payloads.
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
from uuid import (
    uuid4,
)

from apps.common.events.constants import (
    DEFAULT_EVENT_SOURCE,
    DEFAULT_EVENT_VERSION,
)
from apps.common.events.types import (
    EventID,
    EventMetadata,
    EventName,
    EventPayload,
)


@dataclass(
    frozen=True,
    slots=True,
)
class Event:
    """
    Base immutable platform event.

    Represents an event published inside DatavionOS.

    Example:

        Event(
            name="organization.created",
            payload={
                "organization_id": "123"
            }
        )
    """

    name: EventName

    payload: EventPayload = field(
        default_factory=dict,
    )

    metadata: EventMetadata = field(
        default_factory=dict,
    )

    event_id: EventID = field(
        default_factory=lambda: str(uuid4()),
    )

    version: str = DEFAULT_EVENT_VERSION

    source: str = DEFAULT_EVENT_SOURCE

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    @property
    def event_name(
        self,
    ) -> EventName:
        """
        Return the event name.

        Alias provided for compatibility with the
        event envelope contract.
        """

        return self.name


@dataclass(
    frozen=True,
    slots=True,
)
class EventResult:
    """
    Result returned after event dispatching.

    Allows the event framework to report handler execution
    without coupling to business implementations.
    """

    event_id: EventID

    handled: bool = True

    handlers_executed: int = 0


__all__: tuple[str, ...] = (
    "Event",
    "EventResult",
)
