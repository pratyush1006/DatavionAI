"""
Document exception hierarchy for DatavionOS.

Provides reusable exceptions for the document framework.
"""

from __future__ import annotations


class DocumentError(
    Exception,
):
    """
    Base exception for document errors.
    """


class DocumentConfigurationError(
    DocumentError,
):
    """
    Raised when document configuration is invalid.
    """


class DocumentNotFoundError(
    DocumentError,
):
    """
    Raised when a document does not exist.
    """


class DocumentAlreadyExistsError(
    DocumentError,
):
    """
    Raised when creating a duplicate document.
    """


class DocumentValidationError(
    DocumentError,
):
    """
    Raised when document validation fails.
    """


class DocumentStorageError(
    DocumentError,
):
    """
    Raised when storage operation fails.
    """


class DocumentUploadError(
    DocumentStorageError,
):
    """
    Raised when document upload fails.
    """


class DocumentDownloadError(
    DocumentStorageError,
):
    """
    Raised when document download fails.
    """


class DocumentDeleteError(
    DocumentStorageError,
):
    """
    Raised when document deletion fails.
    """


class DocumentVersionError(
    DocumentError,
):
    """
    Raised when versioning operation fails.
    """


class DocumentProcessingError(
    DocumentError,
):
    """
    Raised during document processing failures.

    Examples:

    - OCR failure
    - Extraction failure
    - AI processing failure
    """


class DocumentPermissionError(
    DocumentError,
):
    """
    Raised when document access is denied.
    """


class DocumentRegistryError(
    DocumentError,
):
    """
    Raised when document registry operation fails.
    """


class DocumentAlreadyRegisteredError(
    DocumentRegistryError,
):
    """
    Raised when registering an existing document handler.
    """


class DocumentHandlerNotFoundError(
    DocumentRegistryError,
):
    """
    Raised when document handler is missing.
    """


__all__: tuple[str, ...] = (
    "DocumentAlreadyExistsError",
    "DocumentAlreadyRegisteredError",
    "DocumentConfigurationError",
    "DocumentDeleteError",
    "DocumentDownloadError",
    "DocumentError",
    "DocumentHandlerNotFoundError",
    "DocumentNotFoundError",
    "DocumentPermissionError",
    "DocumentProcessingError",
    "DocumentRegistryError",
    "DocumentStorageError",
    "DocumentUploadError",
    "DocumentValidationError",
    "DocumentVersionError",
)
