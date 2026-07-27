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

        payload = {
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


class ClientException(DatavionException):
    """
    Base client exception.
    """

    status_code = HTTPStatus.BAD_REQUEST


class ValidationException(ClientException):
    code = ErrorCode.VALIDATION_ERROR

    status_code = HTTPStatus.BAD_REQUEST


class AuthenticationException(ClientException):
    code = ErrorCode.UNAUTHENTICATED

    status_code = HTTPStatus.UNAUTHORIZED


class AuthorizationException(ClientException):
    code = ErrorCode.PERMISSION_DENIED

    status_code = HTTPStatus.FORBIDDEN


class ResourceNotFoundException(ClientException):
    code = ErrorCode.RESOURCE_NOT_FOUND

    status_code = HTTPStatus.NOT_FOUND


class ResourceConflictException(ClientException):
    code = ErrorCode.RESOURCE_CONFLICT

    status_code = HTTPStatus.CONFLICT


###############################################################################
# Server Errors
###############################################################################


class ServerException(DatavionException):
    """
    Base server exception.
    """

    code = ErrorCode.INTERNAL_SERVER_ERROR

    status_code = HTTPStatus.INTERNAL_SERVER_ERROR


class DatabaseException(ServerException):
    code = ErrorCode.DATABASE_ERROR


class CacheException(ServerException):
    code = ErrorCode.CACHE_ERROR


class IntegrationException(ServerException):
    code = ErrorCode.INTEGRATION_ERROR


class ConfigurationException(ServerException):
    code = ErrorCode.CONFIGURATION_ERROR


class WorkflowException(ServerException):
    code = ErrorCode.WORKFLOW_ERROR


class AuditException(ServerException):
    code = ErrorCode.AUDIT_ERROR


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
