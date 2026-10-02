"""
Module lifecycle contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class ModuleLifecycleState(
    StrEnum,
):
    """
    Runtime lifecycle state of a module.
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
class ModuleLifecycleContext:
    """
    Context supplied to lifecycle operations.
    """

    metadata: dict[str, Any] | None = None


@runtime_checkable
class ModuleLifecycle(
    Protocol,
):
    """
    Module lifecycle contract.
    """

    @property
    def state(
        self,
    ) -> ModuleLifecycleState:
        """
        Current lifecycle state.
        """

    async def install(
        self,
        context: ModuleLifecycleContext,
    ) -> None:
        """
        Install the module.
        """

    async def load(
        self,
        context: ModuleLifecycleContext,
    ) -> None:
        """
        Load the module into the runtime.
        """

    async def enable(
        self,
        context: ModuleLifecycleContext,
    ) -> None:
        """
        Enable the module.
        """

    async def disable(
        self,
        context: ModuleLifecycleContext,
    ) -> None:
        """
        Disable the module.
        """

    async def unload(
        self,
        context: ModuleLifecycleContext,
    ) -> None:
        """
        Unload the module.
        """

    async def uninstall(
        self,
        context: ModuleLifecycleContext,
    ) -> None:
        """
        Uninstall the module.
        """


__all__ = [
    "ModuleLifecycle",
    "ModuleLifecycleContext",
    "ModuleLifecycleState",
]
