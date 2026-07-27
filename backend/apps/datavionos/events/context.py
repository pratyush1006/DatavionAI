"""
DatavionOS Event Context.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from apps.datavionos.events.event import (
    Event,
)


@dataclass(
    slots=True,
    kw_only=True,
)
class EventContext:
    """
    Runtime execution context for an event.

    Carries runtime state throughout the
    event publication pipeline.
    """

    event: Event

    container: Any | None = None

    correlation_id: str = ""

    causation_id: str = ""

    request_id: str = ""

    tenant_id: str = ""

    organization_id: str = ""

    user_id: str = ""

    transport: str = "in-process"

    delivery_mode: str = "synchronous"

    retry_count: int = 0

    max_retries: int = 0

    idempotency_key: str = ""

    partition_key: str = ""

    routing_key: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    items: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def event_name(
        self,
    ) -> str:
        """
        Event name.
        """

        return self.event.event_name

    @property
    def can_retry(
        self,
    ) -> bool:
        """
        Whether another retry is allowed.
        """

        return self.retry_count < self.max_retries

    def increment_retry(
        self,
    ) -> None:
        """
        Increment retry count.
        """

        self.retry_count += 1

    def set_item(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store runtime item.
        """

        self.items[key] = value

    def get_item(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve runtime item.
        """

        return self.items.get(
            key,
            default,
        )

    def remove_item(
        self,
        key: str,
    ) -> None:
        """
        Remove runtime item.
        """

        self.items.pop(
            key,
            None,
        )

    def clear_items(
        self,
    ) -> None:
        """
        Clear runtime items.
        """

        self.items.clear()

    def update_metadata(
        self,
        **metadata: Any,
    ) -> None:
        """
        Merge metadata.
        """

        self.metadata.update(
            metadata,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"event={self.event_name!r}, "
            f"transport={self.transport!r}, "
            f"delivery_mode={self.delivery_mode!r}, "
            f"retry_count={self.retry_count}, "
            f"tenant_id={self.tenant_id!r})"
        )


__all__ = [
    "EventContext",
]
