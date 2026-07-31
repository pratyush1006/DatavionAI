"""
Hosting platform contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.datavionos.hosting.application import (
    Application,
)
from apps.datavionos.hosting.environment import (
    Environment,
)
from apps.datavionos.hosting.health import (
    HealthReport,
)
from apps.datavionos.hosting.runtime import (
    Runtime,
)


class HostType(
    StrEnum,
):
    """
    Supported host types.
    """

    LOCAL = "local"

    CONTAINER = "container"

    VIRTUAL_MACHINE = "virtual_machine"

    KUBERNETES = "kubernetes"

    SERVERLESS = "serverless"

    CLOUD_SERVICE = "cloud_service"

    CUSTOM = "custom"


@dataclass(
    frozen=True,
    slots=True,
)
class Host:
    """
    Immutable hosting platform.
    """

    id: str

    name: str

    type: HostType

    environment: Environment

    metadata: dict[str, Any] | None = None


@runtime_checkable
class HostProvider(
    Protocol,
):
    """
    Provides access to the hosting platform.
    """

    async def application(
        self,
    ) -> Application:
        """
        Return the hosted application.
        """

    async def runtime(
        self,
    ) -> Runtime:
        """
        Return the active runtime.
        """

    async def health(
        self,
    ) -> HealthReport:
        """
        Return the current health report.
        """

    async def host(
        self,
    ) -> Host:
        """
        Return host information.
        """


__all__ = [
    "Host",
    "HostProvider",
    "HostType",
]
