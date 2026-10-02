"""
DatavionAI API Response Constants.

Centralized response payload definitions used throughout the DatavionAI
platform.

This module defines immutable response keys, response status values,
pagination metadata keys, audit metadata keys, error payload fields,
warning fields, hypermedia keys, and reserved response fields.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- No business logic
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Response Status
###############################################################################


class ResponseStatus(StrEnum):
    """
    Standard API response status values.
    """

    SUCCESS = "success"

    ERROR = "error"

    FAIL = "fail"

    WARNING = "warning"

    PARTIAL = "partial"


###############################################################################
# Root Response Keys
###############################################################################

KEY_SUCCESS: Final[str] = "success"

KEY_STATUS: Final[str] = "status"

KEY_MESSAGE: Final[str] = "message"

KEY_DETAIL: Final[str] = "detail"

KEY_DATA: Final[str] = "data"

KEY_ERRORS: Final[str] = "errors"

KEY_WARNINGS: Final[str] = "warnings"

KEY_META: Final[str] = "meta"

KEY_LINKS: Final[str] = "links"

###############################################################################
# Metadata Keys
###############################################################################

META_REQUEST_ID: Final[str] = "request_id"

META_TIMESTAMP: Final[str] = "timestamp"

META_API_VERSION: Final[str] = "api_version"

META_EXECUTION_TIME: Final[str] = "execution_time"

META_TRACE_ID: Final[str] = "trace_id"

META_CORRELATION_ID: Final[str] = "correlation_id"

###############################################################################
# Pagination Metadata
###############################################################################

META_PAGINATION: Final[str] = "pagination"

PAGINATION_PAGE: Final[str] = "page"

PAGINATION_PAGE_SIZE: Final[str] = "page_size"

PAGINATION_TOTAL_ITEMS: Final[str] = "total_items"

PAGINATION_TOTAL_PAGES: Final[str] = "total_pages"

PAGINATION_HAS_NEXT: Final[str] = "has_next"

PAGINATION_HAS_PREVIOUS: Final[str] = "has_previous"

PAGINATION_NEXT_CURSOR: Final[str] = "next_cursor"

PAGINATION_PREVIOUS_CURSOR: Final[str] = "previous_cursor"

###############################################################################
# Error Payload
###############################################################################

ERROR_CODE: Final[str] = "code"

ERROR_FIELD: Final[str] = "field"

ERROR_MESSAGE: Final[str] = "message"

ERROR_DETAIL: Final[str] = "detail"

ERROR_TYPE: Final[str] = "type"

ERROR_HINT: Final[str] = "hint"

ERROR_DOCS: Final[str] = "documentation"

###############################################################################
# Validation
###############################################################################

VALIDATION_ERRORS: Final[str] = "validation_errors"

FIELD_ERRORS: Final[str] = "field_errors"

NON_FIELD_ERRORS: Final[str] = "non_field_errors"

###############################################################################
# Bulk Operations
###############################################################################

BULK_TOTAL: Final[str] = "total"

BULK_PROCESSED: Final[str] = "processed"

BULK_CREATED: Final[str] = "created"

BULK_UPDATED: Final[str] = "updated"

BULK_DELETED: Final[str] = "deleted"

BULK_SKIPPED: Final[str] = "skipped"

BULK_FAILED: Final[str] = "failed"

###############################################################################
# Audit Metadata
###############################################################################

AUDIT_CREATED_AT: Final[str] = "created_at"

AUDIT_UPDATED_AT: Final[str] = "updated_at"

AUDIT_CREATED_BY: Final[str] = "created_by"

AUDIT_UPDATED_BY: Final[str] = "updated_by"

###############################################################################
# Hypermedia
###############################################################################

LINK_SELF: Final[str] = "self"

LINK_NEXT: Final[str] = "next"

LINK_PREVIOUS: Final[str] = "previous"

LINK_FIRST: Final[str] = "first"

LINK_LAST: Final[str] = "last"

###############################################################################
# Reserved Response Fields
###############################################################################

RESERVED_RESPONSE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        KEY_SUCCESS,
        KEY_STATUS,
        KEY_MESSAGE,
        KEY_DETAIL,
        KEY_DATA,
        KEY_ERRORS,
        KEY_WARNINGS,
        KEY_META,
        KEY_LINKS,
    }
)

###############################################################################
# Metadata Groups
###############################################################################

RESPONSE_META_FIELDS: Final[frozenset[str]] = frozenset(
    {
        META_REQUEST_ID,
        META_TIMESTAMP,
        META_API_VERSION,
        META_EXECUTION_TIME,
        META_TRACE_ID,
        META_CORRELATION_ID,
    }
)

PAGINATION_META_FIELDS: Final[frozenset[str]] = frozenset(
    {
        PAGINATION_PAGE,
        PAGINATION_PAGE_SIZE,
        PAGINATION_TOTAL_ITEMS,
        PAGINATION_TOTAL_PAGES,
        PAGINATION_HAS_NEXT,
        PAGINATION_HAS_PREVIOUS,
        PAGINATION_NEXT_CURSOR,
        PAGINATION_PREVIOUS_CURSOR,
    }
)

AUDIT_FIELDS: Final[frozenset[str]] = frozenset(
    {
        AUDIT_CREATED_AT,
        AUDIT_UPDATED_AT,
        AUDIT_CREATED_BY,
        AUDIT_UPDATED_BY,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "ResponseStatus",
)
