"""
DatavionOS Module Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from apps.datavionos.modules.context import (
    ModuleContext,
)
from apps.datavionos.modules.manifest import (
    ModuleManifest,
)


class Module(
    ABC,
):
    """
    Base class for every DatavionOS module.

    All platform modules (Patients,
    Organizations, Billing, Laboratory,
    Pharmacy, etc.) inherit from this
    class.
    """

    @property
    @abstractmethod
    def manifest(
        self,
    ) -> ModuleManifest:
        """
        Return the immutable module
        manifest.
        """

    @abstractmethod
    async def initialize(
        self,
        context: ModuleContext,
    ) -> None:
        """
        Initialize the module.
        """

    @abstractmethod
    async def start(
        self,
    ) -> None:
        """
        Start the module.
        """

    @abstractmethod
    async def stop(
        self,
    ) -> None:
        """
        Stop the module.
        """

    @abstractmethod
    async def dispose(
        self,
    ) -> None:
        """
        Dispose the module and release
        resources.
        """

    @property
    def name(
        self,
    ) -> str:
        """
        Module name.
        """

        return self.manifest.name

    @property
    def version(
        self,
    ) -> str:
        """
        Module version.
        """

        return self.manifest.version

    @property
    def display_name(
        self,
    ) -> str:
        """
        Human-readable module name.
        """

        return self.manifest.display_name

    def __repr__(
        self,
    ) -> str:
        return f"{self.__class__.__name__}(name={self.name}, version={self.version})"


__all__ = [
    "Module",
]
