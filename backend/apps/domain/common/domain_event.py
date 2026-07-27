"""
Domain event abstractions.
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
    UUID,
    uuid4,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DomainEvent:
    """
    Base class for all domain events.
    """

    event_id: UUID = field(
        default_factory=uuid4,
    )

    occurred_on: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    @property
    def event_name(
        self,
    ) -> str:
        """
        Return the event name.
        """
        return type(self).__name__
