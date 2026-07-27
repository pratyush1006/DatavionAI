"""
Storage exception hierarchy for DatavionOS.

Provides reusable exceptions for the storage framework.
"""

from __future__ import annotations


class StorageError(
    Exception,
):
    """
    Base exception for all storage-related errors.
    """


class StorageConfigurationError(
    StorageError,
):
    """
    Raised when storage configuration is invalid.
    """


class StorageProviderError(
    StorageError,
):
    """
    Raised when a storage provider operation fails.
    """


class StorageConnectionError(
    StorageProviderError,
):
    """
    Raised when connection to storage provider fails.
    """


class StorageUploadError(
    StorageProviderError,
):
    """
    Raised when file upload fails.
    """


class StorageDownloadError(
    StorageProviderError,
):
    """
    Raised when file download fails.
    """


class StorageDeleteError(
    StorageProviderError,
):
    """
    Raised when file deletion fails.
    """


class StorageFileNotFoundError(
    StorageError,
):
    """
    Raised when requested file does not exist.
    """


class StoragePermissionError(
    StorageError,
):
    """
    Raised when access to stored data is denied.
    """


class StorageSecurityError(
    StorageError,
):
    """
    Raised when storage security validation fails.

    Examples:

    - checksum mismatch
    - encryption failure
    - invalid signed URL
    """


__all__: tuple[str, ...] = (
    "StorageConnectionError",
    "StorageConfigurationError",
    "StorageDeleteError",
    "StorageDownloadError",
    "StorageError",
    "StorageFileNotFoundError",
    "StoragePermissionError",
    "StorageProviderError",
    "StorageSecurityError",
    "StorageUploadError",
)
