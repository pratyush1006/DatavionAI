"""
API views for laboratory orders.
"""

from __future__ import annotations

from apps.clinical.laboratories.api.serializers.laboratory_order import (
    LaboratoryOrderDetailSerializer,
    LaboratoryOrderUpdateSerializer,
)
from apps.clinical.laboratories.permissions import (
    IsLaboratoryOrderUser,
)
from apps.clinical.laboratories.selectors import (
    list_laboratory_orders,
)
from apps.clinical.laboratories.services import (
    cancel_laboratory_order,
    update_laboratory_order,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Laboratories"],
)
class LaboratoryOrderRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete laboratory orders.
    """

    permission_classes = (IsLaboratoryOrderUser,)

    lookup_field = "id"
    lookup_url_kwarg = "uuid"

    serializer_classes = {
        "GET": LaboratoryOrderDetailSerializer,
        "PUT": LaboratoryOrderUpdateSerializer,
        "PATCH": LaboratoryOrderUpdateSerializer,
    }

    # Required by BaseRetrieveUpdateDestroyAPIView
    update_service = update_laboratory_order
    delete_service = cancel_laboratory_order

    def get_queryset(
        self,
    ):
        """
        Return the queryset.
        """

        return list_laboratory_orders()


__all__ = [
    "LaboratoryOrderRetrieveUpdateDestroyAPIView",
]
