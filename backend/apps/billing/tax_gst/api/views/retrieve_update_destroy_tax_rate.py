"""
API views for retrieving, updating, and deleting tax_rate records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.tax_gst.api.serializers import (
    TaxRateDetailSerializer,
    TaxRateUpdateSerializer,
)
from apps.billing.tax_gst.models import TaxRate
from apps.billing.tax_gst.permissions import (
    CanDeleteTaxGst,
    CanUpdateTaxGst,
    CanViewTaxGst,
)
from apps.billing.tax_gst.selectors import TaxRateSelector
from apps.billing.tax_gst.services import TaxRateService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

Taxrate_TAG: Final[tuple[str, ...]] = ("Tax and GST",)


@extend_schema(tags=Taxrate_TAG)
class TaxRateRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a tax_rate.
    """

    lookup_url_kwarg = "tax_rate_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewTaxGst,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateTaxGst,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateTaxGst,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteTaxGst,
        ),
    }

    serializer_class = TaxRateDetailSerializer

    serializer_classes = {
        "GET": TaxRateDetailSerializer,
        "PUT": TaxRateUpdateSerializer,
        "PATCH": TaxRateUpdateSerializer,
    }

    update_service = TaxRateService.update

    delete_service = TaxRateService.delete

    def get_object(
        self,
    ) -> TaxRate:
        """
        Return the requested tax_rate.
        """

        return TaxRateSelector.get(
            tax_rate_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "TaxRateRetrieveUpdateDestroyAPIView",
]
