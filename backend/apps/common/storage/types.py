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
)

###############################################################################
# Storage Paths
###############################################################################

type StoragePath = str


###############################################################################
# File Content
###############################################################################

type FileContent = bytes | bytearray


###############################################################################
# File Metadata
###############################################################################

type FileMetadata = Mapping[
    str,
    Any,
]


###############################################################################
# File Identifiers
###############################################################################

type FileID = str


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "FileContent",
    "FileID",
    "FileMetadata",
    "StoragePath",
)
