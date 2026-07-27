"""
Serializer field definitions for the Notes application.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "name",
    "template_type",
    "is_active",
    "is_system_template",
    "created_at",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "name",
    "template_type",
    "content",
    "is_active",
    "is_system_template",
    "created_at",
    "updated_at",
)

TEMPLATE_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "name",
    "template_type",
    "content",
    "is_active",
    "is_system_template",
)

TEMPLATE_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "name",
    "template_type",
    "content",
    "is_active",
    "is_system_template",
)

READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "created_at",
    "updated_at",
)

NOTE_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "patient",
    "encounter",
    "note_type",
    "title",
    "is_amended",
    "signed_at",
    "signed_by",
    "created_by",
    "created_at",
)

NOTE_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "patient",
    "encounter",
    "note_type",
    "title",
    "content",
    "raw_text",
    "is_amended",
    "amendment_reason",
    "original_note",
    "signed_at",
    "signed_by",
    "created_by",
    "created_at",
    "updated_at",
)

NOTE_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "patient",
    "encounter",
    "note_type",
    "title",
    "content",
    "raw_text",
    "amendment_reason",
    "created_by",
)

NOTE_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "note_type",
    "title",
    "content",
    "raw_text",
    "amendment_reason",
)

NOTE_READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "created_at",
    "updated_at",
)

__all__ = [
    "DETAIL_FIELDS",
    "LIST_FIELDS",
    "NOTE_DETAIL_FIELDS",
    "NOTE_LIST_FIELDS",
    "NOTE_READ_ONLY_FIELDS",
    "NOTE_UPDATE_FIELDS",
    "NOTE_WRITE_FIELDS",
    "READ_ONLY_FIELDS",
    "TEMPLATE_UPDATE_FIELDS",
    "TEMPLATE_WRITE_FIELDS",
]
