"""
Serializer field definitions for the Organizations application.
"""

from __future__ import annotations

from typing import Final

_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "name",
    "code",
    "organization_type",
    "city",
    "country",
    "is_active",
)

_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "name",
    "code",
    "organization_type",
    "email",
    "phone",
    "address",
    "city",
    "state",
    "country",
    "is_active",
    "created_at",
    "updated_at",
)

_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "name",
    "code",
    "organization_type",
    "email",
    "phone",
    "address",
    "city",
    "state",
    "country",
    "is_active",
)

_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "name",
    "organization_type",
    "email",
    "phone",
    "address",
    "city",
    "state",
    "country",
    "is_active",
)

__all__ = [
    "_LIST_FIELDS",
    "_DETAIL_FIELDS",
    "_WRITE_FIELDS",
    "_UPDATE_FIELDS",
]
