"""
Shared type aliases for the Datavion AI platform.

This package provides reusable type aliases used throughout the
platform to improve readability, consistency, and static type
checking.
"""

from __future__ import annotations

# ============================================================================
# Generic Aliases
# ============================================================================
from .aliases import (
    DEFAULT_ENCODING,
    AnyDict,
    AnyList,
    AnyTuple,
    Headers,
    ImmutableMapping,
    MutableStringMapping,
    StringDict,
    StringList,
    StringSequence,
)

# ============================================================================
# Domain Identifiers
# ============================================================================
from .identifiers import (
    BranchID,
    DepartmentID,
    FacilityID,
    Identifier,
    OrganizationID,
    PatientID,
    PermissionID,
    ResourceID,
    RoleID,
    SubscriptionID,
    TenantID,
    UserID,
)

# ============================================================================
# JSON Types
# ============================================================================
from .json import (
    JSONArray,
    JSONObject,
    JSONPrimitive,
    JSONValue,
)

# ============================================================================
# Pagination Types
# ============================================================================
from .pagination import (
    Cursor,
    Limit,
    Offset,
    PageNumber,
    PageSize,
    PaginatedResponse,
    PaginationParams,
)

__all__ = [
    # Generic
    "AnyDict",
    "AnyList",
    "AnyTuple",
    "DEFAULT_ENCODING",
    "Headers",
    "ImmutableMapping",
    "MutableStringMapping",
    "StringDict",
    "StringList",
    "StringSequence",
    # Identifiers
    "BranchID",
    "DepartmentID",
    "FacilityID",
    "Identifier",
    "OrganizationID",
    "PatientID",
    "PermissionID",
    "ResourceID",
    "RoleID",
    "SubscriptionID",
    "TenantID",
    "UserID",
    # JSON
    "JSONArray",
    "JSONObject",
    "JSONPrimitive",
    "JSONValue",
    # Pagination
    "Cursor",
    "Limit",
    "Offset",
    "PageNumber",
    "PageSize",
    "PaginatedResponse",
    "PaginationParams",
]
