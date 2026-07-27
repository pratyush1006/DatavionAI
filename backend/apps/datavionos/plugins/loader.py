"""
Plugin loader contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.datavionos.plugins.descriptor import (
    PluginDescriptor,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PluginLoadContext:
    """
    Context supplied during plugin loading.
    """

    metadata: dict[str, Any] | None = None


@runtime_checkable
class RuntimePlugin(
    Protocol,
):
    """
    A live plugin instance managed by the kernel.
    """

    @property
    def descriptor(
        self,
    ) -> PluginDescriptor:
        """
        Return the plugin descriptor.
        """


@runtime_checkable
class PluginLoader(
    Protocol,
):
    """
    Plugin loading contract.
    """

    async def load(
        self,
        descriptor: PluginDescriptor,
        context: PluginLoadContext,
    ) -> RuntimePlugin:
        """
        Load a plugin into the runtime.
        """

    async def unload(
        self,
        plugin: RuntimePlugin,
    ) -> None:
        """
        Unload a runtime plugin.
        """

    async def reload(
        self,
        plugin: RuntimePlugin,
        context: PluginLoadContext,
    ) -> RuntimePlugin:
        """
        Reload a runtime plugin.
        """

    async def is_loaded(
        self,
        plugin_id: str,
    ) -> bool:
        """
        Determine whether a plugin
        is currently loaded.
        """


__all__ = [
    "PluginLoadContext",
    "PluginLoader",
    "RuntimePlugin",
]
