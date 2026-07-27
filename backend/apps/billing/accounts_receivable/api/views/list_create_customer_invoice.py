"""
API views for listing and creating customer_invoice records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.accounts_receivable.api.serializers import (
    CustomerInvoiceCreateSerializer,
    CustomerInvoiceDetailSerializer,
    CustomerInvoiceListSerializer,
)
from apps.billing.accounts_receivable.models import CustomerInvoice
from apps.billing.accounts_receivable.permissions import (
    CanCreateAccountsReceivable,
    CanViewAccountsReceivable,
)
from apps.billing.accounts_receivable.selectors import CustomerInvoiceSelector
from apps.billing.accounts_receivable.services import CustomerInvoiceService
from apps.common.api.base_generics import BaseListCreateAPIView
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

CUSTOMERINVOICE_TAG: Final[tuple[str, ...]] = ("Accounts Receivable",)


@extend_schema(tags=CUSTOMERINVOICE_TAG)
class CustomerInvoiceListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating customer_invoice records.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAccountsReceivable,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateAccountsReceivable,
        ),
    }

    serializer_classes = {
        "GET": CustomerInvoiceListSerializer,
        "POST": CustomerInvoiceCreateSerializer,
    }

    detail_serializer_class = CustomerInvoiceDetailSerializer

    create_service = CustomerInvoiceService.create

    create_success_message = "CustomerInvoice created successfully."

    search_fields = (
        "invoice_number",
        "customer",
        "amount",
        "due_date",
        "status",
        "is_active",
    )

    ordering = ("created_at",)

    ordering_fields = ("created_at",)

    filterset_fields = (
        "organization",
        "is_active",
        "status",
    )

    def get_queryset(
        self,
    ) -> QuerySet[CustomerInvoice]:
        """
        Return the customer_invoice queryset.
        """

        return CustomerInvoiceSelector.queryset()


__all__ = [
    "CustomerInvoiceListCreateAPIView",
]
