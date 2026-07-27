"""
Plugin lifecycle contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class PluginLifecycleState(
    StrEnum,
):
    """
    Runtime lifecycle state of a plugin.
    """

    DISCOVERED = "discovered"

    INSTALLED = "installed"

    LOADED = "loaded"

    ENABLED = "enabled"

    DISABLED = "disabled"

    UNLOADED = "unloaded"

    UNINSTALLED = "uninstalled"

    FAILED = "failed"


@dataclass(
    frozen=True,
    slots=True,
)
class PluginLifecycleContext:
    """
    Context supplied to lifecycle operations.
    """

    metadata: dict[str, Any] | None = None


@runtime_checkable
class PluginLifecycle(
    Protocol,
):
    """
    Plugin lifecycle contract.
    """

    @property
    def state(
        self,
    ) -> PluginLifecycleState:
        """
        Current lifecycle state.
        """

    async def install(
        self,
        context: PluginLifecycleContext,
    ) -> None:
        """
        Install the plugin.
        """

    async def load(
        self,
        context: PluginLifecycleContext,
    ) -> None:
        """
        Load the plugin into the runtime.
        """

    async def enable(
        self,
        context: PluginLifecycleContext,
    ) -> None:
        """
        Enable the plugin.
        """

    async def disable(
        self,
        context: PluginLifecycleContext,
    ) -> None:
        """
        Disable the plugin.
        """

    async def unload(
        self,
        context: PluginLifecycleContext,
    ) -> None:
        """
        Unload the plugin.
        """

    async def uninstall(
        self,
        context: PluginLifecycleContext,
    ) -> None:
        """
        Uninstall the plugin.
        """


__all__ = [
    "PluginLifecycle",
    "PluginLifecycleContext",
    "PluginLifecycleState",
]
