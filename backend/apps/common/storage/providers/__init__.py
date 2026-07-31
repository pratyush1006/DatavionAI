"""
DatavionOS storage providers.

Provides available storage backend implementations.

Providers are adapters only.

Business modules should use StorageClient.
"""

from __future__ import annotations

from .azure import (
    AzureBlobStorageBackend,
)
from .gcs import (
    GCSStorageBackend,
)
from .local import (
    LocalStorageBackend,
)
from .s3 import (
    S3StorageBackend,
)

__all__: tuple[str, ...] = (
    "AzureBlobStorageBackend",
    "LocalStorageBackend",
    "S3StorageBackend",
    "GCSStorageBackend",
)
