"""
Document type definitions for DatavionOS.

Provides reusable type aliases shared across the document
framework.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeAlias

###############################################################################
# Document Identity
###############################################################################

DocumentID: TypeAlias = str | int

DocumentName: TypeAlias = str

DocumentType: TypeAlias = str


###############################################################################
# File Information
###############################################################################

FileName: TypeAlias = str

FilePath: TypeAlias = str

MimeType: TypeAlias = str

StorageKey: TypeAlias = str


###############################################################################
# Context and Metadata
###############################################################################

DocumentMetadata: TypeAlias = Mapping[
    str,
    Any,
]


DocumentContext: TypeAlias = Mapping[
    str,
    Any,
]


###############################################################################
# Tenant Context
###############################################################################

TenantID: TypeAlias = str | int | None

OrganizationID: TypeAlias = str | int | None


###############################################################################
# Versioning
###############################################################################

DocumentVersion: TypeAlias = int


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "DocumentContext",
    "DocumentID",
    "DocumentMetadata",
    "DocumentName",
    "DocumentType",
    "DocumentVersion",
    "FileName",
    "FilePath",
    "MimeType",
    "OrganizationID",
    "StorageKey",
    "TenantID",
)
