"""
Workflow API views for payslips.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hr.payroll.permissions import (
    CanProcessPayslip,
    CanReleasePayslip,
)
from apps.hr.payroll.selectors import get_payslip_by_id
from apps.hr.payroll.services import (
    mark_payslip_paid,
    mark_payslip_processed,
)

PAYROLL_TAG: Final[tuple[str, ...]] = ("Payroll",)


class BasePayslipWorkflowAPIView(APIView):
    """
    Base workflow API view for payslips.
    """

    def get_object(self, payslip_id):
        """
        Return the payslip.
        """

        return get_payslip_by_id(payslip_id=payslip_id)


@extend_schema(tags=PAYROLL_TAG)
class PayslipProcessAPIView(BasePayslipWorkflowAPIView):
    """
    Mark a draft payslip as processed.
    """

    permission_classes = (IsAuthenticated, CanProcessPayslip)

    def post(self, request: Request, payslip_id) -> Response:
        instance = self.get_object(payslip_id)

        instance = mark_payslip_processed(instance=instance)

        return Response(
            {"success": True, "status": instance.status},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=PAYROLL_TAG)
class PayslipMarkPaidAPIView(BasePayslipWorkflowAPIView):
    """
    Mark a processed payslip as paid.
    """

    permission_classes = (IsAuthenticated, CanReleasePayslip)

    def post(self, request: Request, payslip_id) -> Response:
        instance = self.get_object(payslip_id)

        instance = mark_payslip_paid(instance=instance)

        return Response(
            {"success": True, "status": instance.status},
            status=status.HTTP_200_OK,
        )


__all__ = [
    "PayslipProcessAPIView",
    "PayslipMarkPaidAPIView",
]
