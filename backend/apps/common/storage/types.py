"""
Storage type definitions for DatavionOS.

Provides reusable type aliases shared across
the storage infrastructure layer.

Storage does not know about business domains.
It only manages files, objects, and storage metadata.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
)

# ---------------------------------------------------------------------
# Storage Identity
# ---------------------------------------------------------------------

StorageKey = str

StoragePath = str

FileName = str


# ---------------------------------------------------------------------
# File Content
# ---------------------------------------------------------------------

FileContent = bytes | bytearray | memoryview


# ---------------------------------------------------------------------
# File Information
# ---------------------------------------------------------------------

MimeType = str

FileSize = int

Checksum = str


# ---------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------

FileMetadata = Mapping[
    str,
    Any,
]


StorageContext = Mapping[
    str,
    Any,
]


# ---------------------------------------------------------------------
# Ownership Context
# ---------------------------------------------------------------------

TenantID = str | int | None

OrganizationID = str | int | None


# ---------------------------------------------------------------------
# Versioning
# ---------------------------------------------------------------------

VersionNumber = int


__all__: tuple[str, ...] = (
    "Checksum",
    "FileContent",
    "FileMetadata",
    "FileName",
    "FileSize",
    "MimeType",
    "OrganizationID",
    "StorageContext",
    "StorageKey",
    "StoragePath",
    "TenantID",
    "VersionNumber",
)
