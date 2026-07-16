"""
Serializer field definitions for the Teams application.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "department",
    "name",
    "code",
    "is_active",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "department",
    "name",
    "code",
    "description",
    "is_active",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "department",
    "name",
    "code",
    "description",
    "is_active",
)

UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "department",
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
