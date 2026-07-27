"""
DatavionOS Module System Exceptions.
"""

from __future__ import annotations


class ModuleError(Exception):
    """
    Base exception for the
    DatavionOS module system.
    """


class ModuleDiscoveryError(
    ModuleError,
):
    """
    Raised when module discovery fails.
    """


class ModuleRegistrationError(
    ModuleError,
):
    """
    Raised when module registration
    fails.
    """


class ModuleLoadError(
    ModuleError,
):
    """
    Raised when a module cannot
    be loaded.
    """


class ModuleDependencyError(
    ModuleError,
):
    """
    Raised when module dependencies
    are invalid.
    """


class CircularModuleDependencyError(
    ModuleDependencyError,
):
    """
    Raised when circular module
    dependencies are detected.
    """


class ModuleInitializationError(
    ModuleError,
):
    """
    Raised when a module fails to
    initialize.
    """


class ModuleLifecycleError(
    ModuleError,
):
    """
    Raised during module lifecycle
    operations.
    """


class ModuleContextError(
    ModuleError,
):
    """
    Raised when a module context
    is invalid.
    """


__all__ = [
    "ModuleError",
    "ModuleDiscoveryError",
    "ModuleRegistrationError",
    "ModuleLoadError",
    "ModuleDependencyError",
    "CircularModuleDependencyError",
    "ModuleInitializationError",
    "ModuleLifecycleError",
    "ModuleContextError",
]
