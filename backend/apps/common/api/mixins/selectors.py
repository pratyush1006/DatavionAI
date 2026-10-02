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

    Applications should configure:

    - ``list_selector`` for queryset retrieval.
    - ``detail_selector`` for single-object retrieval.

    Selector functions own all read-side business logic.
    API views should remain orchestration layers only.
    """

    list_selector: Callable[..., QuerySet[Any]] | None = None

    detail_selector: Callable[..., Any] | None = None

    lookup_url_kwarg: str = "pk"

    def get_selector_kwargs(self) -> dict[str, Any]:
        """
        Return keyword arguments passed to selector functions.

        Subclasses may override this method to provide additional
        context such as the current user, organization, query
        parameters, or request-scoped data.
        """

        return {}

    def get_queryset(self) -> QuerySet[Any]:
        """
        Return the queryset using the configured selector.
        """

        if self.list_selector is None:
            raise ImproperlyConfigured("'list_selector' must be configured.")

        return self.list_selector(
            **self.get_selector_kwargs(),
        )

    def get_lookup_value(self) -> object:
        """
        Return the lookup value from the URL.
        """

        if not hasattr(self, "kwargs"):
            raise ImproperlyConfigured(
                "SelectorMixin requires 'kwargs' to be available."
            )

        return self.kwargs[self.lookup_url_kwarg]

    def get_object(self) -> Any:
        """
        Return the requested object using the configured selector.
        """

        if self.detail_selector is None:
            raise ImproperlyConfigured("'detail_selector' must be configured.")

        return self.detail_selector(
            self.get_lookup_value(),
            **self.get_selector_kwargs(),
        )


__all__ = ("SelectorMixin",)
