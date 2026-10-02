"""
DatavionAI Base Exceptions.

Enterprise exception hierarchy for the DatavionAI platform.

Design Principles
-----------------
- Framework agnostic
- Immutable error codes
- HTTP status aware
- Serializable
- Overrideable messages
"""

from __future__ import annotations

from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any

from .codes import ErrorCode
from .messages import get_error_message


@dataclass(
    kw_only=True,
)
class DatavionException(Exception):
    """
    Base exception for the DatavionAI platform.
    """

    code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR

    message: str | None = None

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR

    detail: Any = None

    extra: dict[str, Any] = field(
        default_factory=dict,
    )

    def __post_init__(self) -> None:
        """
        Initialize exception message.
        """

        if self.message is None:
            self.message = get_error_message(
                self.code,
            )

        Exception.__init__(
            self,
            self.message,
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize exception.
        """

        payload: dict[str, Any] = {
            "code": self.code.value,
            "message": self.message,
        }

        if self.detail is not None:
            payload["detail"] = self.detail

        if self.extra:
            payload["extra"] = self.extra

        return payload


###############################################################################
# Client Errors
###############################################################################


@dataclass(kw_only=True)
class ClientException(DatavionException):
    """
    Base client exception.
    """

    status_code: int = HTTPStatus.BAD_REQUEST


@dataclass(kw_only=True, init=False)
class ValidationException(ClientException):
    code: ErrorCode = ErrorCode.VALIDATION_ERROR

    status_code: int = HTTPStatus.BAD_REQUEST

    def __init__(
        self,
        message: str | None = None,
        *,
        code: ErrorCode = ErrorCode.VALIDATION_ERROR,
        status_code: int = HTTPStatus.BAD_REQUEST,
        detail: Any = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        """Accept a positional message as well as the shared keyword contract."""
        super().__init__(
            code=code,
            message=message,
            status_code=status_code,
            detail=detail,
            extra=extra or {},
        )


@dataclass(kw_only=True)
class AuthenticationException(ClientException):
    code: ErrorCode = ErrorCode.UNAUTHENTICATED

    status_code: int = HTTPStatus.UNAUTHORIZED


@dataclass(kw_only=True)
class AuthorizationException(ClientException):
    code: ErrorCode = ErrorCode.PERMISSION_DENIED

    status_code: int = HTTPStatus.FORBIDDEN


@dataclass(kw_only=True)
class ResourceNotFoundException(ClientException):
    code: ErrorCode = ErrorCode.RESOURCE_NOT_FOUND

    status_code: int = HTTPStatus.NOT_FOUND


@dataclass(kw_only=True)
class ResourceConflictException(ClientException):
    code: ErrorCode = ErrorCode.RESOURCE_CONFLICT

    status_code: int = HTTPStatus.CONFLICT


###############################################################################
# Server Errors
###############################################################################


@dataclass(kw_only=True)
class ServerException(DatavionException):
    """
    Base server exception.
    """

    code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR


@dataclass(kw_only=True)
class DatabaseException(ServerException):
    code: ErrorCode = ErrorCode.DATABASE_ERROR


@dataclass(kw_only=True)
class CacheException(ServerException):
    code: ErrorCode = ErrorCode.CACHE_ERROR


@dataclass(kw_only=True)
class IntegrationException(ServerException):
    code: ErrorCode = ErrorCode.INTEGRATION_ERROR


@dataclass(kw_only=True)
class ConfigurationException(ServerException):
    code: ErrorCode = ErrorCode.CONFIGURATION_ERROR


@dataclass(kw_only=True)
class WorkflowException(ServerException):
    code: ErrorCode = ErrorCode.WORKFLOW_ERROR


@dataclass(kw_only=True)
class AuditException(ServerException):
    code: ErrorCode = ErrorCode.AUDIT_ERROR


__all__ = (
    "AuditException",
    "AuthenticationException",
    "AuthorizationException",
    "CacheException",
    "ClientException",
    "ConfigurationException",
    "DatabaseException",
    "DatavionException",
    "IntegrationException",
    "ResourceConflictException",
    "ResourceNotFoundException",
    "ServerException",
    "ValidationException",
    "WorkflowException",
)
