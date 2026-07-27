"""
DatavionOS Kernel Exceptions.
"""

from __future__ import annotations


class KernelError(Exception):
    """
    Base exception for the DatavionOS
    Kernel subsystem.
    """


class BootstrapError(
    KernelError,
):
    """
    Raised when kernel bootstrap fails.
    """


class RuntimeError(
    KernelError,
):
    """
    Raised when the runtime encounters
    an unrecoverable error.
    """


class ConfigurationError(
    KernelError,
):
    """
    Raised when runtime configuration
    is invalid.
    """


class EnvironmentError(
    KernelError,
):
    """
    Raised when the runtime environment
    cannot be initialized.
    """


class LifecycleError(
    KernelError,
):
    """
    Raised when lifecycle execution
    fails.
    """


class StartupError(
    LifecycleError,
):
    """
    Raised when startup fails.
    """


class ShutdownError(
    LifecycleError,
):
    """
    Raised when shutdown fails.
    """


class HealthCheckError(
    KernelError,
):
    """
    Raised when health monitoring
    fails.
    """


class ModuleRegistrationError(
    KernelError,
):
    """
    Raised when a runtime module
    cannot be registered.
    """


class ModuleInitializationError(
    KernelError,
):
    """
    Raised when a runtime module
    cannot be initialized.
    """


class RuntimeStateError(
    KernelError,
):
    """
    Raised when an operation is
    invalid for the current runtime
    state.
    """


class ApplicationHostError(
    KernelError,
):
    """
    Raised when the application host
    encounters an error.
    """


__all__ = [
    "KernelError",
    "BootstrapError",
    "RuntimeError",
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
