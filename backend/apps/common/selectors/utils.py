"""
DatavionAI Selector Utilities.

Reusable utilities for selector implementations.

Design Principles
-----------------
- Pure functions
- Framework independent where practical
- QuerySet oriented
- Type-safe
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, TypeVar

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model, QuerySet

ModelType = TypeVar(
    "ModelType",
    bound=Model,
)


def normalize_ordering(
    ordering: str | None,
) -> str | None:
    """
    Normalize an ordering field.

    Removes surrounding whitespace while preserving
    the leading '-' used for descending order.
    """

    if ordering is None:
        return None

    ordering = ordering.strip()

    return ordering or None


def is_valid_field[ModelType: Model](
    model: type[ModelType],
    field: str,
) -> bool:
    """
    Return True if the model contains the field.
    """

    try:
        model._meta.get_field(field)
        return True

    except FieldDoesNotExist:
        return False


def validate_fields[ModelType: Model](
    model: type[ModelType],
    fields: Iterable[str],
) -> tuple[str, ...]:
    """
    Return only valid model fields.
    """

    return tuple(
        field
        for field in fields
        if is_valid_field(
            model,
            field,
        )
    )


def apply_select_related[ModelType: Model](
    queryset: QuerySet[ModelType],
    *fields: str,
) -> QuerySet[ModelType]:
    """
    Apply select_related if fields are provided.
    """

    if not fields:
        return queryset

    return queryset.select_related(
        *fields,
    )


def apply_prefetch_related[ModelType: Model](
    queryset: QuerySet[ModelType],
    *fields: str,
) -> QuerySet[ModelType]:
    """
    Apply prefetch_related if fields are provided.
    """

    if not fields:
        return queryset

    return queryset.prefetch_related(
        *fields,
    )


def apply_only[ModelType: Model](
    queryset: QuerySet[ModelType],
    *fields: str,
) -> QuerySet[ModelType]:
    """
    Restrict selected fields.
    """

    if not fields:
        return queryset

    return queryset.only(
        *fields,
    )


def apply_defer[ModelType: Model](
    queryset: QuerySet[ModelType],
    *fields: str,
) -> QuerySet[ModelType]:
    """
    Defer selected fields.
    """

    if not fields:
        return queryset

    return queryset.defer(
        *fields,
    )


def queryset_metadata[ModelType: Model](
    queryset: QuerySet[ModelType],
) -> dict[str, Any]:
    """
    Return basic queryset metadata.
    """

    return {
        "model": queryset.model.__name__,
        "ordered": queryset.ordered,
        "db": queryset.db,
    }


__all__ = (
    "apply_defer",
    "apply_only",
    "apply_prefetch_related",
    "apply_select_related",
    "is_valid_field",
    "normalize_ordering",
    "queryset_metadata",
    "validate_fields",
)
