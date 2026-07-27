"""
API views for listing and creating bank_account records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.cash_management.api.serializers import (
    BankAccountCreateSerializer,
    BankAccountDetailSerializer,
    BankAccountListSerializer,
)
from apps.billing.cash_management.models import BankAccount
from apps.billing.cash_management.permissions import (
    CanCreateCashManagement,
    CanViewCashManagement,
)
from apps.billing.cash_management.selectors import BankAccountSelector
from apps.billing.cash_management.services import BankAccountService
from apps.common.api.base_generics import BaseListCreateAPIView
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

BANKACCOUNT_TAG: Final[tuple[str, ...]] = ("Cash Management",)


@extend_schema(tags=BANKACCOUNT_TAG)
class BankAccountListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating bank_account records.
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
        "GET": BankAccountListSerializer,
        "POST": BankAccountCreateSerializer,
    }

    detail_serializer_class = BankAccountDetailSerializer

    create_service = BankAccountService.create

    create_success_message = "BankAccount created successfully."

    search_fields = (
        "name",
        "bank_name",
        "currency",
        "is_active",
    )

    ordering = ("created_at",)

    ordering_fields = ("created_at",)

    filterset_fields = (
        "organization",
        "is_active",
        "currency",
    )

    def get_queryset(
        self,
    ) -> QuerySet[BankAccount]:
        """
        Return the bank_account queryset.
        """

        return BankAccountSelector.queryset()


__all__ = [
    "BankAccountListCreateAPIView",
]
