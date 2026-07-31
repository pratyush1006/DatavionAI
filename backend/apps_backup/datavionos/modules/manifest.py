"""
DatavionOS Module Manifest.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from apps.datavionos.modules.dependency import (
    ModuleDependency,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ModuleManifest:
    """
    Immutable metadata describing a
    DatavionOS module.
    """

    #
    # Identity
    #

    name: str

    version: str

    display_name: str

    description: str = ""

    #
    # Dependencies
    #

    dependencies: tuple[
        ModuleDependency,
        ...,
    ] = ()

    #
    # Services
    #

    exported_services: tuple[
        type,
        ...,
    ] = ()

    #
    # Security
    #

    required_permissions: tuple[
        str,
        ...,
    ] = ()

    feature_flags: tuple[
        str,
        ...,
    ] = ()

    #
    # Startup
    #

    auto_start: bool = True

    startup_priority: int = 100

    #
    # Metadata
    #

    metadata: dict[
        str,
        str,
    ] = field(
        default_factory=dict,
    )

    @property
    def has_dependencies(
        self,
    ) -> bool:
        """
        Whether the module declares
        dependencies.
        """

        return bool(
            self.dependencies,
        )

    @property
    def has_exported_services(
        self,
    ) -> bool:
        """
        Whether the module exports
        services.
        """

        return bool(
            self.exported_services,
        )

    @property
    def has_permissions(
        self,
    ) -> bool:
        """
        Whether the module requires
        permissions.
        """

        return bool(
            self.required_permissions,
        )

    @property
    def has_feature_flags(
        self,
    ) -> bool:
        """
        Whether the module declares
        feature flags.
        """

        return bool(
            self.feature_flags,
        )

    def __repr__(
        self,
    ) -> str:
        return f"ModuleManifest(name={self.name}, version={self.version})"


__all__ = [
    "ModuleManifest",
]
