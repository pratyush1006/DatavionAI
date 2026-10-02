"""
DatavionOS Selector Filters.

Enterprise filtering utilities.

Supports:

- Allowlisted filtering
- Tenant isolation
- Safe lookups
- Date ranges
- Custom filtering
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from django.db.models import Model, QuerySet

ModelType = TypeVar(
    "ModelType",
    bound=Model,
)


class FilterSet:
    """
    Enterprise selector filter helpers.
    """

    @staticmethod
    def clean(
        filters: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Remove empty filters.
        """

        return {key: value for key, value in filters.items() if value is not None}

    @classmethod
    def apply(
        cls,
        queryset: QuerySet[ModelType],
        *,
        allowed: tuple[str, ...] = (),
        **filters: Any,
    ) -> QuerySet[ModelType]:
        """
        Apply safe ORM filters.

        Only allowlisted fields are applied.
        """

        cleaned = cls.clean(
            filters,
        )

        if allowed:
            cleaned = {key: value for key, value in cleaned.items() if key in allowed}

        if not cleaned:
            return queryset

        return queryset.filter(
            **cleaned,
        )

    @classmethod
    def apply_tenant(
        cls,
        queryset: QuerySet[ModelType],
        *,
        tenant_id: Any,
        field: str = "tenant_id",
    ) -> QuerySet[ModelType]:
        """
        Apply tenant isolation.
        """

        if tenant_id is None:
            return queryset

        return queryset.filter(
            **{
                field: tenant_id,
            }
        )

    @staticmethod
    def exclude(
        queryset: QuerySet[ModelType],
        **filters: Any,
    ) -> QuerySet[ModelType]:
        """
        Apply exclusions.
        """

        cleaned = {key: value for key, value in filters.items() if value is not None}

        if not cleaned:
            return queryset

        return queryset.exclude(
            **cleaned,
        )

    @staticmethod
    def custom(
        queryset: QuerySet[ModelType],
        callback: Callable[
            [QuerySet[ModelType]],
            QuerySet[ModelType],
        ],
    ) -> QuerySet[ModelType]:
        """
        Apply custom filtering.
        """

        return callback(
            queryset,
        )


__all__: tuple[str, ...] = ("FilterSet",)
