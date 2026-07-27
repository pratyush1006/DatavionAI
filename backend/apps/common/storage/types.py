"""
Storage type definitions for DatavionOS.

Provides reusable type aliases shared across the storage
framework.
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from typing import (
    Any,
    TypeAlias,
)

###############################################################################
# Storage Paths
###############################################################################

StoragePath: TypeAlias = str


###############################################################################
# File Content
###############################################################################

FileContent: TypeAlias = bytes | bytearray


###############################################################################
# File Metadata
###############################################################################

FileMetadata: TypeAlias = Mapping[
    str,
    Any,
]


###############################################################################
# File Identifiers
###############################################################################

FileID: TypeAlias = str


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "FileContent",
    "FileID",
    "FileMetadata",
    "StoragePath",
)
