"""
API views for the Billing Batch module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.billing.api.serializers import (
    BillingBatchCreateSerializer,
    BillingBatchDetailSerializer,
    BillingBatchListSerializer,
    BillingBatchUpdateSerializer,
)
from apps.revenue_cycle.billing.models import BillingBatch
from apps.revenue_cycle.billing.permissions import (
    CanCreateBillingBatch,
    CanDeleteBillingBatch,
    CanUpdateBillingBatch,
    CanViewBillingBatch,
)
from apps.revenue_cycle.billing.selectors import BillingBatchSelector
from apps.revenue_cycle.billing.services import BillingBatchService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Billing",)


@extend_schema(tags=TAG)
class BillingBatchListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewBillingBatch),
        "POST": (IsAuthenticated, CanCreateBillingBatch),
    }

    serializer_classes = {
        "GET": BillingBatchListSerializer,
        "POST": BillingBatchCreateSerializer,
    }

    detail_serializer_class = BillingBatchDetailSerializer

    create_service = BillingBatchService.create

    create_success_message = "Billing Batch created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[BillingBatch]:
        return BillingBatchSelector.queryset()


@extend_schema(tags=TAG)
class BillingBatchRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "batch_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewBillingBatch),
        "PUT": (IsAuthenticated, CanUpdateBillingBatch),
        "PATCH": (IsAuthenticated, CanUpdateBillingBatch),
        "DELETE": (IsAuthenticated, CanDeleteBillingBatch),
    }

    serializer_classes = {
        "GET": BillingBatchDetailSerializer,
        "PUT": BillingBatchUpdateSerializer,
        "PATCH": BillingBatchUpdateSerializer,
    }

    update_service = BillingBatchService.update
    delete_service = BillingBatchService.delete

    def get_object(
        self,
    ) -> BillingBatch:
        return BillingBatchSelector.get(
            batch_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "BillingBatchListCreateAPIView",
    "BillingBatchRetrieveUpdateDestroyAPIView",
]
