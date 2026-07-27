"""
Infrastructure module registration contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.infrastructure.container import (
    ServiceProvider,
)


@runtime_checkable
class InfrastructureModule(
    Protocol,
):
    """
    Infrastructure module contract.
    """

    def register(
        self,
        services: ServiceProvider,
    ) -> None:
        """
        Register services into the container.
        """


__all__ = [
    "InfrastructureModule",
]
