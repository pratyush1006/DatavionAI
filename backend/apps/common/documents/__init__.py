"""
DatavionOS document framework.

Provides the public API for platform document capabilities.

Supports:

- Document lifecycle management
- File metadata handling
- Storage abstraction
- Document processors
- Version-ready architecture
- AI/RAG document pipeline integration

Business applications should import document utilities from
this package instead of internal modules.
"""

from __future__ import annotations

from .config import (
    DEFAULT_DOCUMENT_AI_CONFIGURATION,
    DEFAULT_DOCUMENT_CONFIGURATION,
    DEFAULT_DOCUMENT_STORAGE_CONFIGURATION,
    DocumentAIConfiguration,
    DocumentConfiguration,
    DocumentStorageConfiguration,
)
from .constants import (
    ACCESS_INTERNAL,
    ACCESS_PRIVATE,
    ACCESS_PUBLIC,
    ACCESS_SHARED,
    CATEGORY_CLINICAL,
    CATEGORY_FINANCIAL,
    CATEGORY_GENERAL,
    CATEGORY_LABORATORY,
    CATEGORY_LEGAL,
    CATEGORY_MEDICAL,
    CATEGORY_SYSTEM,
    DEFAULT_ACCESS_LEVEL,
    DEFAULT_CATEGORY,
    DEFAULT_STATUS,
    DEFAULT_STORAGE_BACKEND,
    PROCESSING_COMPLETED,
    PROCESSING_FAILED,
    PROCESSING_PENDING,
    PROCESSING_PROCESSING,
    STATUS_ACTIVE,
    STATUS_ARCHIVED,
    STATUS_DELETED,
    STATUS_DRAFT,
    STORAGE_AZURE,
    STORAGE_GCP,
    STORAGE_LOCAL,
    STORAGE_S3,
    VERSION_CREATE,
    VERSION_RESTORE,
    VERSION_UPDATE,
)
from .exceptions import (
    DocumentAlreadyExistsError,
    DocumentAlreadyRegisteredError,
    DocumentConfigurationError,
    DocumentDeleteError,
    DocumentDownloadError,
    DocumentError,
    DocumentHandlerNotFoundError,
    DocumentNotFoundError,
    DocumentPermissionError,
    DocumentProcessingError,
    DocumentRegistryError,
    DocumentStorageError,
    DocumentUploadError,
    DocumentValidationError,
    DocumentVersionError,
)
from .models import (
    Document,
    DocumentMetadataInfo,
    DocumentResult,
    DocumentVersionInfo,
)
from .registry import (
    DocumentProcessor,
    DocumentRegistry,
    DocumentStorageProvider,
    document_registry,
)
from .services import (
    DocumentService,
    document_service,
)
from .storage import (
    DocumentStorage,
    document_storage,
)
from .types import (
    DocumentContext,
    DocumentID,
    DocumentMetadata,
    DocumentName,
    DocumentType,
    DocumentVersion,
    FileName,
    FilePath,
    MimeType,
    OrganizationID,
    StorageKey,
    TenantID,
)

__all__: tuple[str, ...] = (
    # Models
    "Document",
    "DocumentMetadataInfo",
    "DocumentVersionInfo",
    "DocumentResult",
    # Services
    "DocumentService",
    "document_service",
    # Storage
    "DocumentStorage",
    "document_storage",
    # Registry
    "DocumentRegistry",
    "DocumentStorageProvider",
    "DocumentProcessor",
    "document_registry",
    # Configuration
    "DocumentConfiguration",
    "DocumentStorageConfiguration",
    "DocumentAIConfiguration",
    "DEFAULT_DOCUMENT_CONFIGURATION",
    "DEFAULT_DOCUMENT_STORAGE_CONFIGURATION",
    "DEFAULT_DOCUMENT_AI_CONFIGURATION",
    # Types
    "DocumentID",
    "DocumentName",
    "DocumentType",
    "DocumentMetadata",
    "DocumentContext",
    "DocumentVersion",
    "FileName",
    "FilePath",
    "MimeType",
    "StorageKey",
    "TenantID",
    "OrganizationID",
    # Storage Backends
    "STORAGE_LOCAL",
    "STORAGE_S3",
    "STORAGE_AZURE",
    "STORAGE_GCP",
    # Status
    "STATUS_DRAFT",
    "STATUS_ACTIVE",
    "STATUS_ARCHIVED",
    "STATUS_DELETED",
    # Categories
    "CATEGORY_GENERAL",
    "CATEGORY_MEDICAL",
    "CATEGORY_CLINICAL",
    "CATEGORY_LABORATORY",
    "CATEGORY_FINANCIAL",
    "CATEGORY_LEGAL",
    "CATEGORY_SYSTEM",
    # Access
    "ACCESS_PRIVATE",
    "ACCESS_INTERNAL",
    "ACCESS_SHARED",
    "ACCESS_PUBLIC",
    # Processing
    "PROCESSING_PENDING",
    "PROCESSING_PROCESSING",
    "PROCESSING_COMPLETED",
    "PROCESSING_FAILED",
    # Versioning
    "VERSION_CREATE",
    "VERSION_UPDATE",
    "VERSION_RESTORE",
    # Defaults
    "DEFAULT_STATUS",
    "DEFAULT_CATEGORY",
    "DEFAULT_ACCESS_LEVEL",
    "DEFAULT_STORAGE_BACKEND",
    # Exceptions
    "DocumentError",
    "DocumentConfigurationError",
    "DocumentNotFoundError",
    "DocumentAlreadyExistsError",
    "DocumentValidationError",
    "DocumentStorageError",
    "DocumentUploadError",
    "DocumentDownloadError",
    "DocumentDeleteError",
    "DocumentVersionError",
    "DocumentProcessingError",
    "DocumentPermissionError",
    "DocumentRegistryError",
    "DocumentAlreadyRegisteredError",
    "DocumentHandlerNotFoundError",
)
