"""
Tenant aware module resolver.
"""

from __future__ import annotations

from apps.datavionos.registries.module import (
    module_registry,
)


class ModuleResolver:
    """
    Resolve modules available for a tenant.
    """

    def resolve(
        self,
        *,
        tenant,
    ):

        if tenant is None:
            return []

        tenant_type = tenant.tenant_type

        modules = module_registry.enabled_modules()

        resolved = []

        for module in modules:
            if not module.tenant_scoped:
                resolved.append(
                    module,
                )
                continue

            allowed_types = module.metadata.get(
                "tenant_types",
                [],
            )

            if tenant_type in allowed_types:
                resolved.append(
                    module,
                )

        return resolved


module_resolver = ModuleResolver()


__all__ = (
    "ModuleResolver",
    "module_resolver",
)
