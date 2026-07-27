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

from typing import Final

from django_filters.rest_framework import (
    DjangoFilterBackend,
)
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

    Feature applications define
    their own FilterSet classes.
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
    Secure ordering backend.

    Prevents accidental exposure
    of unrestricted ordering fields.
    """

    ordering_param = "ordering"

    def get_default_ordering(
        self,
        view,
    ):
        """
        Return platform default ordering.
        """

        return getattr(
            view,
            "ordering",
            DEFAULT_ORDERING,
        )


__all__: tuple[str, ...] = (
    "DatavionFilterBackend",
    "DatavionOrderingFilter",
    "DatavionSearchFilter",
)
