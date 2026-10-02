"""
Distributed tracing contracts.
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
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


@dataclass(
    frozen=True,
    slots=True,
)
class Span:
    """
    Immutable trace span.
    """

    id: str

    name: str

    trace_id: str

    parent_span_id: str | None = None

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    ended_at: datetime | None = None

    attributes: dict[str, Any] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class Trace:
    """
    Immutable distributed trace.
    """

    id: str

    root_span_id: str

    spans: tuple[Span, ...] = ()

    attributes: dict[str, Any] | None = None


@runtime_checkable
class Tracer(
    Protocol,
):
    """
    Distributed tracing provider.
    """

    async def start_trace(
        self,
        name: str,
        **attributes: Any,
    ) -> Trace:
        """
        Start a distributed trace.
        """

    async def finish_trace(
        self,
        trace: Trace,
    ) -> None:
        """
        Finish a distributed trace.
        """

    async def start_span(
        self,
        trace: Trace,
        name: str,
        parent_span: Span | None = None,
        **attributes: Any,
    ) -> Span:
        """
        Start a span.
        """

    async def finish_span(
        self,
        span: Span,
    ) -> None:
        """
        Finish a span.
        """


__all__ = [
    "Span",
    "Trace",
    "Tracer",
]
