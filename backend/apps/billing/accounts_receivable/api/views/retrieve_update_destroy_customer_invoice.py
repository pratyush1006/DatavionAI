"""
API views for retrieving, updating, and deleting customer_invoice records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.accounts_receivable.api.serializers import (
    CustomerInvoiceDetailSerializer,
    CustomerInvoiceUpdateSerializer,
)
from apps.billing.accounts_receivable.models import CustomerInvoice
from apps.billing.accounts_receivable.permissions import (
    CanDeleteAccountsReceivable,
    CanUpdateAccountsReceivable,
    CanViewAccountsReceivable,
)
from apps.billing.accounts_receivable.selectors import CustomerInvoiceSelector
from apps.billing.accounts_receivable.services import CustomerInvoiceService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

Customerinvoice_TAG: Final[tuple[str, ...]] = ("Accounts Receivable",)


@extend_schema(tags=Customerinvoice_TAG)
class CustomerInvoiceRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a customer_invoice.
    """

    lookup_url_kwarg = "customer_invoice_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAccountsReceivable,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateAccountsReceivable,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateAccountsReceivable,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteAccountsReceivable,
        ),
    }

    serializer_class = CustomerInvoiceDetailSerializer

    serializer_classes = {
        "GET": CustomerInvoiceDetailSerializer,
        "PUT": CustomerInvoiceUpdateSerializer,
        "PATCH": CustomerInvoiceUpdateSerializer,
    }

    update_service = CustomerInvoiceService.update

    delete_service = CustomerInvoiceService.delete

    def get_object(
        self,
    ) -> CustomerInvoice:
        """
        Return the requested customer_invoice.
        """

        return CustomerInvoiceSelector.get(
            customer_invoice_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "CustomerInvoiceRetrieveUpdateDestroyAPIView",
]
