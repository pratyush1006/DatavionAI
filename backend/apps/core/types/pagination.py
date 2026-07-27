"""
Pagination type aliases for the Datavion AI platform.

Provides reusable pagination contracts used across
DatavionOS APIs.
"""

from __future__ import annotations

from typing import TypeAlias

from .json import JSONValue

# ============================================================================
# Pagination Primitive Types
# ============================================================================

PageNumber: TypeAlias = int

PageSize: TypeAlias = int

Offset: TypeAlias = int

Limit: TypeAlias = int

Cursor: TypeAlias = str


# ============================================================================
# Pagination Request Types
# ============================================================================

PaginationParams: TypeAlias = dict[
    str,
    PageNumber | PageSize | Offset | Limit | Cursor,
]


# ============================================================================
# Pagination Response Types
# ============================================================================

PaginatedResponse: TypeAlias = dict[
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
