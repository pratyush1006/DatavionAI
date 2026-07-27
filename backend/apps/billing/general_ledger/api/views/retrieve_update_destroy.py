"""
API views for retrieving, updating, and deleting general ledger accounts.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.billing.general_ledger.api.serializers import (
    GeneralLedgerAccountDetailSerializer,
    GeneralLedgerAccountUpdateSerializer,
)
from apps.billing.general_ledger.models import GeneralLedgerAccount
from apps.billing.general_ledger.permissions import (
    CanDeleteGeneralLedgerAccount,
    CanUpdateGeneralLedgerAccount,
    CanViewGeneralLedgerAccount,
)
from apps.billing.general_ledger.selectors import GeneralLedgerSelector
from apps.billing.general_ledger.services import GeneralLedgerService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)

GENERAL_LEDGER_TAG: Final[tuple[str, ...]] = ("General Ledger",)


@extend_schema(tags=GENERAL_LEDGER_TAG)
class GeneralLedgerAccountRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a general ledger account.
    """

    lookup_url_kwarg = "account_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewGeneralLedgerAccount,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateGeneralLedgerAccount,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateGeneralLedgerAccount,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteGeneralLedgerAccount,
        ),
    }

    serializer_class = GeneralLedgerAccountDetailSerializer

    serializer_classes = {
        "GET": GeneralLedgerAccountDetailSerializer,
        "PUT": GeneralLedgerAccountUpdateSerializer,
        "PATCH": GeneralLedgerAccountUpdateSerializer,
    }

    update_service = GeneralLedgerService.update

    delete_service = GeneralLedgerService.delete

    def get_object(
        self,
    ) -> GeneralLedgerAccount:
        """
        Return the requested general ledger account.
        """

        return GeneralLedgerSelector.get(
            account_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "GeneralLedgerAccountRetrieveUpdateDestroyAPIView",
]
