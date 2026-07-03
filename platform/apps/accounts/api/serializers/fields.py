"""
Shared serializer field definitions for the Accounts application.
"""

from __future__ import annotations

LIST_FIELDS = (
    "id",
    "username",
    "email",
    "first_name",
    "last_name",
    "is_active",
    "is_verified",
)

DETAIL_FIELDS = (
    "id",
    "username",
    "email",
    "first_name",
    "last_name",
    "is_active",
    "is_verified",
    "created_at",
    "updated_at",
)

WRITE_FIELDS = (
    "username",
    "email",
    "first_name",
    "last_name",
    "password",
    "is_active",
)

UPDATE_FIELDS = (
    "first_name",
    "last_name",
    "email",
    "password",
    "is_active",
)

__all__ = [
    "LIST_FIELDS",
    "DETAIL_FIELDS",
    "WRITE_FIELDS",
    "UPDATE_FIELDS",
]
