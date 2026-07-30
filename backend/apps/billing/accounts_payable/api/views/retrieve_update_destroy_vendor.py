"""
API views for retrieving, updating, and deleting vendor records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.accounts_payable.api.serializers import (
    VendorDetailSerializer,
    VendorUpdateSerializer,
)
from apps.billing.accounts_payable.models import Vendor
from apps.billing.accounts_payable.permissions import (
    CanDeleteAccountsPayable,
    CanUpdateAccountsPayable,
    CanViewAccountsPayable,
)
from apps.billing.accounts_payable.selectors import VendorSelector
from apps.billing.accounts_payable.services import VendorService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

Vendor_TAG: Final[tuple[str, ...]] = ("Accounts Payable",)


@extend_schema(tags=Vendor_TAG)
class VendorRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a vendor.
    """

    lookup_url_kwarg = "vendor_id"

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

    serializer_class = VendorDetailSerializer

    serializer_classes = {
        "GET": VendorDetailSerializer,
        "PUT": VendorUpdateSerializer,
        "PATCH": VendorUpdateSerializer,
    }

    update_service = VendorService.update

    delete_service = VendorService.delete

    def get_object(
        self,
    ) -> Vendor:
        """
        Return the requested vendor.
        """

        return VendorSelector.get(
            vendor_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "VendorRetrieveUpdateDestroyAPIView",
]
