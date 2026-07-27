"""
Serializer field definitions for the General Ledger application.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "code",
    "name",
    "account_type",
    "status",
    "is_active",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "code",
    "name",
    "description",
    "account_type",
    "parent",
    "status",
    "is_active",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "code",
    "name",
    "description",
    "account_type",
    "parent",
    "status",
    "is_active",
)

UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "code",
    "name",
    "description",
    "account_type",
    "parent",
    "status",
    "is_active",
)

READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "created_at",
    "updated_at",
)

__all__ = [
    "DETAIL_FIELDS",
    "LIST_FIELDS",
    "READ_ONLY_FIELDS",
    "UPDATE_FIELDS",
    "WRITE_FIELDS",
]
