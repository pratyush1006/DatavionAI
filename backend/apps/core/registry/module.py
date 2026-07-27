"""
DatavionOS platform module registry.

Defines the contract for dynamically discoverable platform
modules.

Modules represent major capabilities of the DatavionOS
healthcare operating system.

Examples:

- Patient Management
- Appointments
- Laboratory
- Billing
- AI Assistant
- Analytics
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import Registry


@dataclass(
    frozen=True,
    slots=True,
)
class ModuleDefinition:
    """
    Defines a DatavionOS platform module.

    A module represents an independently deployable platform
    capability.

    Attributes:

        name:
            Unique machine-readable module identifier.

        label:
            Human-readable module name.

        description:
            Module description.

        version:
            Semantic module version.

        category:
            Functional grouping.

        dependencies:
            Required modules.

        enabled:
            Whether the module is available globally.

        subscription_required:
            Whether availability depends on organization plan.
    """

    name: str

    label: str

    description: str

    version: str = "1.0.0"

    category: str = "platform"

    dependencies: tuple[str, ...] = ()

    enabled: bool = True

    subscription_required: bool = True


module_registry = Registry[ModuleDefinition]()


__all__: tuple[str, ...] = (
    "ModuleDefinition",
    "module_registry",
)
