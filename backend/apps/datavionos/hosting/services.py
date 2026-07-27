"""
Hosting service aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.hosting.health import (
    HealthChecker,
)
from apps.datavionos.hosting.host import (
    HostProvider,
)
from apps.datavionos.hosting.lifecycle import (
    ApplicationLifecycle,
)
from apps.datavionos.hosting.runtime import (
    RuntimeProvider,
)


@dataclass(
    frozen=True,
    slots=True,
)
class HostingServices:
    """
    Aggregate of hosting services.
    """

    host: HostProvider

    lifecycle: ApplicationLifecycle

    health: HealthChecker

    runtime: RuntimeProvider


__all__ = [
    "HostingServices",
]
