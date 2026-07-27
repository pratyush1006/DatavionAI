"""
API views for retrieving, updating, and deleting tax_filing records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.tax_gst.api.serializers import (
    TaxFilingDetailSerializer,
    TaxFilingUpdateSerializer,
)
from apps.billing.tax_gst.models import TaxFiling
from apps.billing.tax_gst.permissions import (
    CanDeleteTaxGst,
    CanUpdateTaxGst,
    CanViewTaxGst,
)
from apps.billing.tax_gst.selectors import TaxFilingSelector
from apps.billing.tax_gst.services import TaxFilingService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

Taxfiling_TAG: Final[tuple[str, ...]] = ("Tax and GST",)


@extend_schema(tags=Taxfiling_TAG)
class TaxFilingRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a tax_filing.
    """

    lookup_url_kwarg = "tax_filing_id"

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

    serializer_class = TaxFilingDetailSerializer

    serializer_classes = {
        "GET": TaxFilingDetailSerializer,
        "PUT": TaxFilingUpdateSerializer,
        "PATCH": TaxFilingUpdateSerializer,
    }

    update_service = TaxFilingService.update

    delete_service = TaxFilingService.delete

    def get_object(
        self,
    ) -> TaxFiling:
        """
        Return the requested tax_filing.
        """

        return TaxFilingSelector.get(
            tax_filing_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "TaxFilingRetrieveUpdateDestroyAPIView",
]
