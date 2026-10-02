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
    "department_type",
    "is_active",
)


DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_name",
    "name",
    "code",
    "description",
    "department_type",
    "head",
    "phone",
    "email",
    "location",
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
    "department_type",
    "head",
    "phone",
    "email",
    "location",
    "is_active",
)


UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "name",
    "description",
    "department_type",
    "head",
    "phone",
    "email",
    "location",
    "is_active",
)


READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization_name",
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
