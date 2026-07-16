"""
Platform exception hierarchy for the Datavion AI platform.

Service and domain layers should raise these exceptions instead of
Django REST Framework exceptions. The global exception handler is
responsible for translating them into standardized HTTP responses.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from rest_framework import status

from apps.common.exceptions.codes import ErrorCode


class DatavionException(Exception):
    """
    Base exception for all platform-specific exceptions.
    """

    error_code: ErrorCode = ErrorCode.SERVER_ERROR

    default_message: str = "An unexpected error occurred."

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        *,
        message: str | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        """
        Initialize the platform exception.
        """

        super().__init__(
            message or self.default_message,
        )

        self.message = message or self.default_message

        self.details = details

    @property
    def code(
        self,
    ) -> str:
        """
        Return the platform error code.
        """

        return self.error_code.value


class ValidationException(
    DatavionException,
):
    """
    Raised when validation fails.
    """

    error_code = ErrorCode.VALIDATION_ERROR

    default_message = "Validation failed."

    status_code = status.HTTP_400_BAD_REQUEST


class AuthenticationException(
    DatavionException,
):
    """
    Raised when authentication is required.
    """

    error_code = ErrorCode.AUTHENTICATION_REQUIRED

    default_message = "Authentication required."

    status_code = status.HTTP_401_UNAUTHORIZED


class PermissionDeniedException(
    DatavionException,
):
    """
    Raised when the user lacks permission.
    """

    error_code = ErrorCode.PERMISSION_DENIED

    default_message = "Permission denied."

    status_code = status.HTTP_403_FORBIDDEN


class ResourceNotFoundException(
    DatavionException,
):
    """
    Raised when a requested resource does not exist.
    """

    error_code = ErrorCode.RESOURCE_NOT_FOUND

    default_message = "Resource not found."

    status_code = status.HTTP_404_NOT_FOUND


class DuplicateResourceException(
    DatavionException,
):
    """
    Raised when attempting to create a duplicate resource.
    """

    error_code = ErrorCode.DUPLICATE_RESOURCE

    default_message = "Resource already exists."

    status_code = status.HTTP_409_CONFLICT


class ConfigurationException(
    DatavionException,
):
    """
    Raised when platform configuration is invalid.
    """

    error_code = ErrorCode.CONFIGURATION_NOT_FOUND

    default_message = "Configuration not found."

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class FeatureDisabledException(
    DatavionException,
):
    """
    Raised when a platform feature is disabled.
    """

    error_code = ErrorCode.FEATURE_DISABLED

    default_message = "Feature is disabled."

    status_code = status.HTTP_403_FORBIDDEN


class FileValidationException(
    DatavionException,
):
    """
    Raised when file validation fails.
    """

    error_code = ErrorCode.INVALID_FILE_TYPE

    default_message = "Invalid file."

    status_code = status.HTTP_400_BAD_REQUEST


class ExternalServiceException(
    DatavionException,
):
    """
    Raised when an external service fails.
    """

    error_code = ErrorCode.EXTERNAL_SERVICE_ERROR

    default_message = "External service error."

    status_code = status.HTTP_502_BAD_GATEWAY


__all__ = [
    "DatavionException",
    "ValidationException",
    "AuthenticationException",
    "PermissionDeniedException",
    "ResourceNotFoundException",
    "DuplicateResourceException",
    "ConfigurationException",
    "FeatureDisabledException",
    "FileValidationException",
    "ExternalServiceException",
]
