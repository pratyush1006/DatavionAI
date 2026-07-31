"""
API views for listing and creating tax_filing records.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.billing.tax_gst.api.serializers import (
    TaxFilingCreateSerializer,
    TaxFilingDetailSerializer,
    TaxFilingListSerializer,
)
from apps.billing.tax_gst.models import TaxFiling
from apps.billing.tax_gst.permissions import (
    CanCreateTaxGst,
    CanViewTaxGst,
)
from apps.billing.tax_gst.selectors import TaxFilingSelector
from apps.billing.tax_gst.services import TaxFilingService
from apps.common.api.base_generics import BaseListCreateAPIView

TAXFILING_TAG: Final[tuple[str, ...]] = ("Tax and GST",)


@extend_schema(tags=TAXFILING_TAG)
class TaxFilingListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating tax_filing records.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewTaxGst,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateTaxGst,
        ),
    }

    serializer_classes = {
        "GET": TaxFilingListSerializer,
        "POST": TaxFilingCreateSerializer,
    }

    detail_serializer_class = TaxFilingDetailSerializer

    create_service = TaxFilingService.create

    create_success_message = "TaxFiling created successfully."

    search_fields = (
        "period",
        "tax_rate",
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
    ) -> QuerySet[TaxFiling]:
        """
        Return the tax_filing queryset.
        """

        return TaxFilingSelector.queryset()


__all__ = [
    "TaxFilingListCreateAPIView",
]
