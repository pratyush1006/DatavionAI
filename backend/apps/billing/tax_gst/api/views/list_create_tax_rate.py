"""
API views for listing and creating tax_rate records.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.billing.tax_gst.api.serializers import (
    TaxRateCreateSerializer,
    TaxRateDetailSerializer,
    TaxRateListSerializer,
)
from apps.billing.tax_gst.models import TaxRate
from apps.billing.tax_gst.permissions import (
    CanCreateTaxGst,
    CanViewTaxGst,
)
from apps.billing.tax_gst.selectors import TaxRateSelector
from apps.billing.tax_gst.services import TaxRateService
from apps.common.api.base_generics import BaseListCreateAPIView

TAXRATE_TAG: Final[tuple[str, ...]] = ("Tax and GST",)


@extend_schema(tags=TAXRATE_TAG)
class TaxRateListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating tax_rate records.
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
        "GET": TaxRateListSerializer,
        "POST": TaxRateCreateSerializer,
    }

    detail_serializer_class = TaxRateDetailSerializer

    create_service = TaxRateService.create

    create_success_message = "TaxRate created successfully."

    search_fields = (
        "code",
        "name",
        "rate",
        "tax_type",
        "is_active",
    )

    ordering = ("created_at",)

    ordering_fields = ("created_at",)

    filterset_fields = (
        "organization",
        "is_active",
        "tax_type",
    )

    def get_queryset(
        self,
    ) -> QuerySet[TaxRate]:
        """
        Return the tax_rate queryset.
        """

        return TaxRateSelector.queryset()


__all__ = [
    "TaxRateListCreateAPIView",
]
