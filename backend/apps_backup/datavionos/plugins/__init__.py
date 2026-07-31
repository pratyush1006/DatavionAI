"""
DatavionOS Plugin Contracts.
"""

from .dependency import (
    PluginDependency,
    PluginDependencyTarget,
    PluginDependencyType,
)
from .descriptor import (
    PluginCategory,
    PluginDescriptor,
    PluginStatus,
)
from .lifecycle import (
    PluginLifecycle,
    PluginLifecycleContext,
    PluginLifecycleState,
)
from .loader import (
    PluginLoadContext,
    PluginLoader,
    RuntimePlugin,
)
from .registry import (
    PluginRegistry,
)
from .services import (
    PluginServices,
)

__all__ = [
    # Descriptor
    "PluginCategory",
    "PluginDescriptor",
    "PluginStatus",
    # Dependencies
    "PluginDependency",
    "PluginDependencyTarget",
    "PluginDependencyType",
    # Lifecycle
    "PluginLifecycle",
    "PluginLifecycleContext",
    "PluginLifecycleState",
    # Loader
    "PluginLoadContext",
    "PluginLoader",
    "RuntimePlugin",
    # Registry
    "PluginRegistry",
    # Services
    "PluginServices",
]
