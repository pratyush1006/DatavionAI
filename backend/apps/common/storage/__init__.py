"""
DatavionOS storage framework.

Provides the public API for platform storage capabilities.

Supports:

- Storage abstraction
- Multiple providers
- Tenant-aware storage
- File metadata
- Secure access URLs

Business applications should import storage utilities from this
package instead of provider implementations.
"""

from __future__ import annotations

from .backend import (
    StorageBackend,
)
from .client import (
    StorageClient,
)
from .config import (
    DEFAULT_STORAGE_CONFIGURATION,
    DEFAULT_STORAGE_SECURITY_CONFIGURATION,
    StorageConfiguration,
    StorageSecurityConfiguration,
)
from .constants import (
    AWS_S3_STORAGE_PROVIDER,
    AZURE_BLOB_STORAGE_PROVIDER,
    DEFAULT_MAX_FILE_SIZE,
    DEFAULT_SIGNED_URL_EXPIRATION,
    DEFAULT_STORAGE_PROVIDER,
    DOCUMENT_CONTENT_TYPES,
    IMAGE_CONTENT_TYPES,
    LOCAL_STORAGE_PROVIDER,
)
from .exceptions import (
    StorageConfigurationError,
    StorageConnectionError,
    StorageDeleteError,
    StorageDownloadError,
    StorageError,
    StorageFileNotFoundError,
    StoragePermissionError,
    StorageProviderError,
    StorageSecurityError,
    StorageUploadError,
)
from .models import (
    StorageLocation,
    StoredFile,
)
from .providers import (
    AzureBlobStorageProvider,
    LocalStorageProvider,
    S3StorageProvider,
)
from .types import (
    FileContent,
    FileID,
    FileMetadata,
    StoragePath,
)

__all__: tuple[str, ...] = (
    # Backend
    "StorageBackend",
    # Client
    "StorageClient",
    # Configuration
    "StorageConfiguration",
    "StorageSecurityConfiguration",
    "DEFAULT_STORAGE_CONFIGURATION",
    "DEFAULT_STORAGE_SECURITY_CONFIGURATION",
    # Models
    "StoredFile",
    "StorageLocation",
    # Types
    "FileContent",
    "FileID",
    "FileMetadata",
    "StoragePath",
    # Providers
    "LocalStorageProvider",
    "S3StorageProvider",
    "AzureBlobStorageProvider",
    # Constants
    "LOCAL_STORAGE_PROVIDER",
    "AWS_S3_STORAGE_PROVIDER",
    "AZURE_BLOB_STORAGE_PROVIDER",
    "DEFAULT_STORAGE_PROVIDER",
    "DEFAULT_MAX_FILE_SIZE",
    "DEFAULT_SIGNED_URL_EXPIRATION",
    "DOCUMENT_CONTENT_TYPES",
    "IMAGE_CONTENT_TYPES",
    # Exceptions
    "StorageError",
    "StorageConfigurationError",
    "StorageProviderError",
    "StorageConnectionError",
    "StorageUploadError",
    "StorageDownloadError",
    "StorageDeleteError",
    "StorageFileNotFoundError",
    "StoragePermissionError",
    "StorageSecurityError",
)
