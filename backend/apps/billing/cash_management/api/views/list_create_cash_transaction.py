"""
API views for listing and creating cash_transaction records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.cash_management.api.serializers import (
    CashTransactionCreateSerializer,
    CashTransactionDetailSerializer,
    CashTransactionListSerializer,
)
from apps.billing.cash_management.models import CashTransaction
from apps.billing.cash_management.permissions import (
    CanCreateCashManagement,
    CanViewCashManagement,
)
from apps.billing.cash_management.selectors import CashTransactionSelector
from apps.billing.cash_management.services import CashTransactionService
from apps.common.api.base_generics import BaseListCreateAPIView
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

CASHTRANSACTION_TAG: Final[tuple[str, ...]] = ("Cash Management",)


@extend_schema(tags=CASHTRANSACTION_TAG)
class CashTransactionListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating cash_transaction records.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewCashManagement,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateCashManagement,
        ),
    }

    serializer_classes = {
        "GET": CashTransactionListSerializer,
        "POST": CashTransactionCreateSerializer,
    }

    detail_serializer_class = CashTransactionDetailSerializer

    create_service = CashTransactionService.create

    create_success_message = "CashTransaction created successfully."

    search_fields = (
        "reference",
        "bank_account",
        "amount",
        "transaction_type",
        "is_active",
    )

    ordering = ("created_at",)

    ordering_fields = ("created_at",)

    filterset_fields = (
        "organization",
        "is_active",
        "transaction_type",
    )

    def get_queryset(
        self,
    ) -> QuerySet[CashTransaction]:
        """
        Return the cash_transaction queryset.
        """

        return CashTransactionSelector.queryset()


__all__ = [
    "CashTransactionListCreateAPIView",
]
