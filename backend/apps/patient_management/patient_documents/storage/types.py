"""
Storage value objects.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class StorageObject:
    """
    Metadata describing a stored object.
    """

    path: str
    size: int
    mime_type: str
    checksum: str | None = None
    etag: str | None = None
    version_id: str | None = None
    storage_class: str | None = None


__all__ = [
    "StorageObject",
]
