"""
API views for the Payment Posting module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.revenue_cycle.payment_posting.api.serializers import (
    PaymentPostingCreateSerializer,
    PaymentPostingDetailSerializer,
    PaymentPostingListSerializer,
    PaymentPostingUpdateSerializer,
)
from apps.revenue_cycle.payment_posting.models import PaymentPosting
from apps.revenue_cycle.payment_posting.permissions import (
    CanCreatePaymentPosting,
    CanDeletePaymentPosting,
    CanUpdatePaymentPosting,
    CanViewPaymentPosting,
)
from apps.revenue_cycle.payment_posting.selectors import PaymentPostingSelector
from apps.revenue_cycle.payment_posting.services import PaymentPostingService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Payment Posting",)


@extend_schema(tags=TAG)
class PaymentPostingListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPaymentPosting),
        "POST": (IsAuthenticated, CanCreatePaymentPosting),
    }

    serializer_classes = {
        "GET": PaymentPostingListSerializer,
        "POST": PaymentPostingCreateSerializer,
    }

    detail_serializer_class = PaymentPostingDetailSerializer

    create_service = PaymentPostingService.create

    create_success_message = "Payment Posting created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[PaymentPosting]:
        return PaymentPostingSelector.queryset()


@extend_schema(tags=TAG)
class PaymentPostingRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "posting_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPaymentPosting),
        "PUT": (IsAuthenticated, CanUpdatePaymentPosting),
        "PATCH": (IsAuthenticated, CanUpdatePaymentPosting),
        "DELETE": (IsAuthenticated, CanDeletePaymentPosting),
    }

    serializer_classes = {
        "GET": PaymentPostingDetailSerializer,
        "PUT": PaymentPostingUpdateSerializer,
        "PATCH": PaymentPostingUpdateSerializer,
    }

    update_service = PaymentPostingService.update
    delete_service = PaymentPostingService.delete

    def get_object(
        self,
    ) -> PaymentPosting:
        return PaymentPostingSelector.get(
            posting_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PaymentPostingListCreateAPIView",
    "PaymentPostingRetrieveUpdateDestroyAPIView",
]
