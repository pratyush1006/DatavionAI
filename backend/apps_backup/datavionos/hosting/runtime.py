"""
Application runtime contracts.
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
class Runtime:
    """
    Immutable runtime information.
    """

    name: str

    version: str

    process_id: int

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    metadata: dict[str, Any] | None = None


@runtime_checkable
class RuntimeProvider(
    Protocol,
):
    """
    Provides runtime information.
    """

    async def current(
        self,
    ) -> Runtime:
        """
        Return the current runtime.
        """

    async def uptime(
        self,
    ) -> float:
        """
        Return the application uptime in seconds.
        """

    async def metadata(
        self,
    ) -> dict[str, Any]:
        """
        Return runtime metadata.
        """


__all__ = [
    "Runtime",
    "RuntimeProvider",
]
