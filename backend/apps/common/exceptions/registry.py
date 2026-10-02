"""
DatavionAI Exception Registry.

Centralized registry mapping error codes to exception classes.

Design Principles
-----------------
- Framework agnostic
- Immutable default registry
- Extensible
- Type-safe
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

from .base import (
    AuditException,
    AuthenticationException,
    AuthorizationException,
    CacheException,
    ConfigurationException,
    DatabaseException,
    DatavionException,
    IntegrationException,
    ResourceConflictException,
    ResourceNotFoundException,
    ServerException,
    ValidationException,
    WorkflowException,
)
from .codes import ErrorCode

###############################################################################
# Exception Registry
###############################################################################

_EXCEPTION_REGISTRY: dict[
    ErrorCode,
    type[DatavionException],
] = {
    ErrorCode.INTERNAL_SERVER_ERROR: ServerException,
    ErrorCode.VALIDATION_ERROR: ValidationException,
    ErrorCode.UNAUTHENTICATED: AuthenticationException,
    ErrorCode.PERMISSION_DENIED: AuthorizationException,
    ErrorCode.RESOURCE_NOT_FOUND: ResourceNotFoundException,
    ErrorCode.RESOURCE_CONFLICT: ResourceConflictException,
    ErrorCode.DATABASE_ERROR: DatabaseException,
    ErrorCode.CACHE_ERROR: CacheException,
    ErrorCode.CONFIGURATION_ERROR: ConfigurationException,
    ErrorCode.INTEGRATION_ERROR: IntegrationException,
    ErrorCode.WORKFLOW_ERROR: WorkflowException,
    ErrorCode.AUDIT_ERROR: AuditException,
}

EXCEPTION_REGISTRY: Final[
    MappingProxyType[
        ErrorCode,
        type[DatavionException],
    ]
] = MappingProxyType(_EXCEPTION_REGISTRY)

###############################################################################
# Registry Functions
###############################################################################


def get_exception_class(
    code: ErrorCode,
) -> type[DatavionException]:
    """
    Return the registered exception class for an error code.
    """

    return EXCEPTION_REGISTRY.get(
        code,
        ServerException,
    )


def is_registered(
    code: ErrorCode,
) -> bool:
    """
    Return True if an error code has a registered exception.
    """

    return code in EXCEPTION_REGISTRY


def register_exception(
    code: ErrorCode,
    exception_class: type[DatavionException],
) -> None:
    """
    Register or replace an exception class.

    Intended for application startup or extension modules.
    """

    _EXCEPTION_REGISTRY[code] = exception_class


###############################################################################
# Public Exports
###############################################################################

__all__ = (
    "EXCEPTION_REGISTRY",
    "get_exception_class",
    "is_registered",
    "register_exception",
)
