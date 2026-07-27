"""
DatavionOS Command Result.
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
class CommandResult:
    """
    Represents the outcome of a command
    execution.
    """

    success: bool

    value: Any = None

    error: Exception | None = None

    message: str = ""

    correlation_id: str = ""

    started_at: datetime | None = None

    completed_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def failed(
        self,
    ) -> bool:
        """
        Indicates whether execution failed.
        """

        return not self.success

    @property
    def has_value(
        self,
    ) -> bool:
        """
        Indicates whether a value exists.
        """

        return self.value is not None

    @property
    def has_error(
        self,
    ) -> bool:
        """
        Indicates whether an error exists.
        """

        return self.error is not None

    @property
    def duration_ms(
        self,
    ) -> float | None:
        """
        Execution duration in milliseconds.
        """

        if self.started_at is None:
            return None

        return (self.completed_at - self.started_at).total_seconds() * 1000

    @classmethod
    def ok(
        cls,
        value: Any = None,
        *,
        correlation_id: str = "",
        started_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> CommandResult:
        """
        Create a successful result.
        """

        return cls(
            success=True,
            value=value,
            correlation_id=correlation_id,
            started_at=started_at,
            metadata=metadata or {},
        )

    @classmethod
    def fail(
        cls,
        error: Exception,
        *,
        message: str = "",
        correlation_id: str = "",
        started_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> CommandResult:
        """
        Create a failed result.
        """

        return cls(
            success=False,
            error=error,
            message=message or str(error),
            correlation_id=correlation_id,
            started_at=started_at,
            metadata=metadata or {},
        )

    def with_metadata(
        self,
        **metadata: Any,
    ) -> CommandResult:
        """
        Return a new result with additional
        metadata.
        """

        return CommandResult(
            success=self.success,
            value=self.value,
            error=self.error,
            message=self.message,
            correlation_id=self.correlation_id,
            started_at=self.started_at,
            completed_at=self.completed_at,
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
            f"duration_ms={self.duration_ms}, "
            f"correlation_id={self.correlation_id!r})"
        )


__all__ = [
    "CommandResult",
]
