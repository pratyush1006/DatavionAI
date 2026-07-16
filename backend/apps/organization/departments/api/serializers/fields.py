"""
Serializer field definitions for the Departments application.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "name",
    "code",
    "is_active",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "name",
    "code",
    "description",
    "is_active",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "name",
    "code",
    "description",
    "is_active",
)

UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "name",
    "description",
    "is_active",
)

READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "created_at",
    "updated_at",
)

__all__ = [
    "LIST_FIELDS",
    "DETAIL_FIELDS",
    "WRITE_FIELDS",
    "UPDATE_FIELDS",
    "READ_ONLY_FIELDS",
]
