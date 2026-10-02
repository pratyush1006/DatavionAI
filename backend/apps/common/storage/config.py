"""
Storage configuration models for DatavionOS.

Provides immutable configuration objects shared across storage
providers.

Provider implementations should consume this configuration
without knowing business-domain details.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.storage.constants import (
    DEFAULT_STORAGE_BACKEND,
)
from apps.common.storage.types import (
    StoragePath,
)


@dataclass(
    frozen=True,
    slots=True,
)
class StorageConfiguration:
    """
    Storage backend configuration.
    """

    provider: str = DEFAULT_STORAGE_BACKEND

    bucket_name: str | None = None

    base_path: StoragePath = ""

    enable_encryption: bool = True

    generate_signed_urls: bool = True

    signed_url_expiration: int = 3600

    tenant_isolation: bool = True


@dataclass(
    frozen=True,
    slots=True,
)
class StorageSecurityConfiguration:
    """
    Storage security configuration.

    Controls storage-level security behaviour.
    """

    encryption_enabled: bool = True

    checksum_validation: bool = True

    virus_scan_enabled: bool = False


DEFAULT_STORAGE_CONFIGURATION = StorageConfiguration()

DEFAULT_STORAGE_SECURITY_CONFIGURATION = StorageSecurityConfiguration()


__all__: tuple[str, ...] = (
    "DEFAULT_STORAGE_CONFIGURATION",
    "DEFAULT_STORAGE_SECURITY_CONFIGURATION",
    "StorageConfiguration",
    "StorageSecurityConfiguration",
)


def get_storage_client():
    """
    Return the canonical application-facing StorageClient.
    """
    from apps.common.storage.client import StorageClient
    from apps.common.storage.providers.django_storage import (
        DjangoStorageBackend,
    )

    return StorageClient(
        DjangoStorageBackend(),
    )
