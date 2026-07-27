"""
API views for payslips.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.hr.payroll.api.serializers import (
    PayslipCreateSerializer,
    PayslipDetailSerializer,
    PayslipListSerializer,
    PayslipUpdateSerializer,
)
from apps.hr.payroll.models import Payslip
from apps.hr.payroll.permissions import (
    CanCreatePayslip,
    CanDeletePayslip,
    CanUpdatePayslip,
    CanViewPayslip,
)
from apps.hr.payroll.selectors import get_payslip_by_id, get_payslips
from apps.hr.payroll.services import (
    create_payslip,
    delete_payslip,
    update_payslip,
)

PAYROLL_TAG: Final[tuple[str, ...]] = ("Payroll",)


@extend_schema(tags=PAYROLL_TAG)
class PayslipListCreateAPIView(BaseListCreateAPIView):
    """
    List existing payslips or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPayslip),
        "POST": (IsAuthenticated, CanCreatePayslip),
    }

    serializer_classes = {
        "GET": PayslipListSerializer,
        "POST": PayslipCreateSerializer,
    }

    detail_serializer_class = PayslipDetailSerializer

    create_service = create_payslip

    create_success_message = "Payslip created successfully."

    search_fields = ("employee__employee_code",)

    ordering = ("-pay_period_start",)

    ordering_fields = ("pay_period_start", "created_at")

    filterset_fields = ("organization", "employee", "status")

    def get_queryset(self) -> QuerySet[Payslip]:
        return get_payslips()


@extend_schema(tags=PAYROLL_TAG)
class PayslipRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a payslip.
    """

    lookup_url_kwarg = "payslip_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPayslip),
        "PUT": (IsAuthenticated, CanUpdatePayslip),
        "PATCH": (IsAuthenticated, CanUpdatePayslip),
        "DELETE": (IsAuthenticated, CanDeletePayslip),
    }

    serializer_classes = {
        "GET": PayslipDetailSerializer,
        "PUT": PayslipUpdateSerializer,
        "PATCH": PayslipUpdateSerializer,
    }

    detail_serializer_class = PayslipDetailSerializer

    update_service = update_payslip

    delete_service = delete_payslip

    update_success_message = "Payslip updated successfully."

    def get_object(self):
        return get_payslip_by_id(
            payslip_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PayslipListCreateAPIView",
    "PayslipRetrieveUpdateDestroyAPIView",
]
