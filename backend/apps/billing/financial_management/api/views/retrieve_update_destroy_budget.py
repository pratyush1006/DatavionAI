"""
API views for retrieving, updating, and deleting budget records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.financial_management.api.serializers import (
    BudgetDetailSerializer,
    BudgetUpdateSerializer,
)
from apps.billing.financial_management.models import Budget
from apps.billing.financial_management.permissions import (
    CanDeleteFinancialManagement,
    CanUpdateFinancialManagement,
    CanViewFinancialManagement,
)
from apps.billing.financial_management.selectors import BudgetSelector
from apps.billing.financial_management.services import BudgetService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

Budget_TAG: Final[tuple[str, ...]] = ("Financial Management",)


@extend_schema(tags=Budget_TAG)
class BudgetRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a budget.
    """

    lookup_url_kwarg = "budget_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewFinancialManagement,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateFinancialManagement,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateFinancialManagement,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteFinancialManagement,
        ),
    }

    serializer_class = BudgetDetailSerializer

    serializer_classes = {
        "GET": BudgetDetailSerializer,
        "PUT": BudgetUpdateSerializer,
        "PATCH": BudgetUpdateSerializer,
    }

    update_service = BudgetService.update

    delete_service = BudgetService.delete

    def get_object(
        self,
    ) -> Budget:
        """
        Return the requested budget.
        """

        return BudgetSelector.get(
            budget_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "BudgetRetrieveUpdateDestroyAPIView",
]
