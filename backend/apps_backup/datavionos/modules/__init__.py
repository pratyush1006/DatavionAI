"""
DatavionOS Module Contracts.
"""

from .dependency import (
    ModuleDependency,
    ModuleDependencyType,
)
from .descriptor import (
    ModuleCategory,
    ModuleDescriptor,
    ModuleStatus,
)
from .lifecycle import (
    ModuleLifecycle,
    ModuleLifecycleContext,
    ModuleLifecycleState,
)
from .loader import (
    ModuleLoadContext,
    ModuleLoader,
    RuntimeModule,
)
from .metadata import (
    ModuleMetadata,
)
from .registry import (
    ModuleRegistry,
)
from .services import (
    ModuleServices,
)

__all__ = [
    # Descriptor
    "ModuleCategory",
    "ModuleDescriptor",
    "ModuleStatus",
    # Metadata
    "ModuleMetadata",
    # Dependencies
    "ModuleDependency",
    "ModuleDependencyType",
    # Lifecycle
    "ModuleLifecycle",
    "ModuleLifecycleContext",
    "ModuleLifecycleState",
    # Loader
    "ModuleLoadContext",
    "ModuleLoader",
    "RuntimeModule",
    # Registry
    "ModuleRegistry",
    # Services
    "ModuleServices",
]
