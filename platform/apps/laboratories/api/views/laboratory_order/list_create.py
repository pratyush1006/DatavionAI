"""
API views for laboratory orders.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.laboratories.api.serializers.laboratory_order import (
    LaboratoryOrderCreateSerializer,
    LaboratoryOrderListSerializer,
)
from apps.laboratories.permissions import (
    IsLaboratoryOrderUser,
)
from apps.laboratories.selectors import (
    list_laboratory_orders,
)
from apps.laboratories.services import (
    create_laboratory_order,
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
class LaboratoryOrderListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create laboratory orders.
    """

    permission_classes = (IsLaboratoryOrderUser,)

    create_service = create_laboratory_order

    serializer_classes = {
        "GET": LaboratoryOrderListSerializer,
        "POST": LaboratoryOrderCreateSerializer,
    }

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "organization",
        "patient",
        "provider",
        "encounter",
        "priority",
        "status",
    )

    search_fields = (
        "order_number",
        "patient__full_name",
        "provider__full_name",
    )

    ordering_fields = (
        "ordered_at",
        "created_at",
    )

    ordering = ("-ordered_at",)

    def get_queryset(
        self,
    ):
        """
        Return the queryset.
        """

        return list_laboratory_orders()


__all__ = [
    "LaboratoryOrderListCreateAPIView",
]
