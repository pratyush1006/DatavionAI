"""
API views for retrieving, updating, and deleting bank_account records.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.billing.cash_management.api.serializers import (
    BankAccountDetailSerializer,
    BankAccountUpdateSerializer,
)
from apps.billing.cash_management.models import BankAccount
from apps.billing.cash_management.permissions import (
    CanDeleteCashManagement,
    CanUpdateCashManagement,
    CanViewCashManagement,
)
from apps.billing.cash_management.selectors import BankAccountSelector
from apps.billing.cash_management.services import BankAccountService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)

Bankaccount_TAG: Final[tuple[str, ...]] = ("Cash Management",)


@extend_schema(tags=Bankaccount_TAG)
class BankAccountRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a bank_account.
    """

    lookup_url_kwarg = "bank_account_id"

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

    serializer_class = BankAccountDetailSerializer

    serializer_classes = {
        "GET": BankAccountDetailSerializer,
        "PUT": BankAccountUpdateSerializer,
        "PATCH": BankAccountUpdateSerializer,
    }

    update_service = BankAccountService.update

    delete_service = BankAccountService.delete

    def get_object(
        self,
    ) -> BankAccount:
        """
        Return the requested bank_account.
        """

        return BankAccountSelector.get(
            bank_account_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "BankAccountRetrieveUpdateDestroyAPIView",
]
