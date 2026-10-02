"""Validation helpers for Patient Documents."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError

PROTECTED_FIELDS = frozenset(
    {
        "id",
        "organization",
        "organization_id",
        "patient",
        "patient_id",
        "created_at",
        "updated_at",
        "created_by",
        "created_by_id",
        "is_deleted",
        "deleted_at",
        "deleted_by_id",
    }
)


def validate_document_data(
    data: Mapping[str, Any],
) -> None:
    """Validate mutable document metadata supplied to the service."""
    forbidden = PROTECTED_FIELDS.intersection(data.keys())
    if forbidden:
        raise ValidationError(
            "Protected fields cannot be modified: " + ", ".join(sorted(forbidden)),
        )

    title = data.get("title")
    if title is not None and not str(title).strip():
        raise ValidationError(
            "Document title cannot be empty.",
        )

    file_size = data.get("file_size")
    if file_size is not None and int(file_size) < 0:
        raise ValidationError(
            "File size cannot be negative.",
        )


__all__ = (
    "PROTECTED_FIELDS",
    "validate_document_data",
)
