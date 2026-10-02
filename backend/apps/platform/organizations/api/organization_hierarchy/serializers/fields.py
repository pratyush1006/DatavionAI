"""
Serializer field definitions for OrganizationHierarchy.
"""

from __future__ import annotations

from typing import Final

_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "parent_organization",
    "child_organization",
    "relationship_type",
    "status",
)

_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "parent_organization",
    "child_organization",
    "relationship_type",
    "status",
    "display_order",
    "effective_from",
    "effective_to",
    "notes",
    "created_at",
    "updated_at",
)

_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "parent_organization",
    "child_organization",
    "relationship_type",
    "status",
    "display_order",
    "effective_from",
    "effective_to",
    "notes",
)

_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "parent_organization",
    "child_organization",
    "relationship_type",
    "status",
    "display_order",
    "effective_from",
    "effective_to",
    "notes",
)

_SUMMARY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "parent_organization",
    "child_organization",
    "relationship_type",
)

__all__ = [
    "_LIST_FIELDS",
    "_DETAIL_FIELDS",
    "_WRITE_FIELDS",
    "_UPDATE_FIELDS",
    "_SUMMARY_FIELDS",
]
