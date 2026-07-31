"""
API views for retrieving, updating, and deleting customer records.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.billing.accounts_receivable.api.serializers import (
    CustomerDetailSerializer,
    CustomerUpdateSerializer,
)
from apps.billing.accounts_receivable.models import Customer
from apps.billing.accounts_receivable.permissions import (
    CanDeleteAccountsReceivable,
    CanUpdateAccountsReceivable,
    CanViewAccountsReceivable,
)
from apps.billing.accounts_receivable.selectors import CustomerSelector
from apps.billing.accounts_receivable.services import CustomerService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)

Customer_TAG: Final[tuple[str, ...]] = ("Accounts Receivable",)


@extend_schema(tags=Customer_TAG)
class CustomerRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a customer.
    """

    lookup_url_kwarg = "customer_id"

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

    serializer_class = CustomerDetailSerializer

    serializer_classes = {
        "GET": CustomerDetailSerializer,
        "PUT": CustomerUpdateSerializer,
        "PATCH": CustomerUpdateSerializer,
    }

    update_service = CustomerService.update

    delete_service = CustomerService.delete

    def get_object(
        self,
    ) -> Customer:
        """
        Return the requested customer.
        """

        return CustomerSelector.get(
            customer_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "CustomerRetrieveUpdateDestroyAPIView",
]
