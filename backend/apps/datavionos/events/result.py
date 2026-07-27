"""
DatavionOS Event Result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(
    slots=True,
    frozen=True,
    kw_only=True,
)
class EventResult:
    """
    Represents the outcome of an event
    publication.
    """

    success: bool

    handlers_invoked: int = 0

    handlers_succeeded: int = 0

    handlers_failed: int = 0

    transport: str = "in-process"

    delivery_mode: str = "synchronous"

    retry_count: int = 0

    correlation_id: str = ""

    started_at: datetime | None = None

    completed_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    error: Exception | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def failed(
        self,
    ) -> bool:
        """
        Indicates whether publication failed.
        """

        return not self.success

    @property
    def duration_ms(
        self,
    ) -> float | None:
        """
        Publication duration in milliseconds.
        """

        if self.started_at is None:
            return None

        return (self.completed_at - self.started_at).total_seconds() * 1000

    @property
    def has_failures(
        self,
    ) -> bool:
        """
        Indicates whether any handler failed.
        """

        return self.handlers_failed > 0

    @classmethod
    def ok(
        cls,
        *,
        handlers_invoked: int,
        handlers_succeeded: int,
        handlers_failed: int = 0,
        transport: str = "in-process",
        delivery_mode: str = "synchronous",
        retry_count: int = 0,
        correlation_id: str = "",
        started_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EventResult:
        """
        Create a successful publication result.
        """

        return cls(
            success=True,
            handlers_invoked=handlers_invoked,
            handlers_succeeded=handlers_succeeded,
            handlers_failed=handlers_failed,
            transport=transport,
            delivery_mode=delivery_mode,
            retry_count=retry_count,
            correlation_id=correlation_id,
            started_at=started_at,
            metadata=metadata or {},
        )

    @classmethod
    def fail(
        cls,
        *,
        error: Exception,
        handlers_invoked: int = 0,
        handlers_succeeded: int = 0,
        handlers_failed: int = 0,
        transport: str = "in-process",
        delivery_mode: str = "synchronous",
        retry_count: int = 0,
        correlation_id: str = "",
        started_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EventResult:
        """
        Create a failed publication result.
        """

        return cls(
            success=False,
            handlers_invoked=handlers_invoked,
            handlers_succeeded=handlers_succeeded,
            handlers_failed=handlers_failed,
            transport=transport,
            delivery_mode=delivery_mode,
            retry_count=retry_count,
            correlation_id=correlation_id,
            started_at=started_at,
            error=error,
            metadata=metadata or {},
        )

    def with_metadata(
        self,
        **metadata: Any,
    ) -> EventResult:
        """
        Return a copy with merged metadata.
        """

        return EventResult(
            success=self.success,
            handlers_invoked=self.handlers_invoked,
            handlers_succeeded=self.handlers_succeeded,
            handlers_failed=self.handlers_failed,
            transport=self.transport,
            delivery_mode=self.delivery_mode,
            retry_count=self.retry_count,
            correlation_id=self.correlation_id,
            started_at=self.started_at,
            completed_at=self.completed_at,
            error=self.error,
            metadata={
                **self.metadata,
                **metadata,
            },
        )

    def __bool__(
        self,
    ) -> bool:
        """
        Truthiness based on success.
        """

        return self.success

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"success={self.success}, "
            f"handlers={self.handlers_succeeded}/"
            f"{self.handlers_invoked}, "
            f"failed={self.handlers_failed}, "
            f"transport={self.transport!r}, "
            f"duration_ms={self.duration_ms})"
        )


__all__ = [
    "EventResult",
]
