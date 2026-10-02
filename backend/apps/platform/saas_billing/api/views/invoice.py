"""
SaaS Billing Invoice API views.

Handles:

- Invoice listing
- Invoice details
- Invoice generation
- Invoice issuing
- Invoice finalization
- Invoice cancellation

Architecture:

API
 |
Organization Context
 |
RBAC
 |
Workflow Registry
 |
Invoice Workflow
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
    CanManageInvoice,
    CanViewInvoice,
)
from apps.platform.saas_billing.api.serializers import (
    InvoiceLifecycleSerializer,
    InvoiceSerializer,
)
from apps.platform.saas_billing.models import (
    Invoice,
    Subscription,
)
from apps.platform.saas_billing.workflows import (
    WorkflowRegistry,
)


class InvoiceListAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    List organization invoices.
    """

    permission_classes = [
        CanViewInvoice,
    ]

    def get(
        self,
        request,
    ):
        """
        Return invoices.
        """

        organization = self.get_organization(
            request,
        )

        invoices = Invoice.objects.filter(
            organization=organization,
        ).order_by(
            "-created_at",
        )

        return success_response(
            data=InvoiceSerializer(
                invoices,
                many=True,
            ).data,
        )


class InvoiceDetailAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Invoice detail.
    """

    permission_classes = [
        CanViewInvoice,
    ]

    def get(
        self,
        request,
        pk,
    ):

        invoice = Invoice.objects.filter(
            organization=self.get_organization(
                request,
            ),
            id=pk,
        ).first()

        if not invoice:
            return Response(
                {"detail": ("Invoice not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        return success_response(
            data=InvoiceSerializer(
                invoice,
            ).data,
        )


class InvoiceGenerateAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Generate invoice.
    """

    permission_classes = [
        CanManageInvoice,
    ]

    def post(
        self,
        request,
    ):

        subscription = Subscription.objects.filter(
            organization=self.get_organization(
                request,
            ),
        ).first()

        if not subscription:
            return Response(
                {"detail": ("Subscription not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        invoice = WorkflowRegistry.execute(
            "invoice.generate",
            subscription=subscription,
        )

        return success_response(
            data=InvoiceSerializer(
                invoice,
            ).data,
            status_code=status.HTTP_201_CREATED,
        )


class InvoiceIssueAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Issue invoice.
    """

    permission_classes = [
        CanManageInvoice,
    ]

    def post(
        self,
        request,
        pk,
    ):

        invoice = self._get_invoice(
            request,
            pk,
        )

        invoice = WorkflowRegistry.execute(
            "invoice.issue",
            invoice=invoice,
        )

        return success_response(
            data=InvoiceSerializer(
                invoice,
            ).data,
        )

    def _get_invoice(
        self,
        request,
        pk,
    ):

        return Invoice.objects.get(
            organization=self.get_organization(
                request,
            ),
            id=pk,
        )


class InvoiceFinalizeAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Finalize invoice.
    """

    permission_classes = [
        CanManageInvoice,
    ]

    def post(
        self,
        request,
        pk,
    ):

        invoice = Invoice.objects.get(
            organization=self.get_organization(
                request,
            ),
            id=pk,
        )

        invoice = WorkflowRegistry.execute(
            "invoice.finalize",
            invoice=invoice,
        )

        return success_response(
            data=InvoiceSerializer(
                invoice,
            ).data,
        )


class InvoiceCancelAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Cancel invoice.
    """

    permission_classes = [
        CanManageInvoice,
    ]

    def post(
        self,
        request,
        pk,
    ):

        serializer = InvoiceLifecycleSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        invoice = Invoice.objects.get(
            organization=self.get_organization(
                request,
            ),
            id=pk,
        )

        invoice.status = Invoice.Status.CANCELLED

        invoice.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return success_response(
            data=InvoiceSerializer(
                invoice,
            ).data,
        )


__all__ = (
    "InvoiceListAPIView",
    "InvoiceDetailAPIView",
    "InvoiceGenerateAPIView",
    "InvoiceIssueAPIView",
    "InvoiceFinalizeAPIView",
    "InvoiceCancelAPIView",
)
