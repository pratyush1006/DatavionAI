"""
Configuration validation contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.configuration.configuration import (
    ConfigurationEntry,
    ConfigurationSnapshot,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ValidationError:
    """
    Immutable configuration validation error.
    """

    key: str

    message: str


@dataclass(
    frozen=True,
    slots=True,
)
class ValidationResult:
    """
    Immutable configuration validation result.
    """

    valid: bool

    errors: tuple[ValidationError, ...] = ()

    warnings: tuple[str, ...] = ()

    metadata: dict[str, str] = field(
        default_factory=dict,
    )


@runtime_checkable
class ConfigurationValidator(
    Protocol,
):
    """
    Validates configuration.
    """

    async def validate_entry(
        self,
        entry: ConfigurationEntry,
    ) -> ValidationResult:
        """
        Validate a configuration entry.
        """

    async def validate_snapshot(
        self,
        snapshot: ConfigurationSnapshot,
    ) -> ValidationResult:
        """
        Validate a configuration snapshot.
        """


__all__ = [
    "ConfigurationValidator",
    "ValidationError",
    "ValidationResult",
]
