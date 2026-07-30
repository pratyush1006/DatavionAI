"""
SaaS Billing Payment API views.

Handles:

- Payment listing
- Payment details
- Payment processing
- Gateway reconciliation
- Refund operations

Architecture:

API
 |
Organization Context
 |
RBAC
 |
Serializer
 |
Workflow Registry
 |
Payment Workflow
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import (
    success_response,
)
from apps.platform.saas_billing.api.mixins import (
    OrganizationContextMixin,
)
from apps.platform.saas_billing.api.permissions import (
    CanManagePayment,
    CanViewPayment,
)
from apps.platform.saas_billing.api.serializers import (
    PaymentCreateSerializer,
    PaymentReconcileSerializer,
    PaymentRefundSerializer,
    PaymentSerializer,
)
from apps.platform.saas_billing.models import (
    Invoice,
    Payment,
)
from apps.platform.saas_billing.workflows import (
    WorkflowRegistry,
)


class PaymentListAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    List organization payments.

    GET /billing/payments/
    """

    permission_classes = [
        CanViewPayment,
    ]

    def get(
        self,
        request,
    ):
        """
        Return payments.
        """

        payments = Payment.objects.filter(
            organization=self.get_organization(
                request,
            ),
        ).order_by(
            "-created_at",
        )

        return success_response(
            data=PaymentSerializer(
                payments,
                many=True,
            ).data,
        )


class PaymentDetailAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Payment details.

    GET /billing/payments/<id>/
    """

    permission_classes = [
        CanViewPayment,
    ]

    def get(
        self,
        request,
        pk,
    ):

        payment = Payment.objects.filter(
            organization=self.get_organization(
                request,
            ),
            id=pk,
        ).first()

        if not payment:
            return Response(
                {"detail": ("Payment not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        return success_response(
            data=PaymentSerializer(
                payment,
            ).data,
        )


class PaymentProcessAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Process invoice payment.

    POST /billing/payments/process/
    """

    permission_classes = [
        CanManagePayment,
    ]

    def post(
        self,
        request,
    ):

        serializer = PaymentCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        invoice_id = request.data.get(
            "invoice_id",
        )

        invoice = Invoice.objects.filter(
            organization=self.get_organization(
                request,
            ),
            id=invoice_id,
        ).first()

        if not invoice:
            return Response(
                {"detail": ("Invoice not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        payment = WorkflowRegistry.execute(
            "payment.process",
            invoice=invoice,
            provider=(
                serializer.validated_data.get(
                    "provider",
                )
            ),
            transaction_id=(
                serializer.validated_data.get(
                    "transaction_id",
                )
            ),
        )

        return success_response(
            data=PaymentSerializer(
                payment,
            ).data,
            status_code=status.HTTP_201_CREATED,
        )


class PaymentReconcileAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Reconcile gateway payment.

    POST /billing/payments/<id>/reconcile/
    """

    permission_classes = [
        CanManagePayment,
    ]

    def post(
        self,
        request,
        pk,
    ):

        serializer = PaymentReconcileSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        payment = Payment.objects.filter(
            organization=self.get_organization(
                request,
            ),
            id=pk,
        ).first()

        if not payment:
            return Response(
                {"detail": ("Payment not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        payment = WorkflowRegistry.execute(
            "payment.reconcile",
            payment=payment,
            gateway_response=(serializer.validated_data["gateway_response"]),
            success=(serializer.validated_data["success"]),
        )

        return success_response(
            data=PaymentSerializer(
                payment,
            ).data,
        )


class PaymentRefundAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Refund payment.

    POST /billing/payments/<id>/refund/
    """

    permission_classes = [
        CanManagePayment,
    ]

    def post(
        self,
        request,
        pk,
    ):

        serializer = PaymentRefundSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        payment = Payment.objects.filter(
            organization=self.get_organization(
                request,
            ),
            id=pk,
        ).first()

        if not payment:
            return Response(
                {"detail": ("Payment not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        payment = WorkflowRegistry.execute(
            "payment.refund",
            payment=payment,
            refund_amount=(
                serializer.validated_data.get(
                    "refund_amount",
                )
            ),
        )

        return success_response(
            data=PaymentSerializer(
                payment,
            ).data,
        )


__all__ = (
    "PaymentListAPIView",
    "PaymentDetailAPIView",
    "PaymentProcessAPIView",
    "PaymentReconcileAPIView",
    "PaymentRefundAPIView",
)
