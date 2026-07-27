"""
Application lifecycle contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.hosting.application import (
    Application,
)


@runtime_checkable
class ApplicationLifecycle(
    Protocol,
):
    """
    Manages the lifecycle of an application.
    """

    async def initialize(
        self,
        application: Application,
    ) -> None:
        """
        Initialize the application.
        """

    async def start(
        self,
        application: Application,
    ) -> None:
        """
        Start the application.
        """

    async def stop(
        self,
        application: Application,
    ) -> None:
        """
        Stop the application.
        """

    async def restart(
        self,
        application: Application,
    ) -> None:
        """
        Restart the application.
        """

    async def shutdown(
        self,
        application: Application,
    ) -> None:
        """
        Shut down the application gracefully.
        """


__all__ = [
    "ApplicationLifecycle",
]
