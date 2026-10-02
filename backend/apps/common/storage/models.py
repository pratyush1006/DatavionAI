"""
Storage models for DatavionOS.

Defines immutable metadata models representing stored files.

These models only describe storage-level information.

Domain ownership remains with feature applications:

- healthcare
- finance
- analytics
- reporting
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
)

from apps.common.storage.types import (
    FileMetadata,
    StoragePath,
)


@dataclass(
    frozen=True,
    slots=True,
)
class StoredFile:
    """
    Metadata representation of a stored file.

    Example:

        StoredFile(
            path="tenant-1/report.pdf",
            name="report.pdf",
            size=102400,
            content_type="application/pdf",
        )
    """

    path: StoragePath

    name: str

    size: int

    content_type: str | None = None

    checksum: str | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    metadata: FileMetadata = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class StorageLocation:
    """
    Represents a storage location.

    Used for tenant-aware and provider-aware
    storage routing.
    """

    tenant_id: str | None = None

    organization_id: str | None = None

    namespace: str | None = None


__all__: tuple[str, ...] = (
    "StorageLocation",
    "StoredFile",
)
