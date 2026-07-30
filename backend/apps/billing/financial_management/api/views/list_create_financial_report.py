"""
API views for listing and creating financial_report records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.financial_management.api.serializers import (
    FinancialReportCreateSerializer,
    FinancialReportDetailSerializer,
    FinancialReportListSerializer,
)
from apps.billing.financial_management.models import FinancialReport
from apps.billing.financial_management.permissions import (
    CanCreateFinancialManagement,
    CanViewFinancialManagement,
)
from apps.billing.financial_management.selectors import FinancialReportSelector
from apps.billing.financial_management.services import FinancialReportService
from apps.common.api.base_generics import BaseListCreateAPIView
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

FINANCIALREPORT_TAG: Final[tuple[str, ...]] = ("Financial Management",)


@extend_schema(tags=FINANCIALREPORT_TAG)
class FinancialReportListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating financial_report records.
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
        "GET": FinancialReportListSerializer,
        "POST": FinancialReportCreateSerializer,
    }

    detail_serializer_class = FinancialReportDetailSerializer

    create_service = FinancialReportService.create

    create_success_message = "FinancialReport created successfully."

    search_fields = (
        "title",
        "report_type",
        "status",
        "is_active",
    )

    ordering = ("created_at",)

    ordering_fields = ("created_at",)

    filterset_fields = (
        "organization",
        "is_active",
        "status",
        "report_type",
    )

    def get_queryset(
        self,
    ) -> QuerySet[FinancialReport]:
        """
        Return the financial_report queryset.
        """

        return FinancialReportSelector.queryset()


__all__ = [
    "FinancialReportListCreateAPIView",
]
