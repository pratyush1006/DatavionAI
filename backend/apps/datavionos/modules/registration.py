"""
DatavionOS module contract registration.

Central registration point for all DatavionOS
platform modules.

Modules are registered into the global kernel
module registry during application startup.
"""

from __future__ import annotations

from apps.datavionos.registries.module import (
    module_registry,
)

from .ai_assistant_module import (
    ai_assistant_module,
)
from .ai_workflow_module import (
    ai_workflow_module,
)
from .appointment_management_module import (
    appointment_management_module,
)


def register_datavionos_modules() -> None:
    """
    Register all DatavionOS module contracts.

    Registration is idempotent.
    Duplicate modules are ignored.
    """

    registered_ids = {module.identifier for module in module_registry.all()}

    module_factories = (
        ai_assistant_module,
        ai_workflow_module,
        appointment_management_module,
    )

    modules = []

    for factory in module_factories:
        module = factory()

        if module.identifier in registered_ids:
            continue

        modules.append(
            module,
        )

    if modules:
        module_registry.register_modules(
            modules,
        )


__all__ = [
    "register_datavionos_modules",
]
