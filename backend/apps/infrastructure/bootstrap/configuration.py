"""
Bootstrap configuration contracts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class BootstrapConfiguration:
    """
    Immutable bootstrap configuration.
    """

    environment: str

    debug: bool = False

    settings: dict[str, Any] = field(
        default_factory=dict,
    )


__all__ = [
    "BootstrapConfiguration",
]
