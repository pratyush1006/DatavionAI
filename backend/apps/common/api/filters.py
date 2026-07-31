"""
Reusable filter backends for the DatavionOS API framework.

Provides platform-standard filtering:

- Django filters
- Search
- Safe ordering

Business-specific filters belong inside
feature applications.
"""

from __future__ import annotations

from typing import Any, Final

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)

DEFAULT_ORDERING: Final[str] = "-created_at"


class DatavionFilterBackend(
    DjangoFilterBackend,
):
    """
    Standard Django filter backend.

    Feature applications define their own
    FilterSet classes.
    """


class DatavionSearchFilter(
    SearchFilter,
):
    """
    Standard search backend.

    Applications define:

        search_fields = [
            "name",
            "email",
        ]
    """


class DatavionOrderingFilter(
    OrderingFilter,
):
    """
    Secure ordering filter.

    Provides:

    - Platform default ordering
    - Safe empty handling
    - String normalization
    - DRF compatible tuple output

    Applications should explicitly define:

        ordering_fields = [
            "created_at",
            "updated_at",
        ]
    """

    ordering_param: Final[str] = "ordering"

    def get_default_ordering(
        self,
        view: Any,
    ) -> str | tuple[str, ...]:
        """
        Return platform default ordering.

        Always returns an iterable compatible
        with DRF OrderingFilter.
        """

        ordering = getattr(
            view,
            "ordering",
            None,
        )

        if not ordering:
            return (DEFAULT_ORDERING,)

        if isinstance(
            ordering,
            str,
        ):
            return (ordering,)

        return ordering

    def get_ordering(
        self,
        request,
        queryset,
        view,
    ):
        """
        Resolve requested ordering safely.

        Handles:

        - No ordering parameter
        - Empty ordering parameter
        - Comma separated ordering
        - Default fallback
        """

        params = request.query_params.get(
            self.ordering_param,
        )

        if not params:
            return self.get_default_ordering(
                view,
            )

        fields = [field.strip() for field in params.split(",") if field.strip()]

        if not fields:
            return self.get_default_ordering(
                view,
            )

        return fields


__all__: Final[tuple[str, ...]] = (
    "DatavionFilterBackend",
    "DatavionOrderingFilter",
    "DatavionSearchFilter",
)
