"""
Default application bootstrap.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.infrastructure.bootstrap.builder import (
    BootstrapBuilder,
)
from apps.infrastructure.bootstrap.configuration import (
    BootstrapConfiguration,
)
from apps.infrastructure.bootstrap.modules import (
    InfrastructureModule,
)
from apps.infrastructure.container import (
    Container,
    ServiceProvider,
)


class DefaultBootstrapBuilder(
    BootstrapBuilder,
):
    """
    Default DatavionOS bootstrap builder.
    """

    def __init__(
        self,
        modules: Iterable[InfrastructureModule] = (),
    ) -> None:
        self._modules = tuple(modules)

    def build(
        self,
        configuration: BootstrapConfiguration,
    ) -> ServiceProvider:
        """
        Build the application's service provider.
        """
        container = Container()

        # Future:
        # Register configuration
        container.register_instance(
            BootstrapConfiguration,
            configuration,
        )

        # Register infrastructure modules
        for module in self._modules:
            module.register(container)

        return container


__all__ = [
    "DefaultBootstrapBuilder",
]
