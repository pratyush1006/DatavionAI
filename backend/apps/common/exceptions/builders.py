"""
DatavionAI Exception Builders.

Factory functions for constructing enterprise exceptions.

Design Principles
-----------------
- Framework agnostic
- Centralized exception creation
- Consistent error metadata
- Reusable across all modules
"""

from __future__ import annotations

from typing import Any

from .base import (
    AuthenticationException,
    AuthorizationException,
    ConfigurationException,
    DatabaseException,
    IntegrationException,
    ResourceConflictException,
    ResourceNotFoundException,
    ValidationException,
)


def validation_error(
    *,
    message: str | None = None,
    detail: Any = None,
) -> ValidationException:
    """
    Create a validation exception.
    """

    return ValidationException(
        message=message,
        detail=detail,
    )


def resource_not_found(
    *,
    resource: str,
    identifier: str | int | None = None,
) -> ResourceNotFoundException:
    """
    Create a resource not found exception.
    """

    exception = ResourceNotFoundException(
        message=f"{resource} was not found.",
    )

    if hasattr(exception, "set_resource"):
        exception.set_resource(
            resource=resource,
            identifier=identifier,
        )

    return exception


def resource_conflict(
    *,
    resource: str,
    message: str | None = None,
) -> ResourceConflictException:
    """
    Create a resource conflict exception.
    """

    return ResourceConflictException(
        message=message or f"{resource} already exists.",
    )


def authentication_required() -> AuthenticationException:
    """
    Create an authentication exception.
    """

    return AuthenticationException()


def permission_denied(
    *,
    message: str | None = None,
) -> AuthorizationException:
    """
    Create an authorization exception.
    """

    return AuthorizationException(
        message=message,
    )


def database_error(
    *,
    message: str | None = None,
    detail: Any = None,
) -> DatabaseException:
    """
    Create a database exception.
    """

    return DatabaseException(
        message=message,
        detail=detail,
    )


def integration_error(
    *,
    message: str | None = None,
    detail: Any = None,
) -> IntegrationException:
    """
    Create an integration exception.
    """

    return IntegrationException(
        message=message,
        detail=detail,
    )


def configuration_error(
    *,
    message: str | None = None,
) -> ConfigurationException:
    """
    Create a configuration exception.
    """

    return ConfigurationException(
        message=message,
    )


__all__ = (
    "authentication_required",
    "configuration_error",
    "database_error",
    "integration_error",
    "permission_denied",
    "resource_conflict",
    "resource_not_found",
    "validation_error",
)
