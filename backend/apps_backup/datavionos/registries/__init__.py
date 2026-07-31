"""
DatavionOS registry package.

This package provides the registry infrastructure used by the
DatavionOS kernel.

Exports:
    BaseRegistry
    Registry
    ModuleRegistry
    CapabilityRegistry
    ServiceRegistry
    PluginRegistry
    RegistryBootstrap
"""

from .base import BaseRegistry
from .bootstrap import RegistryBootstrap
from .capability import CapabilityRegistry
from .module import ModuleRegistry
from .plugin import PluginRegistry
from .registry import Registry
from .service import ServiceRegistry

__all__ = [
    "BaseRegistry",
    "Registry",
    "ModuleRegistry",
    "module_registry",
    "CapabilityRegistry",
    "ServiceRegistry",
    "PluginRegistry",
    "RegistryBootstrap",
]
