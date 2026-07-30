"""
API views for retrieving, updating, and deleting vendor_invoice records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.accounts_payable.api.serializers import (
    VendorInvoiceDetailSerializer,
    VendorInvoiceUpdateSerializer,
)
from apps.billing.accounts_payable.models import VendorInvoice
from apps.billing.accounts_payable.permissions import (
    CanDeleteAccountsPayable,
    CanUpdateAccountsPayable,
    CanViewAccountsPayable,
)
from apps.billing.accounts_payable.selectors import VendorInvoiceSelector
from apps.billing.accounts_payable.services import VendorInvoiceService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

Vendorinvoice_TAG: Final[tuple[str, ...]] = ("Accounts Payable",)


@extend_schema(tags=Vendorinvoice_TAG)
class VendorInvoiceRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a vendor_invoice.
    """

    lookup_url_kwarg = "vendor_invoice_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAccountsPayable,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateAccountsPayable,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateAccountsPayable,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteAccountsPayable,
        ),
    }

    serializer_class = VendorInvoiceDetailSerializer

    serializer_classes = {
        "GET": VendorInvoiceDetailSerializer,
        "PUT": VendorInvoiceUpdateSerializer,
        "PATCH": VendorInvoiceUpdateSerializer,
    }

    update_service = VendorInvoiceService.update

    delete_service = VendorInvoiceService.delete

    def get_object(
        self,
    ) -> VendorInvoice:
        """
        Return the requested vendor_invoice.
        """

        return VendorInvoiceSelector.get(
            vendor_invoice_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "VendorInvoiceRetrieveUpdateDestroyAPIView",
]
