"""
Custom pagination classes used across the DatavionOS platform.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, ClassVar, Final

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.common.api.responses import success_response

DEFAULT_PAGE_SIZE: Final[int] = 20

MAX_PAGE_SIZE: Final[int] = 100


class DatavionPagination(
    PageNumberPagination,
):
    """
    Default enterprise pagination for DatavionOS APIs.

    Provides:

    - Standard page pagination
    - Pagination metadata
    - Query context
    - Request-aware responses
    """

    page_size: ClassVar[int] = DEFAULT_PAGE_SIZE

    page_size_query_param: ClassVar[str] = "page_size"

    max_page_size: ClassVar[int] = MAX_PAGE_SIZE

    page_query_param: ClassVar[str] = "page"

    def get_pagination_meta(
        self,
    ) -> dict[str, Any]:
        """
        Return pagination metadata.
        """

        page_size = self.get_page_size(
            self.request,
        )

        return {
            "count": self.page.paginator.count,
            "page": self.page.number,
            "page_size": (page_size or self.page_size),
            "total_pages": (self.page.paginator.num_pages),
            "next": (self.get_next_link()),
            "previous": (self.get_previous_link()),
        }

    def get_query_meta(
        self,
    ) -> dict[str, Any]:
        """
        Return active query parameters.
        """

        if not self.request:
            return {}

        params = {}

        for key in (
            "search",
            "ordering",
            "page",
            "page_size",
        ):
            value = self.request.query_params.get(
                key,
            )

            if value:
                params[key] = value

        return params

    def get_meta(
        self,
    ) -> Mapping[str, Any]:
        """
        Return response metadata.
        """

        return {
            "pagination": (self.get_pagination_meta()),
            "query": (self.get_query_meta()),
        }

    def get_paginated_response(
        self,
        data: Any,
    ) -> Response:
        """
        Return standardized paginated response.
        """

        return success_response(
            request=self.request,
            data=data,
            meta=self.get_meta(),
        )


__all__: tuple[str, ...] = ("DatavionPagination",)
