"""
Shared serializer field definitions for the Accounts app.
"""

from __future__ import annotations

_LIST_FIELDS = (
    "id",
    "username",
    "email",
    "first_name",
    "last_name",
    "is_active",
    "is_verified",
)

_DETAIL_FIELDS = (
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

_WRITE_FIELDS = (
    "username",
    "email",
    "first_name",
    "last_name",
    "password",
    "is_active",
)

_UPDATE_FIELDS = (
    "first_name",
    "last_name",
    "email",
    "password",
    "is_active",
)

__all__ = [
    "_DETAIL_FIELDS",
    "_LIST_FIELDS",
    "_UPDATE_FIELDS",
    "_WRITE_FIELDS",
]
