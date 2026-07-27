"""
Messaging contracts.
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
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class Message:
    """
    Base message contract.
    """

    id: str

    name: str

    correlation_id: str | None = None

    causation_id: str | None = None

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    payload: dict[str, Any] = field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


__all__ = [
    "Message",
]
