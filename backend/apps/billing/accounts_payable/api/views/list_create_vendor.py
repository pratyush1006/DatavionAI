"""
API views for listing and creating vendor records.
"""

from __future__ import annotations

from typing import Final

from apps.billing.accounts_payable.api.serializers import (
    VendorCreateSerializer,
    VendorDetailSerializer,
    VendorListSerializer,
)
from apps.billing.accounts_payable.models import Vendor
from apps.billing.accounts_payable.permissions import (
    CanCreateAccountsPayable,
    CanViewAccountsPayable,
)
from apps.billing.accounts_payable.selectors import VendorSelector
from apps.billing.accounts_payable.services import VendorService
from apps.common.api.base_generics import BaseListCreateAPIView
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

VENDOR_TAG: Final[tuple[str, ...]] = ("Accounts Payable",)


@extend_schema(tags=VENDOR_TAG)
class VendorListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing and creating vendor records.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAccountsPayable,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateAccountsPayable,
        ),
    }

    serializer_classes = {
        "GET": VendorListSerializer,
        "POST": VendorCreateSerializer,
    }

    detail_serializer_class = VendorDetailSerializer

    create_service = VendorService.create

    create_success_message = "Vendor created successfully."

    search_fields = (
        "code",
        "name",
        "email",
        "is_active",
    )

    ordering = ("created_at",)

    ordering_fields = ("created_at",)

    filterset_fields = (
        "organization",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Vendor]:
        """
        Return the vendor queryset.
        """

        return VendorSelector.queryset()


__all__ = [
    "VendorListCreateAPIView",
]
