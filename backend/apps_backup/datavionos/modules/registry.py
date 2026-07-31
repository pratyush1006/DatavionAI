"""
Module registry contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.modules.descriptor import (
    ModuleDescriptor,
)


@runtime_checkable
class ModuleRegistry(
    Protocol,
):
    """
    Registry of available modules.
    """

    async def register(
        self,
        descriptor: ModuleDescriptor,
    ) -> None:
        """
        Register a module descriptor.
        """

    async def unregister(
        self,
        module_id: str,
    ) -> None:
        """
        Remove a module from the registry.
        """

    async def get(
        self,
        module_id: str,
    ) -> ModuleDescriptor | None:
        """
        Return a module descriptor by ID.
        """

    async def contains(
        self,
        module_id: str,
    ) -> bool:
        """
        Determine whether a module
        is registered.
        """

    async def list(
        self,
    ) -> tuple[ModuleDescriptor, ...]:
        """
        Return all registered modules.
        """

    async def list_by_category(
        self,
        category: str,
    ) -> tuple[ModuleDescriptor, ...]:
        """
        Return modules belonging to
        a category.
        """


__all__ = [
    "ModuleRegistry",
]
