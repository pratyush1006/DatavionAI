"""
DatavionOS Selector Ordering.

Reusable ordering utilities for selectors.

Supports:

- Allowlist ordering
- Multiple fields
- Stable ordering
- Cursor pagination compatibility
"""

from __future__ import annotations

from typing import TypeVar

from django.db.models import Model, QuerySet

ModelType = TypeVar(
    "ModelType",
    bound=Model,
)


class Ordering:
    """
    Generic safe ordering helper.
    """

    @staticmethod
    def normalize(
        ordering: str,
    ) -> tuple[str, ...]:
        """
        Normalize comma separated ordering.

        Example:

        "-created_at,name"

        becomes:

        (
            "-created_at",
            "name",
        )
        """

        return tuple(item.strip() for item in ordering.split(",") if item.strip())

    @staticmethod
    def is_allowed(
        field: str,
        allowed: tuple[str, ...],
    ) -> bool:
        """
        Check ordering field whitelist.
        """

        return field.lstrip("-") in allowed

    @classmethod
    def apply(
        cls,
        queryset: QuerySet[ModelType],
        *,
        ordering: str | None = None,
        allowed: tuple[str, ...] = (),
        default: tuple[str, ...] = (),
        stable_field: str | None = None,
    ) -> QuerySet[ModelType]:
        """
        Apply validated ordering.

        Parameters
        ----------

        ordering:
            Requested ordering.

            Example:

            "-created_at,name"


        allowed:
            Allowed fields.


        default:
            Default ordering.


        stable_field:
            Additional deterministic ordering.

            Example:

            uuid
        """

        fields: tuple[str, ...] = ()

        if ordering:
            requested = cls.normalize(
                ordering,
            )

            valid = tuple(
                field
                for field in requested
                if cls.is_allowed(
                    field,
                    allowed,
                )
            )

            fields = valid

        if not fields:
            fields = default

        if stable_field:
            existing = {field.lstrip("-") for field in fields}

            if stable_field not in existing:
                fields = (
                    *fields,
                    stable_field,
                )

        if not fields:
            return queryset

        return queryset.order_by(
            *fields,
        )


__all__: tuple[str, ...] = ("Ordering",)
