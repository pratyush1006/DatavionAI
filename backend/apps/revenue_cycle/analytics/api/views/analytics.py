"""
API views for the RCM Metric module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.analytics.api.serializers import (
    RcmMetricCreateSerializer,
    RcmMetricDetailSerializer,
    RcmMetricListSerializer,
    RcmMetricUpdateSerializer,
)
from apps.revenue_cycle.analytics.models import RcmMetric
from apps.revenue_cycle.analytics.permissions import (
    CanCreateRcmMetric,
    CanDeleteRcmMetric,
    CanUpdateRcmMetric,
    CanViewRcmMetric,
)
from apps.revenue_cycle.analytics.selectors import RcmMetricSelector
from apps.revenue_cycle.analytics.services import RcmMetricService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Analytics",)


@extend_schema(tags=TAG)
class RcmMetricListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewRcmMetric),
        "POST": (IsAuthenticated, CanCreateRcmMetric),
    }

    serializer_classes = {
        "GET": RcmMetricListSerializer,
        "POST": RcmMetricCreateSerializer,
    }

    detail_serializer_class = RcmMetricDetailSerializer

    create_service = RcmMetricService.create

    create_success_message = "RCM Metric created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[RcmMetric]:
        return RcmMetricSelector.queryset()


@extend_schema(tags=TAG)
class RcmMetricRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "metric_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewRcmMetric),
        "PUT": (IsAuthenticated, CanUpdateRcmMetric),
        "PATCH": (IsAuthenticated, CanUpdateRcmMetric),
        "DELETE": (IsAuthenticated, CanDeleteRcmMetric),
    }

    serializer_classes = {
        "GET": RcmMetricDetailSerializer,
        "PUT": RcmMetricUpdateSerializer,
        "PATCH": RcmMetricUpdateSerializer,
    }

    update_service = RcmMetricService.update
    delete_service = RcmMetricService.delete

    def get_object(
        self,
    ) -> RcmMetric:
        return RcmMetricSelector.get(
            metric_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "RcmMetricListCreateAPIView",
    "RcmMetricRetrieveUpdateDestroyAPIView",
]
