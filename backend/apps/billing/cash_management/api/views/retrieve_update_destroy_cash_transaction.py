"""
API views for retrieving, updating, and deleting cash_transaction records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.cash_management.api.serializers import (
    CashTransactionDetailSerializer,
    CashTransactionUpdateSerializer,
)
from apps.billing.cash_management.models import CashTransaction
from apps.billing.cash_management.permissions import (
    CanDeleteCashManagement,
    CanUpdateCashManagement,
    CanViewCashManagement,
)
from apps.billing.cash_management.selectors import CashTransactionSelector
from apps.billing.cash_management.services import CashTransactionService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

Cashtransaction_TAG: Final[tuple[str, ...]] = ("Cash Management",)


@extend_schema(tags=Cashtransaction_TAG)
class CashTransactionRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a cash_transaction.
    """

    lookup_url_kwarg = "cash_transaction_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewCashManagement,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateCashManagement,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateCashManagement,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteCashManagement,
        ),
    }

    serializer_class = CashTransactionDetailSerializer

    serializer_classes = {
        "GET": CashTransactionDetailSerializer,
        "PUT": CashTransactionUpdateSerializer,
        "PATCH": CashTransactionUpdateSerializer,
    }

    update_service = CashTransactionService.update

    delete_service = CashTransactionService.delete

    def get_object(
        self,
    ) -> CashTransaction:
        """
        Return the requested cash_transaction.
        """

        return CashTransactionSelector.get(
            cash_transaction_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "CashTransactionRetrieveUpdateDestroyAPIView",
]
