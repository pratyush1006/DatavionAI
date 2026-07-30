"""
API views for laboratory results.
"""

from __future__ import annotations

from apps.clinical.laboratories.api.serializers import (
    LaboratoryResultDetailSerializer,
    LaboratoryResultUpdateSerializer,
)
from apps.clinical.laboratories.permissions import (
    IsLaboratoryResultUser,
)
from apps.clinical.laboratories.selectors import (
    list_laboratory_results,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Laboratories"],
)
class LaboratoryResultRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete laboratory results.
    """

    permission_classes = (IsLaboratoryResultUser,)

    lookup_field = "id"

    lookup_url_kwarg = "uuid"

    serializer_classes = {
        "GET": LaboratoryResultDetailSerializer,
        "PUT": LaboratoryResultUpdateSerializer,
        "PATCH": LaboratoryResultUpdateSerializer,
    }

    def get_queryset(
        self,
    ):
        """
        Return the queryset.
        """

        return list_laboratory_results()


__all__ = [
    "LaboratoryResultRetrieveUpdateDestroyAPIView",
]
