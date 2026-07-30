"""
API views for listing and creating vendor_invoice records.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.billing.accounts_payable.api.serializers import (
    VendorInvoiceCreateSerializer,
    VendorInvoiceDetailSerializer,
    VendorInvoiceListSerializer,
)
from apps.billing.accounts_payable.models import VendorInvoice
from apps.billing.accounts_payable.permissions import (
    CanCreateAccountsPayable,
    CanViewAccountsPayable,
)
from apps.billing.accounts_payable.selectors import VendorInvoiceSelector
from apps.billing.accounts_payable.services import VendorInvoiceService
from apps.common.api.base_generics import BaseListCreateAPIView

VENDORINVOICE_TAG: Final[tuple[str, ...]] = ("Accounts Payable",)


@extend_schema(tags=VENDORINVOICE_TAG)
class VendorInvoiceListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating vendor_invoice records.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAccountsPayable,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateAccountsPayable,
        ),
    }

    serializer_classes = {
        "GET": VendorInvoiceListSerializer,
        "POST": VendorInvoiceCreateSerializer,
    }

    detail_serializer_class = VendorInvoiceDetailSerializer

    create_service = VendorInvoiceService.create

    create_success_message = "VendorInvoice created successfully."

    search_fields = (
        "invoice_number",
        "vendor",
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
    ) -> QuerySet[VendorInvoice]:
        """
        Return the vendor_invoice queryset.
        """

        return VendorInvoiceSelector.queryset()


__all__ = [
    "VendorInvoiceListCreateAPIView",
]
