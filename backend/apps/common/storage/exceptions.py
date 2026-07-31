"""
Storage exception hierarchy for DatavionOS.

Provides reusable exceptions for the storage infrastructure layer.

Storage exceptions are independent from business domains:

- healthcare
- finance
- analytics
- reporting
"""

from __future__ import annotations


class StorageError(
    Exception,
):
    """
    Base exception for storage errors.
    """


class StorageConfigurationError(
    StorageError,
):
    """
    Raised when storage configuration is invalid.
    """


class StorageNotFoundError(
    StorageError,
):
    """
    Raised when stored object is not found.
    """


class StorageFileNotFoundError(
    StorageNotFoundError,
):
    """
    Raised when a file is not found in storage.
    """


class StorageAlreadyExistsError(
    StorageError,
):
    """
    Raised when creating duplicate storage object.
    """


class StorageValidationError(
    StorageError,
):
    """
    Raised when storage validation fails.
    """


class StorageOperationError(
    StorageError,
):
    """
    Raised when storage operation fails.
    """


class StorageUploadError(
    StorageOperationError,
):
    """
    Raised when upload fails.
    """


class StorageDownloadError(
    StorageOperationError,
):
    """
    Raised when download fails.
    """


class StorageDeleteError(
    StorageOperationError,
):
    """
    Raised when delete fails.
    """


class StorageConnectionError(
    StorageOperationError,
):
    """
    Raised when connection to storage backend fails.
    """


class StorageRegistryError(
    StorageError,
):
    """
    Raised when storage registry operation fails.
    """


class StorageAlreadyRegisteredError(
    StorageRegistryError,
):
    """
    Raised when registering an existing storage handler.
    """


class StorageHandlerNotFoundError(
    StorageRegistryError,
):
    """
    Raised when storage handler is missing.
    """


__all__: tuple[str, ...] = (
    "StorageError",
    "StorageConfigurationError",
    "StorageNotFoundError",
    "StorageFileNotFoundError",
    "StorageAlreadyExistsError",
    "StorageValidationError",
    "StorageOperationError",
    "StorageUploadError",
    "StorageDownloadError",
    "StorageDeleteError",
    "StorageConnectionError",
    "StorageRegistryError",
    "StorageAlreadyRegisteredError",
    "StorageHandlerNotFoundError",
)
