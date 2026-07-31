"""
Platform logging contracts.
"""

from __future__ import annotations

from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


@runtime_checkable
class Logger(
    Protocol,
):
    """
    Platform logger abstraction.

    Implementations may delegate to
    Python logging, OpenTelemetry,
    Serilog-style structured logging,
    or any enterprise logging backend.
    """

    def debug(
        self,
        message: str,
        **context: Any,
    ) -> None:
        """
        Log a debug message.
        """

    def info(
        self,
        message: str,
        **context: Any,
    ) -> None:
        """
        Log an informational message.
        """

    def warning(
        self,
        message: str,
        **context: Any,
    ) -> None:
        """
        Log a warning.
        """

    def error(
        self,
        message: str,
        *,
        exception: Exception | None = None,
        **context: Any,
    ) -> None:
        """
        Log an error.
        """

    def critical(
        self,
        message: str,
        *,
        exception: Exception | None = None,
        **context: Any,
    ) -> None:
        """
        Log a critical error.
        """

    def audit(
        self,
        action: str,
        **context: Any,
    ) -> None:
        """
        Write an immutable audit log.
        """

    def begin_scope(
        self,
        **context: Any,
    ) -> LogScope:
        """
        Begin a contextual logging scope.

        Example context:

        - tenant_id
        - organization_id
        - user_id
        - request_id
        - correlation_id
        """

    @property
    def name(
        self,
    ) -> str:
        """
        Logger name.
        """


@runtime_checkable
class LogScope(
    Protocol,
):
    """
    Context manager representing a
    structured logging scope.
    """

    def __enter__(
        self,
    ) -> LogScope: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: Any,
    ) -> None: ...


__all__ = [
    "Logger",
    "LogScope",
]
