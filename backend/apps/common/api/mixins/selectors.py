"""
Selector-related API mixins.

Provides reusable mixins for delegating read operations to
selector functions instead of embedding ORM logic inside API
views.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet


class SelectorMixin:
    """
    Delegate read operations to selector functions.

    Views should configure:

    - list_selector for queryset retrieval.
    - detail_selector for object retrieval.
    """

    list_selector: (
        Callable[
            ...,
            QuerySet[Any],
        ]
        | None
    ) = None

    detail_selector: (
        Callable[
            ...,
            Any,
        ]
        | None
    ) = None

    lookup_url_kwarg = "pk"

    def get_queryset(
        self,
    ) -> QuerySet[Any]:
        """
        Return the queryset using the configured selector.
        """

        if self.list_selector is None:
            raise ImproperlyConfigured(
                "list_selector must be configured.",
            )

        return self.list_selector()

    def get_object(
        self,
    ) -> Any:
        """
        Return the requested object using the configured selector.
        """

        if self.detail_selector is None:
            raise ImproperlyConfigured(
                "detail_selector must be configured.",
            )

        return self.detail_selector(
            self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "SelectorMixin",
]
