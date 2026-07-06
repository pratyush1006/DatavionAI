"""
Platform exception hierarchy for Datavion AI.

Service and domain layers should raise these exceptions instead of
Django REST Framework exceptions. The global exception handler is
responsible for translating them into standardized HTTP responses.
"""

from __future__ import annotations

from typing import Any

from rest_framework import status

from apps.common.exceptions.codes import ErrorCode


class DatavionException(Exception):
    """
    Base exception for all platform-specific exceptions.
    """

    error_code: ErrorCode = ErrorCode.SERVER_ERROR
    default_message: str = "An unexpected error occurred."

    # Explicitly type as int so subclasses can override freely.
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        *,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message or self.default_message)
        self.message = message or self.default_message
        self.details = details


class ValidationException(DatavionException):
    error_code: ErrorCode = ErrorCode.VALIDATION_ERROR
    default_message: str = "Validation failed."
    status_code: int = status.HTTP_400_BAD_REQUEST


class AuthenticationException(DatavionException):
    error_code: ErrorCode = ErrorCode.AUTHENTICATION_REQUIRED
    default_message: str = "Authentication required."
    status_code: int = status.HTTP_401_UNAUTHORIZED


class PermissionDeniedException(DatavionException):
    error_code: ErrorCode = ErrorCode.PERMISSION_DENIED
    default_message: str = "Permission denied."
    status_code: int = status.HTTP_403_FORBIDDEN


class ResourceNotFoundException(DatavionException):
    error_code: ErrorCode = ErrorCode.RESOURCE_NOT_FOUND
    default_message: str = "Resource not found."
    status_code: int = status.HTTP_404_NOT_FOUND


class DuplicateResourceException(DatavionException):
    error_code: ErrorCode = ErrorCode.DUPLICATE_RESOURCE
    default_message: str = "Resource already exists."
    status_code: int = status.HTTP_409_CONFLICT


class ConfigurationException(DatavionException):
    error_code: ErrorCode = ErrorCode.CONFIGURATION_NOT_FOUND
    default_message: str = "Configuration not found."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class FeatureDisabledException(DatavionException):
    error_code: ErrorCode = ErrorCode.FEATURE_DISABLED
    default_message: str = "Feature is disabled."
    status_code: int = status.HTTP_403_FORBIDDEN


class FileValidationException(DatavionException):
    error_code: ErrorCode = ErrorCode.INVALID_FILE_TYPE
    default_message: str = "Invalid file."
    status_code: int = status.HTTP_400_BAD_REQUEST


class ExternalServiceException(DatavionException):
    error_code: ErrorCode = ErrorCode.EXTERNAL_SERVICE_ERROR
    default_message: str = "External service error."
    status_code: int = status.HTTP_502_BAD_GATEWAY


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
