"""
Module registry for DatavionOS.

This module provides the registry responsible for managing
platform module contracts.

The registry is a global kernel component.

Responsibilities:

- Register modules
- Validate module contracts
- Lookup modules
- Provide module metadata
- Provide enabled/system/tenant module collections

Tenant subscription filtering is handled separately
by module availability selectors.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.datavionos.exceptions import RegistryError
from apps.datavionos.types import Identifier

from ..contracts.module import ModuleContract
from .registry import Registry

PlatformModule = ModuleContract


class ModuleRegistry(
    Registry[
        Identifier,
        ModuleContract,
    ],
):
    """
    Global DatavionOS module registry.
    """

    def __init__(
        self,
    ) -> None:

        super().__init__(
            name="modules",
        )

    #
    # Registration
    #

    def register_module(
        self,
        module: ModuleContract,
    ) -> ModuleContract:
        """
        Register a platform module.
        """

        return self.register(
            key=module.identifier,
            value=module,
        )

    def register_modules(
        self,
        modules: Iterable[ModuleContract],
    ) -> None:
        """
        Register multiple modules.
        """

        for module in modules:
            self.register_module(
                module,
            )

    #
    # Lookup
    #

    def get_module(
        self,
        identifier: Identifier,
    ) -> ModuleContract | None:
        """
        Retrieve module.
        """

        return self.get(
            identifier,
        )

    def require_module(
        self,
        identifier: Identifier,
    ) -> ModuleContract:

        return self.require(
            identifier,
        )

    def unregister_module(
        self,
        identifier: Identifier,
    ) -> ModuleContract:

        return self.unregister(
            identifier,
        )

    #
    # Query
    #

    def enabled_modules(
        self,
    ) -> list[ModuleContract]:
        """
        Return globally enabled modules.
        """

        return [module for module in self.values() if module.enabled]

    def disabled_modules(
        self,
    ) -> list[ModuleContract]:

        return [module for module in self.values() if not module.enabled]

    def system_modules(
        self,
    ) -> list[ModuleContract]:

        return [module for module in self.values() if module.system]

    def tenant_modules(
        self,
    ) -> list[ModuleContract]:

        return [module for module in self.values() if not module.system]

    def get_by_category(
        self,
        category: str,
    ) -> list[ModuleContract]:
        """
        Return modules by category.
        """

        return [
            module
            for module in self.values()
            if str(
                module.category,
            )
            == category
        ]

    def identifiers(
        self,
    ) -> tuple[Identifier, ...]:
        """
        Return all module identifiers.
        """

        return tuple(
            self.keys(),
        )

    def enabled_identifiers(
        self,
    ) -> tuple[Identifier, ...]:
        """
        Return enabled module identifiers.
        """

        return tuple(module.identifier for module in self.enabled_modules())

    #
    # Validation
    #

    def _validate_registration(
        self,
        *,
        key: Identifier,
        value: ModuleContract,
    ) -> None:
        """
        Validate module registration.
        """

        super()._validate_registration(
            key=key,
            value=value,
        )

        if value.identifier != key:
            raise RegistryError(
                message=("Module identifier does not match registry key."),
                error_code=("MODULE_IDENTIFIER_MISMATCH"),
            )

        if not value.name.strip():
            raise RegistryError(
                message=("Module name cannot be empty."),
                error_code=("MODULE_NAME_REQUIRED"),
            )

        if not value.version.strip():
            raise RegistryError(
                message=("Module version cannot be empty."),
                error_code=("MODULE_VERSION_REQUIRED"),
            )

        if self.exists(key):
            existing = self.require(
                key,
            )

            if existing.version == value.version:
                raise RegistryError(
                    message=(
                        f"Module '{value.name}' "
                        f"version '{value.version}' "
                        "is already registered."
                    ),
                    error_code=("MODULE_ALREADY_REGISTERED"),
                )

    #
    # Statistics
    #

    @property
    def total_modules(
        self,
    ) -> int:

        return self.size

    @property
    def total_enabled(
        self,
    ) -> int:

        return len(
            self.enabled_modules(),
        )

    @property
    def total_disabled(
        self,
    ) -> int:

        return len(
            self.disabled_modules(),
        )

    @property
    def total_system(
        self,
    ) -> int:

        return len(
            self.system_modules(),
        )

    @property
    def total_tenant(
        self,
    ) -> int:

        return len(
            self.tenant_modules(),
        )

    #
    # Maintenance
    #

    def enable_module(
        self,
        identifier: Identifier,
    ) -> ModuleContract:
        """
        Enable module globally.
        """

        module = self.require_module(
            identifier,
        )

        module.enabled = True

        return module

    def disable_module(
        self,
        identifier: Identifier,
    ) -> ModuleContract:
        """
        Disable module globally.
        """

        module = self.require_module(
            identifier,
        )

        module.enabled = False

        return module

    #
    # Export
    #

    def as_dict(
        self,
    ) -> dict[Identifier, ModuleContract]:

        return self.copy()

    #
    # Dunder
    #

    def __repr__(
        self,
    ) -> str:

        return (
            f"{type(self).__name__}("
            f"modules={self.total_modules}, "
            f"enabled={self.total_enabled}"
            ")"
        )


module_registry = ModuleRegistry()


__all__ = [
    "ModuleRegistry",
    "PlatformModule",
    "module_registry",
]
