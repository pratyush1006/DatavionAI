"""
DatavionOS Search API Views.
"""

from __future__ import annotations

from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)
from apps.common.search import (
    search_service,
)

from .serializers import (
    SearchRequestSerializer,
)


class SearchAPIView(
    BaseGenericAPIView,
):
    """
    Unified enterprise search endpoint.
    """

    def post(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Execute unified search.
        """

        serializer = SearchRequestSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        result = search_service.search(
            **serializer.validated_data,
        )

        return self.success_response(
            data=result,
        )


__all__ = ("SearchAPIView",)
