"""
City reference-data API.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from apps.common.api.base_generics import BaseGenericAPIView
from apps.platform.geography.api.geography.serializers import (
    CitySerializer,
)
from apps.platform.geography.selectors import get_cities

GEOGRAPHY_TAG: Final[tuple[str, ...]] = ("Geography",)


@extend_schema(
    tags=GEOGRAPHY_TAG,
    parameters=[
        OpenApiParameter(
            name="region",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Administrative region UUID.",
        ),
    ],
)
class CityListAPIView(
    BaseGenericAPIView,
):
    """
    Return active cities for an administrative region.
    """

    permission_classes = (AllowAny,)

    serializer_class = CitySerializer

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):
        region_id = request.query_params.get(
            "region",
        )

        if not region_id:
            raise ValidationError(
                {
                    "region": ("This query parameter is required."),
                },
            )

        queryset = get_cities(
            region_id=region_id,
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


__all__: tuple[str, ...] = ("CityListAPIView",)
