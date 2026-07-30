"""
Serializer field definitions for Teams.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "name",
    "code",
    "team_type",
    "status",
    "is_active",
)


DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "name",
    "code",
    "description",
    "team_type",
    "status",
    "is_active",
    "created_at",
    "updated_at",
)


WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "name",
    "code",
    "description",
    "team_type",
    "status",
    "is_active",
)


UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "name",
    "description",
    "team_type",
    "status",
    "is_active",
)


READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "created_at",
    "updated_at",
)


__all__ = (
    "LIST_FIELDS",
    "DETAIL_FIELDS",
    "WRITE_FIELDS",
    "UPDATE_FIELDS",
    "READ_ONLY_FIELDS",
)
