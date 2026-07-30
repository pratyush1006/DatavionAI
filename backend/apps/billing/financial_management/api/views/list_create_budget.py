"""
API views for listing and creating budget records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.financial_management.api.serializers import (
    BudgetCreateSerializer,
    BudgetDetailSerializer,
    BudgetListSerializer,
)
from apps.billing.financial_management.models import Budget
from apps.billing.financial_management.permissions import (
    CanCreateFinancialManagement,
    CanViewFinancialManagement,
)
from apps.billing.financial_management.selectors import BudgetSelector
from apps.billing.financial_management.services import BudgetService
from apps.common.api.base_generics import BaseListCreateAPIView
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

BUDGET_TAG: Final[tuple[str, ...]] = ("Financial Management",)


@extend_schema(tags=BUDGET_TAG)
class BudgetListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating budget records.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewFinancialManagement,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateFinancialManagement,
        ),
    }

    serializer_classes = {
        "GET": BudgetListSerializer,
        "POST": BudgetCreateSerializer,
    }

    detail_serializer_class = BudgetDetailSerializer

    create_service = BudgetService.create

    create_success_message = "Budget created successfully."

    search_fields = (
        "name",
        "fiscal_year",
        "status",
        "is_active",
    )

    ordering = ("created_at",)

    ordering_fields = ("created_at",)

    filterset_fields = (
        "organization",
        "is_active",
        "status",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Budget]:
        """
        Return the budget queryset.
        """

        return BudgetSelector.queryset()


__all__ = [
    "BudgetListCreateAPIView",
]
