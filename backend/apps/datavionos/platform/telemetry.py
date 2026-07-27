"""
Platform telemetry contracts.
"""

from __future__ import annotations

from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

TelemetryAttributes = dict[str, str | int | float | bool]


@runtime_checkable
class Span(
    Protocol,
):
    """
    Represents a telemetry span.
    """

    @property
    def trace_id(
        self,
    ) -> str:
        """
        Distributed trace identifier.
        """

    @property
    def span_id(
        self,
    ) -> str:
        """
        Span identifier.
        """

    def set_attribute(
        self,
        key: str,
        value: str | int | float | bool,
    ) -> None:
        """
        Set a span attribute.
        """

    def add_event(
        self,
        name: str,
        **attributes: Any,
    ) -> None:
        """
        Record an event.
        """

    def record_exception(
        self,
        exception: BaseException,
    ) -> None:
        """
        Record an exception.
        """

    def set_status(
        self,
        success: bool,
        description: str | None = None,
    ) -> None:
        """
        Set span completion status.
        """

    def __enter__(
        self,
    ) -> Span: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: Any,
    ) -> None: ...


@runtime_checkable
class Tracer(
    Protocol,
):
    """
    Creates distributed tracing spans.
    """

    def start_span(
        self,
        name: str,
        *,
        attributes: TelemetryAttributes | None = None,
    ) -> Span:
        """
        Start a new span.
        """

    @property
    def current_span(
        self,
    ) -> Span | None:
        """
        Return the currently active span.
        """


@runtime_checkable
class TelemetryService(
    Protocol,
):
    """
    Platform telemetry abstraction.
    """

    @property
    def tracer(
        self,
    ) -> Tracer:
        """
        Return the platform tracer.
        """

    def flush(
        self,
    ) -> None:
        """
        Flush buffered telemetry.
        """


__all__ = [
    "TelemetryAttributes",
    "Span",
    "Tracer",
    "TelemetryService",
]
