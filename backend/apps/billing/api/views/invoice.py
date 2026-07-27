"""
API views for invoices.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.billing.api.serializers import (
    InvoiceCreateSerializer,
    InvoiceDetailSerializer,
    InvoiceListSerializer,
    InvoiceUpdateSerializer,
)
from apps.billing.models import Invoice
from apps.billing.permissions import (
    CanCreateInvoice,
    CanDeleteInvoice,
    CanUpdateInvoice,
    CanViewInvoice,
    CanVoidInvoice,
)
from apps.billing.selectors import InvoiceSelector
from apps.billing.services import InvoiceService
from apps.common.api.responses import (
    error_response,
    success_response,
)
from apps.common.permissions import IsAuthenticatedAndActive

INVOICE_TAG: Final[tuple[str, ...]] = ("Invoices",)


@extend_schema(tags=INVOICE_TAG)
class InvoiceListCreateAPIView(APIView):
    """
    API view for listing and creating invoices.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    def get_permissions(
        self,
    ):
        """
        Return permissions for the current request.
        """

        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                CanCreateInvoice(),
            ]

        return [
            IsAuthenticated(),
            CanViewInvoice(),
        ]

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        List invoices.
        """

        queryset = InvoiceSelector.queryset()

        page = self.paginate_queryset(
            queryset,
        )

        if page is not None:
            serializer = InvoiceListSerializer(
                page,
                many=True,
            )

            return self.get_paginated_response(
                serializer.data,
            )

        serializer = InvoiceListSerializer(
            queryset,
            many=True,
        )

        return success_response(
            data=serializer.data,
        )

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create an invoice.
        """

        serializer = InvoiceCreateSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        items = serializer.validated_data.pop(
            "items",
            None,
        )

        invoice = InvoiceService.create(
            validated_data=serializer.validated_data,
            items=items,
        )

        response_serializer = InvoiceDetailSerializer(
            invoice,
        )

        return success_response(
            message="Invoice created successfully.",
            data=response_serializer.data,
            status_code=201,
        )


@extend_schema(tags=INVOICE_TAG)
class InvoiceRetrieveUpdateDestroyAPIView(APIView):
    """
    Retrieve, update, or delete an invoice.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    def get_permissions(
        self,
    ):
        """
        Return permissions for the current request.
        """

        method = self.request.method

        if method == "GET":
            return [
                IsAuthenticated(),
                CanViewInvoice(),
            ]

        if method in ("PUT", "PATCH"):
            return [
                IsAuthenticated(),
                CanUpdateInvoice(),
            ]

        if method == "DELETE":
            return [
                IsAuthenticated(),
                CanDeleteInvoice(),
            ]

        return super().get_permissions()

    def get_object(
        self,
        invoice_id: str,
    ) -> Invoice:
        """
        Return the requested invoice.
        """

        return InvoiceSelector.get(
            invoice_id=invoice_id,
        )

    def get(
        self,
        request: Request,
        invoice_id: str,
    ) -> Response:
        """
        Retrieve an invoice.
        """

        invoice = self.get_object(
            invoice_id=invoice_id,
        )

        serializer = InvoiceDetailSerializer(
            invoice,
        )

        return success_response(
            data=serializer.data,
        )

    def put(
        self,
        request: Request,
        invoice_id: str,
    ) -> Response:
        """
        Update an invoice.
        """

        invoice = self.get_object(
            invoice_id=invoice_id,
        )

        serializer = InvoiceUpdateSerializer(
            instance=invoice,
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        updated_invoice = InvoiceService.update(
            instance=invoice,
            validated_data=serializer.validated_data,
        )

        response_serializer = InvoiceDetailSerializer(
            updated_invoice,
        )

        return success_response(
            message="Invoice updated successfully.",
            data=response_serializer.data,
        )

    def patch(
        self,
        request: Request,
        invoice_id: str,
    ) -> Response:
        """
        Partially update an invoice.
        """

        invoice = self.get_object(
            invoice_id=invoice_id,
        )

        serializer = InvoiceUpdateSerializer(
            instance=invoice,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        updated_invoice = InvoiceService.update(
            instance=invoice,
            validated_data=serializer.validated_data,
        )

        response_serializer = InvoiceDetailSerializer(
            updated_invoice,
        )

        return success_response(
            message="Invoice updated successfully.",
            data=response_serializer.data,
        )

    def delete(
        self,
        request: Request,
        invoice_id: str,
    ) -> Response:
        """
        Delete an invoice.
        """

        invoice = self.get_object(
            invoice_id=invoice_id,
        )

        invoice.delete()

        return success_response(
            message="Invoice deleted successfully.",
        )


@extend_schema(tags=INVOICE_TAG)
class InvoiceVoidAPIView(APIView):
    """
    Void an invoice.
    """

    permission_classes = (IsAuthenticated, CanVoidInvoice)

    def post(
        self,
        request: Request,
        invoice_id: str,
    ) -> Response:
        """
        Void an invoice.
        """

        invoice = InvoiceSelector.get(
            invoice_id=invoice_id,
        )

        voided_invoice = InvoiceService.void(
            instance=invoice,
            performed_by=request.user,
        )

        serializer = InvoiceDetailSerializer(
            voided_invoice,
        )

        return success_response(
            message="Invoice voided successfully.",
            data=serializer.data,
        )


@extend_schema(tags=INVOICE_TAG)
class InvoiceBulkCreateAPIView(APIView):
    """
    Bulk create invoices.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create multiple invoices.
        """

        if not isinstance(request.data, list):
            return error_response(
                message="Expected a list of invoices.",
                status_code=400,
            )

        serializer = InvoiceCreateSerializer(
            data=request.data,
            many=True,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        validated_data_list = []

        for item in serializer.validated_data:
            items = item.pop("items", None)
            validated_data_list.append(
                {
                    **item,
                    "items": items,
                }
            )

        invoices = InvoiceService.bulk_create(
            validated_data_list=validated_data_list,
            performed_by=request.user,
        )

        response_serializer = InvoiceDetailSerializer(
            invoices,
            many=True,
        )

        return success_response(
            message="Invoices created successfully.",
            data=response_serializer.data,
            status_code=201,
        )


__all__ = [
    "InvoiceBulkCreateAPIView",
    "InvoiceListCreateAPIView",
    "InvoiceRetrieveUpdateDestroyAPIView",
    "InvoiceVoidAPIView",
]
