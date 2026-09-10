"""
DatavionOS module registry.

Concrete registry for DatavionOS ModuleContract instances.

Architecture:

    ModuleContract
          |
          v
    ModuleRegistry
          |
          +--> Module Registration
          |
          +--> Runtime Discovery
          |
          +--> Module Availability Selector
          |
          +--> Bootstrap

The registry is responsible only for maintaining the canonical collection
of module contracts known to the DatavionOS runtime.

The registry does NOT decide:

- SaaS subscription entitlement
- tenant-type eligibility
- RBAC authorization
- feature-flag authorization
- navigation visibility
- dashboard visibility

Those concerns belong to their respective services/selectors/builders.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.datavionos.contracts.module import (
    ModuleContract,
)

from .registry import (
    Registry,
)


class ModuleRegistry(
    Registry[str, ModuleContract],
):
    """
    Concrete registry of DatavionOS module contracts.

    Modules are keyed by their canonical ``identifier``.

    Example:

        module_registry.register(
            module,
        )

    The generic Registry provides:

    - duplicate protection
    - thread safety
    - lookup
    - removal
    - snapshots
    - collection operations
    """

    def __init__(
        self,
        *,
        name: str = "datavionos.modules",
    ) -> None:
        """
        Initialize the module registry.
        """

        super().__init__(
            name=name,
        )

    # ==================================================================
    # Registration
    # ==================================================================

    def register(
        self,
        module: ModuleContract,
    ) -> ModuleContract:
        """
        Register a module contract.

        The module identifier is the canonical registry key.

        Duplicate identifiers are rejected by BaseRegistry.
        """

        if not isinstance(
            module,
            ModuleContract,
        ):
            raise TypeError(
                "module must be an instance of ModuleContract.",
            )

        return super().register(
            key=module.identifier,
            value=module,
        )

    def register_modules(
        self,
        modules: Iterable[ModuleContract],
    ) -> None:
        """
        Register multiple module contracts.

        Each module is registered through the canonical ``register()``
        path so duplicate detection and validation remain centralized.
        """

        for module in modules:
            self.register(
                module,
            )

    # ==================================================================
    # Module Lookup
    # ==================================================================

    def get_module(
        self,
        identifier: str,
    ) -> ModuleContract | None:
        """
        Return a module by identifier.
        """

        return self.get(
            identifier,
        )

    def require_module(
        self,
        identifier: str,
    ) -> ModuleContract:
        """
        Return a required module.

        Raises RegistryError when the module is not registered.
        """

        return self.require(
            identifier,
        )

    def has_module(
        self,
        identifier: str,
    ) -> bool:
        """
        Determine whether a module is registered.
        """

        return self.exists(
            identifier,
        )

    # ==================================================================
    # Runtime Discovery
    # ==================================================================

    def enabled_modules(
        self,
    ) -> tuple[ModuleContract, ...]:
        """
        Return modules explicitly enabled by the module definition.

        This is NOT tenant entitlement.

        It only evaluates the module's canonical ``enabled`` property.
        """

        return tuple(
            module
            for module in self.values()
            if module.enabled
        )

    def available_modules(
        self,
    ) -> tuple[ModuleContract, ...]:
        """
        Return modules available at the platform-runtime level.

        ModuleContract already owns the canonical availability rule:

            enabled and active

        Therefore the registry delegates to ``module.is_available`` instead
        of duplicating lifecycle logic.
        """

        return tuple(
            module
            for module in self.values()
            if module.is_available
        )

    def active_modules(
        self,
    ) -> tuple[ModuleContract, ...]:
        """
        Return modules whose lifecycle status is ACTIVE.
        """

        return tuple(
            module
            for module in self.values()
            if module.is_active
        )

    def disabled_modules(
        self,
    ) -> tuple[ModuleContract, ...]:
        """
        Return modules that are not enabled.
        """

        return tuple(
            module
            for module in self.values()
            if not module.enabled
        )

    # ==================================================================
    # Categorization
    # ==================================================================

    def modules_by_category(
        self,
        category: str,
    ) -> tuple[ModuleContract, ...]:
        """
        Return modules belonging to a category.

        Supports both string and enum-backed category values.
        """

        normalized_category = str(
            getattr(
                category,
                "value",
                category,
            ),
        ).lower()

        return tuple(
            module
            for module in self.values()
            if str(
                getattr(
                    module.category,
                    "value",
                    module.category,
                ),
            ).lower()
            == normalized_category
        )

    # ==================================================================
    # UI Capability Discovery
    # ==================================================================

    def navigable_modules(
        self,
    ) -> tuple[ModuleContract, ...]:
        """
        Return available modules that declare navigation metadata.

        This does not perform RBAC or entitlement checks.
        """

        return tuple(
            module
            for module in self.available_modules()
            if module.has_navigation
        )

    def dependency_order(
        self,
        modules: Iterable[ModuleContract] | None = None,
    ) -> tuple[ModuleContract, ...]:
        """Return modules in deterministic dependency-first order."""

        selected = tuple(modules if modules is not None else self.values())
        by_id = {module.identifier: module for module in selected}
        missing = sorted(
            dependency
            for module in selected
            for dependency in module.dependencies
            if dependency not in by_id
        )
        if missing:
            raise ValueError(
                "Missing DatavionOS module dependencies: "
                + ", ".join(sorted(set(missing)))
            )

        temporary: set[str] = set()
        permanent: set[str] = set()
        ordered: list[ModuleContract] = []

        def visit(identifier: str) -> None:
            if identifier in permanent:
                return
            if identifier in temporary:
                raise ValueError(
                    f"Circular DatavionOS module dependency detected at: {identifier}"
                )
            temporary.add(identifier)
            for dependency in sorted(by_id[identifier].dependencies):
                visit(dependency)
            temporary.remove(identifier)
            permanent.add(identifier)
            ordered.append(by_id[identifier])

        for identifier in sorted(by_id):
            visit(identifier)
        return tuple(ordered)

    def dashboard_modules(
        self,
    ) -> tuple[ModuleContract, ...]:
        """
        Return available modules that declare an enabled dashboard.

        This does not perform RBAC or entitlement checks.
        """

        return tuple(
            module
            for module in self.available_modules()
            if module.has_dashboard
        )


module_registry = ModuleRegistry()


__all__ = (
    "ModuleRegistry",
    "module_registry",
)
