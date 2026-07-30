"""
API views for retrieving, updating, and deleting financial_report records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.financial_management.api.serializers import (
    FinancialReportDetailSerializer,
    FinancialReportUpdateSerializer,
)
from apps.billing.financial_management.models import FinancialReport
from apps.billing.financial_management.permissions import (
    CanDeleteFinancialManagement,
    CanUpdateFinancialManagement,
    CanViewFinancialManagement,
)
from apps.billing.financial_management.selectors import FinancialReportSelector
from apps.billing.financial_management.services import FinancialReportService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

Financialreport_TAG: Final[tuple[str, ...]] = ("Financial Management",)


@extend_schema(tags=Financialreport_TAG)
class FinancialReportRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a financial_report.
    """

    lookup_url_kwarg = "financial_report_id"

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

    serializer_class = FinancialReportDetailSerializer

    serializer_classes = {
        "GET": FinancialReportDetailSerializer,
        "PUT": FinancialReportUpdateSerializer,
        "PATCH": FinancialReportUpdateSerializer,
    }

    update_service = FinancialReportService.update

    delete_service = FinancialReportService.delete

    def get_object(
        self,
    ) -> FinancialReport:
        """
        Return the requested financial_report.
        """

        return FinancialReportSelector.get(
            financial_report_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "FinancialReportRetrieveUpdateDestroyAPIView",
]
