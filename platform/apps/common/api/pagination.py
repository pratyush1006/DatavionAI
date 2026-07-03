"""
Custom pagination classes used across Datavion APIs.
"""

from __future__ import annotations

from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DatavionPagination(PageNumberPagination):
    """
    Default pagination class for Datavion API endpoints.

    Features:
    - Standard page-number pagination.
    - Configurable page size.
    - Standardized response format.
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(
        self,
        data: Any,
    ) -> Response:
        """
        Return a standardized paginated response.
        """

        return Response(
            {
                "success": True,
                "message": "Data retrieved successfully.",
                "data": data,
                "meta": {
                    "pagination": {
                        "count": self.page.paginator.count,
                        "page": self.page.number,
                        "page_size": self.get_page_size(self.request),
                        "total_pages": self.page.paginator.num_pages,
                        "next": self.get_next_link(),
                        "previous": self.get_previous_link(),
                    },
                },
            }
        )


__all__ = [
    "DatavionPagination",
]
