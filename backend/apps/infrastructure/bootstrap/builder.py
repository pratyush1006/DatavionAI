"""
Bootstrap builder contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.infrastructure.bootstrap.configuration import (
    BootstrapConfiguration,
)
from apps.infrastructure.container import (
    ServiceProvider,
)


@runtime_checkable
class BootstrapBuilder(
    Protocol,
):
    """
    Application bootstrap builder.
    """

    def build(
        self,
        configuration: BootstrapConfiguration,
    ) -> ServiceProvider:
        """
        Build and configure the application's service provider.
        """


__all__ = [
    "BootstrapBuilder",
]
