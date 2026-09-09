"""
Administrative region reference-data API.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseGenericAPIView
from apps.platform.geography.api.geography.serializers import (
    AdministrativeRegionSerializer,
)
from apps.platform.geography.selectors import get_regions

GEOGRAPHY_TAG: Final[tuple[str, ...]] = ("Geography",)


@extend_schema(
    tags=GEOGRAPHY_TAG,
    parameters=(
        OpenApiParameter(
            name="country",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Country UUID.",
        ),
    ),
)
class RegionListAPIView(
    BaseGenericAPIView,
):
    """
    Return active administrative regions for a country.
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = AdministrativeRegionSerializer

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):
        country_id = request.query_params.get(
            "country",
        )

        if not country_id:
            raise ValidationError(
                {
                    "country": ("This query parameter is required."),
                },
            )

        queryset = get_regions(
            country_id=country_id,
        )

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


__all__: tuple[str, ...] = ("RegionListAPIView",)
