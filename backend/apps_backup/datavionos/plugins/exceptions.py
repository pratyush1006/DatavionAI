"""
Plugin exceptions.
"""

from __future__ import annotations


class PluginError(Exception):
    """Base plugin error."""


class PluginNotFoundError(PluginError):
    """Plugin not found."""


class PluginAlreadyRegisteredError(PluginError):
    """Plugin already registered."""


class PluginDependencyError(PluginError):
    """Plugin dependency resolution failed."""


class PluginLoadError(PluginError):
    """Plugin failed to load."""


class PluginLifecycleError(PluginError):
    """Invalid plugin lifecycle transition."""


class PluginRegistrationError(PluginError):
    """Plugin registration failed."""


class PluginCompatibilityError(PluginError):
    """Plugin is not compatible with the current platform."""


__all__ = [
    "PluginError",
    "PluginNotFoundError",
    "PluginAlreadyRegisteredError",
    "PluginDependencyError",
    "PluginLoadError",
    "PluginLifecycleError",
    "PluginRegistrationError",
    "PluginCompatibilityError",
]
