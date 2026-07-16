"""
Platform module definition.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class PlatformModule:
    """
    Represents a platform module registered with the platform kernel.
    """

    key: str

    title: str

    description: str

    route: str

    icon: str

    permission: str

    category: str

    order: int

    enabled: bool = True


__all__ = [
    "PlatformModule",
]
