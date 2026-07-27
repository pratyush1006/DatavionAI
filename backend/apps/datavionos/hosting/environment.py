"""
Hosting environment contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
)


class EnvironmentType(
    StrEnum,
):
    """
    Supported hosting environments.
    """

    DEVELOPMENT = "development"

    TESTING = "testing"

    STAGING = "staging"

    PRODUCTION = "production"

    CUSTOM = "custom"


@dataclass(
    frozen=True,
    slots=True,
)
class Environment:
    """
    Immutable hosting environment.
    """

    name: str

    type: EnvironmentType

    region: str | None = None

    metadata: dict[str, Any] | None = None


__all__ = [
    "Environment",
    "EnvironmentType",
]
