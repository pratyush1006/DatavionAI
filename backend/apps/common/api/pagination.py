"""
Custom pagination classes used across Datavion APIs.
"""

from __future__ import annotations

from typing import Final

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

SUCCESS_MESSAGE: Final = "Success."


class DatavionPagination(
    PageNumberPagination,
):
    """
    Default pagination class for Datavion APIs.
    """

    page_size = 20

    page_size_query_param = "page_size"

    max_page_size = 100

    page_query_param = "page"

    def get_pagination_meta(
        self,
    ) -> dict[str, object]:
        """
        Return pagination metadata.
        """

        return {
            "count": self.page.paginator.count,
            "page": self.page.number,
            "page_size": self.get_page_size(
                self.request,
            ),
            "total_pages": self.page.paginator.num_pages,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
        }

    def get_meta(
        self,
    ) -> dict[str, object]:
        """
        Return response metadata.
        """

        return {
            "pagination": self.get_pagination_meta(),
        }

    def get_paginated_response(
        self,
        data: object,
    ) -> Response:
        """
        Return a standardized paginated response.
        """

        return Response(
            {
                "success": True,
                "message": SUCCESS_MESSAGE,
                "data": data,
                "meta": self.get_meta(),
            }
        )


__all__ = [
    "DatavionPagination",
]
