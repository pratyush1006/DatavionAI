"""
Application contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
)


class ApplicationStatus(
    StrEnum,
):
    """
    Application status.
    """

    CREATED = "created"

    INITIALIZED = "initialized"

    STARTING = "starting"

    RUNNING = "running"

    STOPPING = "stopping"

    STOPPED = "stopped"

    FAILED = "failed"


@dataclass(
    frozen=True,
    slots=True,
)
class Application:
    """
    Immutable application definition.
    """

    id: str

    name: str

    version: str

    status: ApplicationStatus = ApplicationStatus.CREATED

    metadata: dict[str, Any] | None = None


__all__ = [
    "Application",
    "ApplicationStatus",
]
