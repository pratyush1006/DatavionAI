"""
Custom pagination classes used across the DatavionOS platform.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.common.api.responses import JSONValue, success_response

DEFAULT_PAGE_SIZE: Final[int] = 20
MAX_PAGE_SIZE: Final[int] = 100

_QUERY_PARAMS: Final[tuple[str, ...]] = (
    "search",
    "ordering",
    "page",
    "page_size",
)


class DatavionPagination(PageNumberPagination):
    """
    Default enterprise pagination for DatavionOS APIs.

    Provides:

    - Standard page pagination
    - Pagination metadata
    - Query context
    - Request-aware responses
    """

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = MAX_PAGE_SIZE
    page_query_param = "page"

    def get_pagination_meta(self) -> dict[str, JSONValue]:
        """
        Return pagination metadata.
        """

        page = self.page
        request = self.request
        page_size = (
            self.get_page_size(request) if request is not None else self.page_size
        )

        if page is None:
            return {
                "count": 0,
                "page": 1,
                "page_size": page_size,
                "total_pages": 0,
                "next": None,
                "previous": None,
            }

        return {
            "count": page.paginator.count,
            "page": page.number,
            "page_size": page_size or self.page_size,
            "total_pages": page.paginator.num_pages,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
        }

    def get_query_meta(self) -> dict[str, str]:
        """
        Return active query parameters.
        """

        if self.request is None:
            return {}

        params: dict[str, str] = {}

        for key in _QUERY_PARAMS:
            if value := self.request.query_params.get(key):
                params[key] = value

        return params

    def get_meta(self) -> Mapping[str, JSONValue]:
        """
        Return response metadata.
        """

        return {
            "pagination": self.get_pagination_meta(),
            "query": dict(self.get_query_meta()),
        }

    def get_paginated_response(
        self,
        data: JSONValue,
    ) -> Response:
        """
        Return standardized paginated response.
        """

        return success_response(
            request=self.request,
            data=data,
            meta=self.get_meta(),
        )


__all__ = ("DatavionPagination",)
