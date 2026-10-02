"""
Public API for the DatavionOS Kernel.

This package exposes the stable public interface for the DatavionOS
runtime. Consumers should import kernel components from this package
instead of individual implementation modules.
"""

from __future__ import annotations

from apps.datavionos.kernel.application import (
    KernelApplication,
)
from apps.datavionos.kernel.bootstrap import (
    KernelBootstrap,
)
from apps.datavionos.kernel.configuration import (
    KernelConfiguration,
)
from apps.datavionos.kernel.environment import (
    EnvironmentType,
    KernelEnvironment,
)
from apps.datavionos.kernel.exceptions import (
    ApplicationHostError,
    BootstrapError,
    ConfigurationError,
    EnvironmentError,
    HealthCheckError,
    KernelError,
    LifecycleError,
    ModuleInitializationError,
    ModuleRegistrationError,
    RuntimeStateError,
    ShutdownError,
    StartupError,
)
from apps.datavionos.kernel.health import (
    HealthCheck,
    HealthResult,
    HealthStatus,
    KernelHealth,
)
from apps.datavionos.kernel.kernel import (
    Kernel,
)
from apps.datavionos.kernel.lifecycle import (
    KernelLifecycle,
    LifecycleState,
)
from apps.datavionos.kernel.runtime import (
    KernelRuntime,
)

__all__ = [
    # Public API
    "Kernel",
    "KernelApplication",
    "KernelBootstrap",
    "KernelRuntime",
    # Configuration
    "KernelConfiguration",
    "KernelEnvironment",
    "EnvironmentType",
    # Lifecycle
    "KernelLifecycle",
    "LifecycleState",
    # Health
    "KernelHealth",
    "HealthCheck",
    "HealthResult",
    "HealthStatus",
    # Exceptions
    "KernelError",
    "BootstrapError",
    "ConfigurationError",
    "EnvironmentError",
    "LifecycleError",
    "StartupError",
    "ShutdownError",
    "HealthCheckError",
    "ModuleRegistrationError",
    "ModuleInitializationError",
    "RuntimeStateError",
    "ApplicationHostError",
]
