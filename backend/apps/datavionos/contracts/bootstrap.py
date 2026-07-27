"""
Bootstrap contract definitions.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
)

from apps.datavionos.contracts.base import (
    BaseContract,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BootstrapContract(BaseContract):
    """
    Immutable bootstrap definition.
    """

    identifier: str

    environment: str

    version: str = "1.0.0"

    description: str = ""

    modules: tuple[str, ...] = ()

    plugins: tuple[str, ...] = ()

    services: tuple[str, ...] = ()

    enabled: bool = True

    system: bool = False

    @property
    def qualified_name(self) -> str:
        """
        Qualified bootstrap identifier.
        """

        return f"{self.environment}:{self.version}"

    @property
    def has_modules(self) -> bool:
        """
        Whether modules are registered.
        """

        return bool(
            self.modules,
        )

    @property
    def has_plugins(self) -> bool:
        """
        Whether plugins are registered.
        """

        return bool(
            self.plugins,
        )


__all__ = [
    "BootstrapContract",
]
