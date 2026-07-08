"""
API views for laboratory tests.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.laboratories.api.serializers.laboratory_test import (
    LaboratoryTestCreateSerializer,
    LaboratoryTestListSerializer,
)
from apps.laboratories.permissions import (
    IsLaboratoryTestUser,
)
from apps.laboratories.selectors import (
    list_laboratory_tests,
)
from apps.laboratories.services import (
    create_laboratory_test,
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
class LaboratoryTestListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create laboratory tests.
    """

    permission_classes = (IsLaboratoryTestUser,)

    create_service = create_laboratory_test

    serializer_classes = {
        "GET": LaboratoryTestListSerializer,
        "POST": LaboratoryTestCreateSerializer,
    }

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "laboratory_order",
        "category",
        "priority",
        "specimen_type",
        "status",
    )

    search_fields = (
        "code",
        "name",
    )

    ordering_fields = (
        "display_order",
        "created_at",
    )

    ordering = ("display_order",)

    def get_queryset(
        self,
    ):
        """
        Return the queryset.
        """

        return list_laboratory_tests()


__all__ = [
    "LaboratoryTestListCreateAPIView",
]
