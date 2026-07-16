"""
Public exception API for the Datavion AI platform.

Feature applications should import framework exceptions and
error codes from this package instead of importing individual
modules directly.
"""

from __future__ import annotations

from .base import (
    AuthenticationException,
    ConfigurationException,
    DatavionException,
    DuplicateResourceException,
    ExternalServiceException,
    FeatureDisabledException,
    FileValidationException,
    PermissionDeniedException,
    ResourceNotFoundException,
    ValidationException,
)
from .codes import ErrorCode

__all__ = [
    "ErrorCode",
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
