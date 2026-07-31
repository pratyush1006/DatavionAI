"""
Diagnostics contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class DiagnosticStatus(
    StrEnum,
):
    """
    Status of a diagnostic component.
    """

    OK = "ok"

    WARNING = "warning"

    ERROR = "error"

    UNKNOWN = "unknown"


@dataclass(
    frozen=True,
    slots=True,
)
class Diagnostic:
    """
    Immutable diagnostic record.
    """

    component: str

    status: DiagnosticStatus

    message: str | None = None

    details: dict[str, Any] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class DiagnosticReport:
    """
    Immutable diagnostic report.
    """

    diagnostics: tuple[Diagnostic, ...] = ()

    metadata: dict[str, Any] | None = None


@runtime_checkable
class DiagnosticsProvider(
    Protocol,
):
    """
    Provides runtime diagnostics.
    """

    async def check(
        self,
    ) -> DiagnosticReport:
        """
        Collect diagnostic information.
        """

    async def component(
        self,
        name: str,
    ) -> Diagnostic | None:
        """
        Return diagnostics for a component.
        """

    async def components(
        self,
    ) -> tuple[Diagnostic, ...]:
        """
        Return diagnostics for all components.
        """


__all__ = [
    "Diagnostic",
    "DiagnosticReport",
    "DiagnosticStatus",
    "DiagnosticsProvider",
]
