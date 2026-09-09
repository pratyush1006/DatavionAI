"""
Billing Core Invoice API views.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.billing.api.serializers import (
    InvoiceCreateSerializer,
    InvoiceDetailSerializer,
    InvoiceListSerializer,
    InvoiceUpdateSerializer,
)
from apps.billing.api.views._base import BillingAPIViewMixin
from apps.billing.permissions import (
    CanCreateInvoice,
    CanDeleteInvoice,
    CanUpdateInvoice,
    CanViewBilling,
)
from apps.billing.selectors import InvoiceSelector
from apps.billing.workflows import (
    InvoiceCreationRequest,
    InvoiceCreationWorkflow,
    InvoiceDeleteWorkflow,
    InvoiceMutationRequest,
    InvoiceUpdateWorkflow,
)


class InvoiceListCreateAPIView(BillingAPIViewMixin, APIView):
    """List and create organization-scoped invoices."""

    def get(self, request):
        """List invoices through a tenant-scoped selector."""
        organization = self.get_organization(request)
        CanViewBilling().has_permission(request, self)
        records = InvoiceSelector.list(
            tenant_id=organization.tenant_id,
            organization_id=organization.pk,
        )
        return Response(InvoiceListSerializer(records, many=True).data)

    def post(self, request):
        """Create an invoice through the workflow boundary."""
        organization = self.get_organization(request)
        CanCreateInvoice().has_permission(request, self)
        serializer = InvoiceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        patient_id = data.pop("patient")
        items = data.pop("items", [])
        result = InvoiceCreationWorkflow(
            request=InvoiceCreationRequest(
                organization_id=organization.pk,
                patient_id=patient_id,
                data=data,
                items=items,
            ),
        ).run(context=self.workflow_context(request, "billing.invoice.create"))
        return Response(
            InvoiceDetailSerializer(result.data).data, status=status.HTTP_201_CREATED
        )


class InvoiceRetrieveUpdateDestroyAPIView(BillingAPIViewMixin, APIView):
    """Retrieve, update, or delete an invoice through workflow boundaries."""

    def get(self, request, invoice_id):
        """Retrieve one organization-scoped invoice."""
        organization = self.get_organization(request)
        CanViewBilling().has_permission(request, self)
        invoice = InvoiceSelector.get(
            tenant_id=organization.tenant_id,
            organization_id=organization.pk,
            invoice_id=invoice_id,
        )
        return Response(InvoiceDetailSerializer(invoice).data)

    def patch(self, request, invoice_id):
        """Update an invoice through the workflow boundary."""
        organization = self.get_organization(request)
        CanUpdateInvoice().has_permission(request, self)
        serializer = InvoiceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = InvoiceUpdateWorkflow(
            request=InvoiceMutationRequest(
                organization_id=organization.pk,
                invoice_id=invoice_id,
                data=serializer.validated_data,
            ),
        ).run(context=self.workflow_context(request, "billing.invoice.update"))
        return Response(InvoiceDetailSerializer(result.data).data)

    def delete(self, request, invoice_id):
        """Soft-delete an invoice through the workflow boundary."""
        organization = self.get_organization(request)
        CanDeleteInvoice().has_permission(request, self)
        result = InvoiceDeleteWorkflow(
            request=InvoiceMutationRequest(
                organization_id=organization.pk,
                invoice_id=invoice_id,
            ),
        ).run(context=self.workflow_context(request, "billing.invoice.delete"))
        return Response(InvoiceDetailSerializer(result.data).data)


__all__ = (
    "InvoiceListCreateAPIView",
    "InvoiceRetrieveUpdateDestroyAPIView",
)
