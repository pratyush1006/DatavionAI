"""
API views for payments.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.billing.api.serializers import (
    PaymentCreateSerializer,
    PaymentListSerializer,
    PaymentSerializer,
)
from apps.billing.permissions import CanProcessPayment, CanViewInvoice
from apps.billing.selectors import PaymentSelector
from apps.billing.services import PaymentService
from apps.common.api.responses import (
    error_response,
    success_response,
)
from apps.common.permissions import IsAuthenticatedAndActive

PAYMENT_TAG: Final[tuple[str, ...]] = ("Payments",)


@extend_schema(tags=PAYMENT_TAG)
class PaymentListCreateAPIView(APIView):
    """
    API view for listing and creating payments.
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
                CanProcessPayment(),
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
        List payments.
        """

        queryset = PaymentSelector.queryset()

        page = self.paginate_queryset(
            queryset,
        )

        if page is not None:
            serializer = PaymentListSerializer(
                page,
                many=True,
            )

            return self.get_paginated_response(
                serializer.data,
            )

        serializer = PaymentListSerializer(
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
        Create a payment.
        """

        serializer = PaymentCreateSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        payment = PaymentService.create(
            validated_data=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = PaymentSerializer(
            payment,
        )

        return success_response(
            message="Payment recorded successfully.",
            data=response_serializer.data,
            status_code=201,
        )


@extend_schema(tags=PAYMENT_TAG)
class PaymentRetrieveAPIView(APIView):
    """
    Retrieve a payment.
    """

    permission_classes = (IsAuthenticated, CanViewInvoice)

    def get(
        self,
        request: Request,
        payment_id: str,
    ) -> Response:
        """
        Retrieve a payment.
        """

        payment = PaymentSelector.get(
            payment_id=payment_id,
        )

        serializer = PaymentSerializer(
            payment,
        )

        return success_response(
            data=serializer.data,
        )


@extend_schema(tags=PAYMENT_TAG)
class PaymentBulkCreateAPIView(APIView):
    """
    Bulk create payments.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create multiple payments.
        """

        if not isinstance(request.data, list):
            return error_response(
                message="Expected a list of payments.",
                status_code=400,
            )

        serializer = PaymentCreateSerializer(
            data=request.data,
            many=True,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        payments = PaymentService.bulk_create(
            validated_data_list=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = PaymentSerializer(
            payments,
            many=True,
        )

        return success_response(
            message="Payments created successfully.",
            data=response_serializer.data,
            status_code=201,
        )


__all__ = [
    "PaymentBulkCreateAPIView",
    "PaymentListCreateAPIView",
    "PaymentRetrieveAPIView",
]
