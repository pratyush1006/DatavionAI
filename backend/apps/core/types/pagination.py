"""
Pagination type aliases for the Datavion AI platform.

Provides reusable pagination contracts used across
DatavionOS APIs.
"""

from __future__ import annotations

from .json import JSONValue

# ============================================================================
# Pagination Primitive Types
# ============================================================================

type PageNumber = int

type PageSize = int

type Offset = int

type Limit = int

type Cursor = str


# ============================================================================
# Pagination Request Types
# ============================================================================

type PaginationParams = dict[
    str,
    PageNumber | PageSize | Offset | Limit | Cursor,
]


# ============================================================================
# Pagination Response Types
# ============================================================================

type PaginatedResponse = dict[
    str,
    JSONValue,
]


__all__ = [
    "Cursor",
    "Limit",
    "Offset",
    "PageNumber",
    "PageSize",
    "PaginatedResponse",
    "PaginationParams",
]
