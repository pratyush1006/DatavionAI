"""
Registry bootstrap for DatavionOS.

Responsible for constructing and initializing all platform registries
during kernel startup.
"""

from __future__ import annotations

from collections.abc import Iterable

from ..contracts.capability import CapabilityContract
from ..contracts.module import ModuleContract
from ..contracts.plugin import PluginContract
from ..contracts.service import ServiceContract
from .capability import CapabilityRegistry
from .module import ModuleRegistry
from .plugin import PluginRegistry
from .registry import Registry
from .service import ServiceRegistry


class RegistryBootstrap:
    """
    Bootstraps every registry required by DatavionOS.

    The bootstrap owns every registry instance and exposes them to
    the DatavionOS kernel.
    """

    def __init__(self) -> None:
        self._registries = Registry[
            str,
            object,
        ](
            name="registries",
        )

        self._modules = ModuleRegistry()
        self._capabilities = CapabilityRegistry()
        self._services = ServiceRegistry()
        self._plugins = PluginRegistry()

        self._registries.register(
            key="modules",
            value=self._modules,
        )

        self._registries.register(
            key="capabilities",
            value=self._capabilities,
        )

        self._registries.register(
            key="services",
            value=self._services,
        )

        self._registries.register(
            key="plugins",
            value=self._plugins,
        )

    # ------------------------------------------------------------------
    # Registry Properties
    # ------------------------------------------------------------------

    @property
    def registries(
        self,
    ) -> Registry[
        str,
        object,
    ]:
        """
        Root registry.
        """
        return self._registries

    @property
    def modules(
        self,
    ) -> ModuleRegistry:
        """
        Module registry.
        """
        return self._modules

    @property
    def capabilities(
        self,
    ) -> CapabilityRegistry:
        """
        Capability registry.
        """
        return self._capabilities

    @property
    def services(
        self,
    ) -> ServiceRegistry:
        """
        Service registry.
        """
        return self._services

    @property
    def plugins(
        self,
    ) -> PluginRegistry:
        """
        Plugin registry.
        """
        return self._plugins

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_modules(
        self,
        modules: Iterable[ModuleContract],
    ) -> None:
        """
        Register platform modules.
        """
        self._modules.register_modules(
            modules,
        )

    def register_capabilities(
        self,
        capabilities: Iterable[CapabilityContract],
    ) -> None:
        """
        Register capabilities.
        """
        self._capabilities.register_capabilities(
            capabilities,
        )

    def register_services(
        self,
        services: Iterable[ServiceContract],
    ) -> None:
        """
        Register services.
        """
        self._services.register_services(
            services,
        )

    def register_plugins(
        self,
        plugins: Iterable[PluginContract],
    ) -> None:
        """
        Register plugins.
        """
        self._plugins.register_plugins(
            plugins,
        )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_registry(
        self,
        name: str,
    ) -> object | None:
        """
        Retrieve a registry by name.
        """
        return self._registries.get(
            name,
        )

    def require_registry(
        self,
        name: str,
    ) -> object:
        """
        Retrieve a required registry.
        """
        return self._registries.require(
            name,
        )

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def registry_count(
        self,
    ) -> int:
        """
        Return the number of registered registries.
        """
        return self._registries.size

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """
        Clear all platform registries.
        """
        self._modules.clear()
        self._capabilities.clear()
        self._services.clear()
        self._plugins.clear()

    def reset(self) -> None:
        """
        Reset every registry.
        """
        self.clear()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate every registry.
        """
        self._modules.validate()
        self._capabilities.validate()
        self._services.validate()
        self._plugins.validate()

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def snapshot(
        self,
    ) -> dict[str, object]:
        """
        Export the registry bootstrap state.
        """
        return {
            "modules": self._modules.snapshot(),
            "capabilities": self._capabilities.snapshot(),
            "services": self._services.snapshot(),
            "plugins": self._plugins.snapshot(),
        }

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Return the number of registries.
        """
        return self.registry_count

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """
        return f"{type(self).__name__}(registries={self.registry_count})"


__all__ = [
    "RegistryBootstrap",
]
