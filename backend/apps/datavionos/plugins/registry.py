"""
Plugin registry contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.plugins.descriptor import (
    PluginCategory,
    PluginDescriptor,
)


@runtime_checkable
class PluginRegistry(
    Protocol,
):
    """
    Registry of available plugins.
    """

    async def register(
        self,
        descriptor: PluginDescriptor,
    ) -> None:
        """
        Register a plugin descriptor.
        """

    async def unregister(
        self,
        plugin_id: str,
    ) -> None:
        """
        Remove a plugin from the registry.
        """

    async def get(
        self,
        plugin_id: str,
    ) -> PluginDescriptor | None:
        """
        Return a plugin descriptor by ID.
        """

    async def contains(
        self,
        plugin_id: str,
    ) -> bool:
        """
        Determine whether a plugin
        is registered.
        """

    async def list(
        self,
    ) -> tuple[PluginDescriptor, ...]:
        """
        Return all registered plugins.
        """

    async def list_by_category(
        self,
        category: PluginCategory,
    ) -> tuple[PluginDescriptor, ...]:
        """
        Return plugins belonging to
        the specified category.
        """

    async def list_by_module(
        self,
        module_id: str,
    ) -> tuple[PluginDescriptor, ...]:
        """
        Return plugins targeting
        the specified module.
        """


__all__ = [
    "PluginRegistry",
]
