"""
Module loader contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.datavionos.modules.descriptor import (
    ModuleDescriptor,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ModuleLoadContext:
    """
    Context supplied during module loading.
    """

    metadata: dict[str, Any] | None = None


@runtime_checkable
class RuntimeModule(
    Protocol,
):
    """
    A live module instance managed by the kernel.
    """

    @property
    def descriptor(
        self,
    ) -> ModuleDescriptor:
        """
        Return the module descriptor.
        """


@runtime_checkable
class ModuleLoader(
    Protocol,
):
    """
    Module loading contract.
    """

    async def load(
        self,
        descriptor: ModuleDescriptor,
        context: ModuleLoadContext,
    ) -> RuntimeModule:
        """
        Load a module into the runtime.
        """

    async def unload(
        self,
        module: RuntimeModule,
    ) -> None:
        """
        Unload a runtime module.
        """

    async def reload(
        self,
        module: RuntimeModule,
        context: ModuleLoadContext,
    ) -> RuntimeModule:
        """
        Reload a runtime module.
        """

    async def is_loaded(
        self,
        module_id: str,
    ) -> bool:
        """
        Determine whether a module is currently loaded.
        """


__all__ = [
    "ModuleLoadContext",
    "ModuleLoader",
    "RuntimeModule",
]
