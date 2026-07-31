"""
Configuration contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from enum import StrEnum
from typing import (
    Any,
)


class ConfigurationScope(
    StrEnum,
):
    """
    Configuration scope.
    """

    GLOBAL = "global"

    TENANT = "tenant"

    ORGANIZATION = "organization"

    USER = "user"

    SESSION = "session"


@dataclass(
    frozen=True,
    slots=True,
)
class ConfigurationEntry:
    """
    Immutable configuration entry.
    """

    key: str

    value: Any

    scope: ConfigurationScope = ConfigurationScope.GLOBAL

    description: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class ConfigurationSnapshot:
    """
    Immutable configuration snapshot.
    """

    entries: tuple[ConfigurationEntry, ...] = ()

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


__all__ = [
    "ConfigurationEntry",
    "ConfigurationScope",
    "ConfigurationSnapshot",
]
