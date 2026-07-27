"""
API views for the Remittance Advice module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.era.api.serializers import (
    RemittanceAdviceCreateSerializer,
    RemittanceAdviceDetailSerializer,
    RemittanceAdviceListSerializer,
    RemittanceAdviceUpdateSerializer,
)
from apps.revenue_cycle.era.models import RemittanceAdvice
from apps.revenue_cycle.era.permissions import (
    CanCreateRemittanceAdvice,
    CanDeleteRemittanceAdvice,
    CanUpdateRemittanceAdvice,
    CanViewRemittanceAdvice,
)
from apps.revenue_cycle.era.selectors import RemittanceAdviceSelector
from apps.revenue_cycle.era.services import RemittanceAdviceService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("ERA",)


@extend_schema(tags=TAG)
class RemittanceAdviceListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewRemittanceAdvice),
        "POST": (IsAuthenticated, CanCreateRemittanceAdvice),
    }

    serializer_classes = {
        "GET": RemittanceAdviceListSerializer,
        "POST": RemittanceAdviceCreateSerializer,
    }

    detail_serializer_class = RemittanceAdviceDetailSerializer

    create_service = RemittanceAdviceService.create

    create_success_message = "Remittance Advice created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[RemittanceAdvice]:
        return RemittanceAdviceSelector.queryset()


@extend_schema(tags=TAG)
class RemittanceAdviceRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "remittance_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewRemittanceAdvice),
        "PUT": (IsAuthenticated, CanUpdateRemittanceAdvice),
        "PATCH": (IsAuthenticated, CanUpdateRemittanceAdvice),
        "DELETE": (IsAuthenticated, CanDeleteRemittanceAdvice),
    }

    serializer_classes = {
        "GET": RemittanceAdviceDetailSerializer,
        "PUT": RemittanceAdviceUpdateSerializer,
        "PATCH": RemittanceAdviceUpdateSerializer,
    }

    update_service = RemittanceAdviceService.update
    delete_service = RemittanceAdviceService.delete

    def get_object(
        self,
    ) -> RemittanceAdvice:
        return RemittanceAdviceSelector.get(
            remittance_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "RemittanceAdviceListCreateAPIView",
    "RemittanceAdviceRetrieveUpdateDestroyAPIView",
]
