"""
Plugin registry for DatavionOS.

This module provides the registry responsible for managing plugins
throughout the DatavionOS platform.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.datavionos.exceptions import RegistryError
from apps.datavionos.types import PluginName

from ..contracts.plugin import PluginContract
from .registry import Registry


class PluginRegistry(
    Registry[
        PluginName,
        PluginContract,
    ],
):
    """
    Registry of DatavionOS plugins.

    Plugins extend the platform with optional functionality,
    integrations and AI capabilities.
    """

    def __init__(self) -> None:
        super().__init__(
            name="plugins",
        )

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_plugin(
        self,
        plugin: PluginContract,
    ) -> PluginContract:
        """
        Register a plugin.
        """
        return self.register(
            key=plugin.name,
            value=plugin,
        )

    def register_plugins(
        self,
        plugins: Iterable[PluginContract],
    ) -> None:
        """
        Register multiple plugins.
        """
        for plugin in plugins:
            self.register_plugin(
                plugin,
            )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_plugin(
        self,
        name: PluginName,
    ) -> PluginContract | None:
        """
        Retrieve a plugin.
        """
        return self.get(
            name,
        )

    def require_plugin(
        self,
        name: PluginName,
    ) -> PluginContract:
        """
        Retrieve a required plugin.
        """
        return self.require(
            name,
        )

    def unregister_plugin(
        self,
        name: PluginName,
    ) -> PluginContract:
        """
        Remove a plugin.
        """
        return self.unregister(
            name,
        )

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def enabled_plugins(
        self,
    ) -> list[PluginContract]:
        """
        Return enabled plugins.
        """
        return [plugin for plugin in self.values() if plugin.enabled]

    def disabled_plugins(
        self,
    ) -> list[PluginContract]:
        """
        Return disabled plugins.
        """
        return [plugin for plugin in self.values() if not plugin.enabled]

    def installed_plugins(
        self,
    ) -> list[PluginContract]:
        """
        Return installed plugins.
        """
        return [plugin for plugin in self.values() if plugin.installed]

    def uninstalled_plugins(
        self,
    ) -> list[PluginContract]:
        """
        Return uninstalled plugins.
        """
        return [plugin for plugin in self.values() if not plugin.installed]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_registration(
        self,
        *,
        key: PluginName,
        value: PluginContract,
    ) -> None:
        """
        Validate plugin registration.
        """
        super()._validate_registration(
            key=key,
            value=value,
        )

        if value.name != key:
            raise RegistryError(
                message=("Plugin name does not match registry key."),
                error_code="PLUGIN_NAME_MISMATCH",
            )

        if not value.name.strip():
            raise RegistryError(
                message="Plugin name cannot be empty.",
                error_code="PLUGIN_NAME_REQUIRED",
            )

        if not value.version.strip():
            raise RegistryError(
                message="Plugin version cannot be empty.",
                error_code="PLUGIN_VERSION_REQUIRED",
            )

        if self.exists(key):
            existing = self.require(key)

            if existing.version == value.version:
                raise RegistryError(
                    message=(
                        f"Plugin '{value.name}' "
                        f"version '{value.version}' "
                        "is already registered."
                    ),
                    error_code="PLUGIN_ALREADY_REGISTERED",
                )

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def total_plugins(
        self,
    ) -> int:
        """
        Return the total number of registered plugins.
        """
        return self.size

    @property
    def total_enabled(
        self,
    ) -> int:
        """
        Return the number of enabled plugins.
        """
        return len(
            self.enabled_plugins(),
        )

    @property
    def total_disabled(
        self,
    ) -> int:
        """
        Return the number of disabled plugins.
        """
        return len(
            self.disabled_plugins(),
        )

    @property
    def total_installed(
        self,
    ) -> int:
        """
        Return the number of installed plugins.
        """
        return len(
            self.installed_plugins(),
        )

    @property
    def total_uninstalled(
        self,
    ) -> int:
        """
        Return the number of uninstalled plugins.
        """
        return len(
            self.uninstalled_plugins(),
        )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def enable_plugin(
        self,
        name: PluginName,
    ) -> PluginContract:
        """
        Enable a plugin.
        """
        plugin = self.require_plugin(
            name,
        )

        plugin.enabled = True

        return plugin

    def disable_plugin(
        self,
        name: PluginName,
    ) -> PluginContract:
        """
        Disable a plugin.
        """
        plugin = self.require_plugin(
            name,
        )

        plugin.enabled = False

        return plugin

    def install_plugin(
        self,
        name: PluginName,
    ) -> PluginContract:
        """
        Mark a plugin as installed.
        """
        plugin = self.require_plugin(
            name,
        )

        plugin.installed = True

        return plugin

    def uninstall_plugin(
        self,
        name: PluginName,
    ) -> PluginContract:
        """
        Mark a plugin as uninstalled.
        """
        plugin = self.require_plugin(
            name,
        )

        plugin.installed = False

        return plugin

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def as_dict(
        self,
    ) -> dict[
        PluginName,
        PluginContract,
    ]:
        """
        Export all registered plugins.
        """
        return self.copy()

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """
        return (
            f"{type(self).__name__}("
            f"plugins={self.total_plugins}, "
            f"enabled={self.total_enabled}, "
            f"installed={self.total_installed})"
        )


__all__ = [
    "PluginRegistry",
]
