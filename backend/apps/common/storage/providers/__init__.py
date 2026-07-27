"""
DatavionOS storage providers.

Provides available storage backend implementations.

Providers are adapters only.
Business modules should use StorageClient.
"""

from __future__ import annotations

from .azure import (
    AzureBlobStorageProvider,
)
from .local import (
    LocalStorageProvider,
)
from .s3 import (
    S3StorageProvider,
)

__all__: tuple[str, ...] = (
    "AzureBlobStorageProvider",
    "LocalStorageProvider",
    "S3StorageProvider",
)
