"""
Billing Core Payment API views.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.billing.api.serializers import (
    PaymentCreateSerializer,
    PaymentListSerializer,
    PaymentSerializer,
)
from apps.billing.api.views._base import BillingAPIViewMixin
from apps.billing.permissions import CanProcessPayment, CanViewBilling
from apps.billing.selectors import PaymentSelector
from apps.billing.workflows import PaymentCreationRequest, PaymentCreationWorkflow


class PaymentListCreateAPIView(BillingAPIViewMixin, APIView):
    """List and create payments through Billing Core boundaries."""

    def get(self, request):
        """List organization-scoped payments."""
        organization = self.get_organization(request)
        CanViewBilling().has_permission(request, self)
        records = PaymentSelector.list(
            tenant_id=organization.tenant_id,
            organization_id=organization.pk,
        )
        return Response(PaymentListSerializer(records, many=True).data)

    def post(self, request):
        """Record a payment through the workflow boundary."""
        organization = self.get_organization(request)
        CanProcessPayment().has_permission(request, self)
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        invoice_id = data.pop("invoice")
        patient_id = data.pop("patient")
        data["invoice_id"] = invoice_id
        result = PaymentCreationWorkflow(
            request=PaymentCreationRequest(
                organization_id=organization.pk,
                patient_id=patient_id,
                data=data,
            ),
        ).run(context=self.workflow_context(request, "billing.payment.create"))
        return Response(
            PaymentSerializer(result.data).data, status=status.HTTP_201_CREATED
        )


class PaymentRetrieveAPIView(BillingAPIViewMixin, APIView):
    """Retrieve one organization-scoped payment."""

    def get(self, request, payment_id):
        """Return one payment."""
        organization = self.get_organization(request)
        CanViewBilling().has_permission(request, self)
        payment = PaymentSelector.get(
            tenant_id=organization.tenant_id,
            organization_id=organization.pk,
            payment_id=payment_id,
        )
        return Response(PaymentSerializer(payment).data)


class PaymentBulkCreateAPIView(BillingAPIViewMixin, APIView):
    """Create payments through the workflow boundary one aggregate at a time."""

    def post(self, request):
        """Create a batch of payments."""
        if not isinstance(request.data, list):
            return Response(
                {"detail": "Expected a list of payments."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        organization = self.get_organization(request)
        CanProcessPayment().has_permission(request, self)
        created = []
        for payload in request.data:
            serializer = PaymentCreateSerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            data = dict(serializer.validated_data)
            invoice_id = data.pop("invoice")
            patient_id = data.pop("patient")
            data["invoice_id"] = invoice_id
            result = PaymentCreationWorkflow(
                request=PaymentCreationRequest(
                    organization_id=organization.pk,
                    patient_id=patient_id,
                    data=data,
                ),
            ).run(context=self.workflow_context(request, "billing.payment.create"))
            created.append(result.data)
        return Response(
            PaymentSerializer(created, many=True).data, status=status.HTTP_201_CREATED
        )


__all__ = (
    "PaymentBulkCreateAPIView",
    "PaymentListCreateAPIView",
    "PaymentRetrieveAPIView",
)
