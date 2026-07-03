"""
Selector-related API mixins.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet


class SelectorMixin:
    """
    Delegate read operations to selector functions.
    """

    queryset_selector: (
        Callable[
            [],
            QuerySet[Any],
        ]
        | None
    ) = None

    lookup_selector: (
        Callable[
            [Any],
            Any,
        ]
        | None
    ) = None

    lookup_url_kwarg = "pk"

    def get_queryset(
        self,
    ) -> QuerySet[Any]:
        if self.queryset_selector is None:
            raise ImproperlyConfigured("queryset_selector must be configured.")

        return self.queryset_selector()

    def get_object(
        self,
    ) -> Any:
        if self.lookup_selector is None:
            raise ImproperlyConfigured("lookup_selector must be configured.")

        return self.lookup_selector(
            self.kwargs[self.lookup_url_kwarg],
        )
