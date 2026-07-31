"""
Public exception hierarchy for the DatavionOS kernel.

The DatavionOS exception package defines the canonical exception types used
throughout the kernel. All kernel-specific exceptions should inherit from
``DatavionOSError`` to provide consistent error handling, logging, and API
serialization.

Consumers should import exceptions from this package rather than individual
implementation modules to maintain a stable public API.
"""

from __future__ import annotations

from apps.datavionos.exceptions.base import (
    CapabilityError,
    CompositionError,
    ConfigurationError,
    ContractError,
    DatavionOSError,
    DatavionOSRuntimeError,
    EventError,
    KernelError,
    PluginError,
    RegistryError,
    ValidationError,
    WorkflowError,
)
from apps.datavionos.kernel.exceptions import (
    RuntimeError,
)

__all__ = [
    "CapabilityError",
    "CompositionError",
    "ConfigurationError",
    "ContractError",
    "DatavionOSError",
    "DatavionOSRuntimeError",
    "EventError",
    "KernelError",
    "PluginError",
    "RegistryError",
    "DatavionOSRuntimeError",
    "ValidationError",
    "WorkflowError",
    "RuntimeError",
]
