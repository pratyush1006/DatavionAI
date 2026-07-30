"""
Document type definitions for DatavionOS.

Provides reusable type aliases shared across the document
framework.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

###############################################################################
# Document Identity
###############################################################################

type DocumentID = str | int

type DocumentName = str

type DocumentType = str


###############################################################################
# File Information
###############################################################################

type FileName = str

type FilePath = str

type MimeType = str

type StorageKey = str


###############################################################################
# Context and Metadata
###############################################################################

type DocumentMetadata = Mapping[
    str,
    Any,
]


type DocumentContext = Mapping[
    str,
    Any,
]


###############################################################################
# Tenant Context
###############################################################################

type TenantID = str | int | None

type OrganizationID = str | int | None


###############################################################################
# Versioning
###############################################################################

type DocumentVersion = int


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
