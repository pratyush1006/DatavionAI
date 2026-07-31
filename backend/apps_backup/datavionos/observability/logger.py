"""
Logging contracts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
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


class LogLevel(
    StrEnum,
):
    """
    Supported log levels.
    """

    TRACE = "trace"

    DEBUG = "debug"

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"

    CRITICAL = "critical"


@dataclass(
    frozen=True,
    slots=True,
)
class LogRecord:
    """
    Immutable log record.
    """

    level: LogLevel

    message: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    logger: str | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class Logger(
    Protocol,
):
    """
    Structured logger.
    """

    async def log(
        self,
        record: LogRecord,
    ) -> None:
        """
        Write a log record.
        """

    async def trace(
        self,
        message: str,
        **metadata: Any,
    ) -> None:
        """
        Write a trace log.
        """

    async def debug(
        self,
        message: str,
        **metadata: Any,
    ) -> None:
        """
        Write a debug log.
        """

    async def info(
        self,
        message: str,
        **metadata: Any,
    ) -> None:
        """
        Write an informational log.
        """

    async def warning(
        self,
        message: str,
        **metadata: Any,
    ) -> None:
        """
        Write a warning log.
        """

    async def error(
        self,
        message: str,
        **metadata: Any,
    ) -> None:
        """
        Write an error log.
        """

    async def critical(
        self,
        message: str,
        **metadata: Any,
    ) -> None:
        """
        Write a critical log.
        """


__all__ = [
    "LogLevel",
    "Logger",
    "LogRecord",
]
