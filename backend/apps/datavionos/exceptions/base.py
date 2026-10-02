"""
Exception hierarchy for the DatavionOS kernel.

Every exception raised by the DatavionOS kernel should inherit from
``DatavionOSError``. This provides a consistent, structured, and extensible
error model across the platform.

The hierarchy is intentionally framework-agnostic and does not depend on
Django or DRF, allowing it to be safely reused by runtime components,
management commands, background workers, and integrations.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

from apps.datavionos.types import Metadata

DEFAULT_ERROR_CODE: str = "DATAVIONOS_ERROR"


@dataclass(
    frozen=True,
    kw_only=True,
    slots=True,
)
class DatavionOSError(Exception):
    """
    Base exception for the DatavionOS kernel.

    Attributes:
        message:
            Human-readable error description.

        error_code:
            Stable machine-readable error identifier.

        context:
            Optional structured diagnostic information.
    """

    message: str

    error_code: str = DEFAULT_ERROR_CODE

    context: Metadata = field(
        default_factory=dict,
    )

    def __str__(self) -> str:
        """
        Return the formatted exception message.
        """
        return f"[{self.error_code}] {self.message}"

    def __repr__(self) -> str:
        """
        Return the developer-friendly representation.
        """
        return (
            f"{type(self).__name__}("
            f"error_code={self.error_code!r}, "
            f"message={self.message!r})"
        )

    def to_dict(self) -> Metadata:
        """
        Serialize the exception.

        Returns:
            Serializable representation suitable for APIs,
            structured logging, telemetry, and debugging.
        """
        return {
            "type": type(self).__name__,
            "error": self.error_code,
            "message": self.message,
            "context": dict(self.context),
        }


# ============================================================================
# Generic Exceptions
# ============================================================================


class ConfigurationError(DatavionOSError):
    """Raised when kernel configuration is invalid."""


class ValidationError(DatavionOSError):
    """Raised when validation fails."""


class ContractError(DatavionOSError):
    """Raised when a contract is invalid or incompatible."""


class DatavionOSRuntimeError(DatavionOSError):
    """
    Base runtime exception for the DatavionOS platform.

    This class intentionally avoids shadowing Python's built-in
    ``RuntimeError``.
    """


# ============================================================================
# Runtime Exceptions
# ============================================================================


class KernelError(DatavionOSRuntimeError):
    """Raised for kernel lifecycle failures."""


class RegistryError(DatavionOSRuntimeError):
    """Raised for registry failures."""


class PluginError(DatavionOSRuntimeError):
    """Raised for plugin loading or execution failures."""


class CapabilityError(DatavionOSRuntimeError):
    """Raised when capability resolution fails."""


class CompositionError(DatavionOSRuntimeError):
    """Raised during platform composition failures."""


class WorkflowError(DatavionOSRuntimeError):
    """Raised when workflow execution fails."""


class EventError(DatavionOSRuntimeError):
    """Raised when event processing fails."""


__all__ = [
    "DEFAULT_ERROR_CODE",
    "DatavionOSError",
    "ConfigurationError",
    "ValidationError",
    "ContractError",
    "DatavionOSRuntimeError",
    "KernelError",
    "RegistryError",
    "PluginError",
    "CapabilityError",
    "CompositionError",
    "WorkflowError",
    "EventError",
]
