"""
API views for laboratory results.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.laboratories.api.serializers import (
    LaboratoryResultCreateSerializer,
    LaboratoryResultListSerializer,
)
from apps.laboratories.permissions import (
    IsLaboratoryResultUser,
)
from apps.laboratories.selectors import (
    list_laboratory_results,
)
from apps.laboratories.services import (
    create_laboratory_result,
)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)


@extend_schema(
    tags=["Laboratories"],
)
class LaboratoryResultListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create laboratory results.
    """

    permission_classes = (IsLaboratoryResultUser,)

    create_service = create_laboratory_result

    serializer_classes = {
        "GET": LaboratoryResultListSerializer,
        "POST": LaboratoryResultCreateSerializer,
    }

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "laboratory_test",
        "status",
        "abnormal_flag",
        "verified_by",
    )

    search_fields = (
        "result_value_text",
        "notes",
    )

    ordering_fields = (
        "resulted_at",
        "created_at",
    )

    ordering = ("-resulted_at",)

    def get_queryset(
        self,
    ):
        """
        Return the queryset.
        """

        return list_laboratory_results()


__all__ = [
    "LaboratoryResultListCreateAPIView",
]
