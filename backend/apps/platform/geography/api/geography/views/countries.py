"""
Country reference-data API.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseGenericAPIView
from apps.platform.geography.api.geography.serializers import (
    CountrySerializer,
)
from apps.platform.geography.selectors import get_countries

GEOGRAPHY_TAG: Final[tuple[str, ...]] = ("Geography",)


@extend_schema(
    tags=GEOGRAPHY_TAG,
)
class CountryListAPIView(
    BaseGenericAPIView,
):
    """
    Return active countries.

    Geography is platform-level reference data and is not tenant
    scoped.
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = CountrySerializer

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):
        queryset = get_countries()

        page = self.paginate_queryset(
            queryset,
        )

        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
            )

            return self.get_paginated_response(
                serializer.data,
            )

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return self.success_response(
            data=serializer.data,
        )


__all__: tuple[str, ...] = ("CountryListAPIView",)
